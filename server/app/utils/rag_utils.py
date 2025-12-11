"""RAG pipeline utilities"""
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_community.llms import Ollama
from app.models.models import ConversationMessage
from app.core.config import (
    OLLAMA_BASE_URL, OLLAMA_MODEL, MAX_CONTEXT_LENGTH, 
    MAX_CONVERSATION_MESSAGES, DEFAULT_K, MAX_K, MIN_K,
    WEB_SEARCH_TOP_PAGES
)
from app.utils.web_utils import search_web, fetch_webpage_content


def classify_question(question: str) -> str:
    """
    Classify a question to determine the retrieval strategy.
    
    Categories:
    - video_content: Questions about the video content itself (default).
    - external_knowledge: Questions requiring fact-checking or broader context.
    
    Args:
        question: The user query string.
        
    Returns:
        str: Classification label ('video_content' or 'external_knowledge').
    """
    # Video-specific indicators
    video_indicators = [
        "in this video", "in the video", "speaker says", "speaker mentions",
        "what does the speaker", "according to the video", "video explains",
        "video discusses", "mentioned in", "talked about", "presenter says",
        "host says", "in this episode", "in this conversation"
    ]
    
    # External knowledge indicators
    external_indicators = [
        "is this correct", "is this true", "compare with", "real-world examples",
        "how does this compare", "what are other", "alternative to",
        "in general", "scientific evidence", "research shows",
        "according to experts", "fact check", "verify", "true or false"
    ]
    
    question_lower = question.lower()
    
    # Check for video-specific questions
    for indicator in video_indicators:
        if indicator in question_lower:
            return "video_content"
    
    # Check for external knowledge questions
    for indicator in external_indicators:
        if indicator in question_lower:
            return "external_knowledge"
    
    return "video_content"


def get_optimal_k(video_length: int, question: str) -> int:
    """Dynamically determine optimal k based on video length and question complexity"""
    k = DEFAULT_K
    
    # Adjust based on video length
    if video_length > 50000:
        k = 5
    elif video_length > 20000:
        k = 4
    elif video_length < 5000:
        k = 2
    
    # Adjust based on question complexity
    question_words = len(question.split())
    if question_words > 20:
        k = min(k + 1, MAX_K)
    elif question_words < 5:
        k = max(k - 1, MIN_K)
    
    return k


def format_conversation_history(history: List[ConversationMessage], max_messages: int = MAX_CONVERSATION_MESSAGES) -> str:
    """Format conversation history for inclusion in prompts"""
    if not history:
        return ""
    
    recent_history = history[-max_messages:] if len(history) > max_messages else history
    
    formatted = "Previous conversation:\n"
    for msg in recent_history:
        role = "User" if msg.role == "user" else "Assistant"
        formatted += f"{role}: {msg.content}\n"
    
    return formatted + "\n"


def compress_context(context_chunks: List[str], question: str, max_length: int = MAX_CONTEXT_LENGTH) -> str:
    """Compress retrieved context chunks using LLM summarization"""
    if not context_chunks:
        return ""
    
    combined_context = "\n\n".join(context_chunks)
    if len(combined_context) <= max_length:
        return combined_context
    
    llm = Ollama(
        model=OLLAMA_MODEL,
        temperature=0.1,
        base_url=OLLAMA_BASE_URL
    )
    
    compression_prompt = f"""You are a context compression assistant. Your job is to summarize and condense the following context chunks while preserving all key information relevant to the question.

Question: {question}

Context chunks to compress:
{combined_context[:3000]}

Provide a concise but complete summary that includes:
1. All facts and details relevant to the question
2. Key points and arguments
3. Important examples or evidence
4. Maintain chronological order if applicable

Compressed context (max 400 words):"""
    
    try:
        compressed = llm.invoke(compression_prompt)
        if isinstance(compressed, dict):
            compressed = compressed.get('response', '') or str(compressed)
        compressed_text = str(compressed).strip()
        
        if len(compressed_text) > max_length:
            compressed_text = compressed_text[:max_length] + "..."
        
        return compressed_text
    except Exception as e:
        print(f"Context compression error: {e}")
        return combined_context[:max_length] + "..."


def get_window_chunks(retrieved_docs: List[Document], vector_store, window_size: int = 1) -> List[Document]:
    """Retrieve neighboring chunks for better context"""
    all_docs = []
    seen_indices = set()
    
    for doc in retrieved_docs:
        chunk_index = doc.metadata.get("chunk_index")
        total_chunks = doc.metadata.get("total_chunks")
        
        if chunk_index is None:
            all_docs.append(doc)
            continue
        
        start_idx = max(0, chunk_index - window_size)
        end_idx = min(total_chunks - 1, chunk_index + window_size)
        
        for idx in range(start_idx, end_idx + 1):
            if idx not in seen_indices:
                seen_indices.add(idx)
                if idx == chunk_index:
                    all_docs.append(doc)
    
    return retrieved_docs


def create_metadata_documents(metadata: Dict[str, Any], video_id: str) -> List[Document]:
    """Create LangChain documents from video metadata"""
    docs = []
    
    if metadata.get("title"):
        docs.append(Document(
            page_content=f"Video Title: {metadata['title']}",
            metadata={"source": "title", "video_id": video_id, "type": "metadata"}
        ))
    
    if metadata.get("description"):
        docs.append(Document(
            page_content=f"Video Description: {metadata['description']}",
            metadata={"source": "description", "video_id": video_id, "type": "metadata"}
        ))
    
    if metadata.get("channel_name"):
        docs.append(Document(
            page_content=f"Channel Name: {metadata['channel_name']}. This video is published by {metadata['channel_name']}.",
            metadata={"source": "channel", "video_id": video_id, "type": "metadata"}
        ))
    
    if metadata.get("tags"):
        tags_str = ", ".join(metadata["tags"][:10])
        docs.append(Document(
            page_content=f"Video Tags/Topics: {tags_str}",
            metadata={"source": "tags", "video_id": video_id, "type": "metadata"}
        ))
    
    if metadata.get("view_count"):
        stats = f"Video Statistics: {metadata['view_count']:,} views"
        if metadata.get("like_count"):
            stats += f", {metadata['like_count']:,} likes"
        docs.append(Document(
            page_content=stats,
            metadata={"source": "statistics", "video_id": video_id, "type": "metadata"}
        ))
    
    return docs


def create_web_documents(question: str, video_context: str = "") -> List[Document]:
    """Create documents from web search results"""
    search_query = question
    if video_context:
        search_query = f"{question} {video_context[:100]}"
    
    search_results = search_web(search_query)
    
    docs = []
    for i, result in enumerate(search_results):
        content = f"{result['title']}\n\n{result['body']}"
        
        docs.append(Document(
            page_content=content,
            metadata={
                "source": "web_search",
                "url": result.get("url", ""),
                "search_rank": i + 1,
                "type": "external_knowledge"
            }
        ))
        
        if i < WEB_SEARCH_TOP_PAGES:
            webpage_content = fetch_webpage_content(result.get("url", ""))
            if webpage_content:
                docs.append(Document(
                    page_content=webpage_content,
                    metadata={
                        "source": "webpage",
                        "url": result.get("url", ""),
                        "type": "external_knowledge"
                    }
                ))
    
    return docs
