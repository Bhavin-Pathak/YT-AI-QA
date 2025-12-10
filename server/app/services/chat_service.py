"""Chat service for RAG functionality"""
from typing import List, Dict, Any, Optional
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from app.models.models import ConversationMessage
from app.core.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.core.storage import vector_stores, video_info, video_metadata
from app.utils.rag_utils import (
    classify_question, get_optimal_k, format_conversation_history,
    compress_context, get_window_chunks, create_web_documents
)

def create_rag_pipeline(video_id: str, question_type: str = "video_content", 
                       use_compression: bool = True, 
                       conversation_history: List[ConversationMessage] = None):
    """Create RAG pipeline for a video"""
    if video_id not in vector_stores:
        raise ValueError("Video not processed yet")
    
    vector_store = vector_stores[video_id]
    
    # Dynamically determine k
    video_length = video_info.get(video_id, {}).get("transcript_length", 10000)
    optimal_k = get_optimal_k(video_length, "")
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": optimal_k}
    )
    
    # Create LLM using ChatOllama
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.0 if question_type == "video_content" else 0.3,
        base_url=OLLAMA_BASE_URL
    )

    # Choose prompt template
    history_text = format_conversation_history(conversation_history) if conversation_history else ""
    
    if question_type == "video_content":
        template = f"""{history_text}Based on the following context from a YouTube video transcript, answer the question in a natural, conversational way.

Instructions:
- Provide a helpful, well-explained answer
- {'Use the conversation history above for context about follow-up questions' if history_text else 'Focus on the video content'}
- Don't just list keywords - form complete thoughts
- Be conversational and informative

Context: {{context}}

Question: {{question}}

Answer:"""
    else:
        template = f"""{history_text}You are a helpful AI assistant analyzing a YouTube video.

You are given:
1. A YouTube video transcript and metadata (partial, may be incomplete).
2. A user question.

Use the video content as your primary source.
If the video doesn't fully address the question, you may use general knowledge to provide helpful context.
Always indicate what comes from the video versus general knowledge.

Video context:
{{context}}

Question:
{{question}}

Answer (clear, structured, and honest):"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=['context', 'question']
    )
    
    def format_docs(retrieved_docs):
        """Format documents with optional compression"""
        windowed_docs = get_window_chunks(retrieved_docs, vector_store, window_size=1)
        context_chunks = [doc.page_content for doc in windowed_docs]
        
        if use_compression and len(context_chunks) > 2:
            combined = "\n\n".join(context_chunks)
            max_context_length = 2000
            if len(combined) > max_context_length:
                combined = combined[:max_context_length] + "..."
            return combined
        else:
            return "\n\n".join(context_chunks)
    
    def clean_answer(output):
        """Extract clean answer from LLM output"""
        # ChatOllama returns AIMessage object or content string depending on invoking method, 
        # but invoke() typically returns AIMessage.
        if hasattr(output, 'content'):
            text = output.content
        elif isinstance(output, dict):
            text = output.get('response', '') or output.get('text', '') or str(output)
        else:
            text = str(output)
        
        if not text:
            return ""
        
        return text.strip()
    
    # Create the chain
    chain = (
        RunnableParallel({
            'context': retriever | RunnableLambda(format_docs),
            'question': RunnablePassthrough()
        })
        | prompt
        | llm
        | RunnableLambda(clean_answer)
    )
    
    return chain, retriever


def answer_question(question: str, video_id: str = None, 
                    conversation_history: List[ConversationMessage] = None) -> Dict[str, Any]:
    """Answer a question about a video"""
    # Get most recent video if not specified
    if not video_id:
        if not vector_stores:
            raise ValueError("No videos processed yet")
        video_id = list(vector_stores.keys())[-1]
    
    if video_id not in vector_stores:
        raise ValueError("Video not found. Please process the video first.")
    
    # Classify question
    question_type = classify_question(question)
    
    # Get optimal k
    video_length = video_info.get(video_id, {}).get("transcript_length", 10000)
    optimal_k = get_optimal_k(video_length, question)
    
    # Retrieve documents
    video_vector_store = vector_stores[video_id]
    video_retriever = video_vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": optimal_k}
    )
    retrieved_docs = video_retriever.invoke(question)
    retrieved_docs = get_window_chunks(retrieved_docs, video_vector_store, window_size=1)
    
    # Collect metadata
    metadata_info = {}
    for doc in retrieved_docs:
        if doc.metadata.get("type") == "metadata":
            source = doc.metadata.get("source", "unknown")
            metadata_info[source] = doc.page_content
    
    # Extract context
    raw_context = [doc.page_content for doc in retrieved_docs]
    if len(raw_context) > 3 and question_type == "video_content":
        compressed_context = compress_context(raw_context, question, max_length=1500)
        context = [compressed_context]
    else:
        context = raw_context
    
    sources = []
    for doc in retrieved_docs:
        source_data = {
            "text": doc.page_content,
            "type": doc.metadata.get("type", "unknown"),
            "source": doc.metadata.get("source", "unknown")
        }
        
        # Try to recover timestamp info if available (heuristic or if stored)
        # Note: In video_service.py we didn't explicitly store timestamp in metadata for every chunk, 
        # but we did store chunk_index. Mapping back to timestamp would require looking up the transcript.
        # For now, we'll return what we have.
        if "start" in doc.metadata:
             source_data["timestamp"] = str(doc.metadata["start"])
        
        sources.append(source_data)
    answer_type = "video_content"
    
    # Handle external knowledge queries
    if question_type == "external_knowledge":
        video_context = ""
        if video_id in video_metadata:
            video_context = f"{video_metadata[video_id].get('title', '')} {video_metadata[video_id].get('description', '')}"
        
        web_docs = create_web_documents(question, video_context)
        
        if web_docs:
            llm = ChatOllama(
                model=OLLAMA_MODEL,
                temperature=0.3,
                base_url=OLLAMA_BASE_URL
            )
            
            video_context_text = "\n\n".join(context[:3])
            if len(video_context_text) > 1000:
                video_context_text = compress_context(context[:3], question, max_length=1000)
            
            web_context_text = "\n\n".join([doc.page_content[:800] for doc in web_docs[:3]])
            history_text = format_conversation_history(conversation_history) if conversation_history else ""
            
            hybrid_prompt = f"""{history_text}You are a helpful AI assistant.

Context from YouTube video:
{video_context_text}

Context from web search:
{web_context_text}

Question:
{question}

Answer (clear, structured, and helpful):"""
            
            answer_msg = llm.invoke(hybrid_prompt)
            answer = answer_msg.content if hasattr(answer_msg, 'content') else str(answer_msg)
            answer = answer.strip()
            answer_type = "hybrid"
            
            for doc in web_docs[:3]:
                url = doc.metadata.get("url", "")
                url = doc.metadata.get("url", "")
                if url:
                    sources.append({
                        "text": f"[Web] {doc.page_content[:150]}...",
                        "source": url,
                        "type": "web"
                    })
        else:
            chain, _ = create_rag_pipeline(video_id, "general", use_compression=True, 
                                          conversation_history=conversation_history)
            answer = chain.invoke(question)
            answer_type = "video_content"
    else:
        chain, _ = create_rag_pipeline(video_id, question_type, use_compression=True,
                                      conversation_history=conversation_history)
        answer = chain.invoke(question)
    
    return {
        "question": question,
        "answer": answer,
        "context": context,
        "sources": sources,
        "video_id": video_id,
        "answer_type": answer_type,
        "metadata_used": metadata_info if metadata_info else None
    }
