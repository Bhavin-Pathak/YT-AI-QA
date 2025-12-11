"""Video processing service"""
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from typing import Dict, Any, List
from app.core.config import (
    CHUNK_SIZE, 
    CHUNK_OVERLAP, 
    OLLAMA_EMBEDDING_MODEL, 
    OLLAMA_BASE_URL
)
from app.core.storage import vector_stores, video_info, video_transcripts, video_metadata
from app.utils.youtube_utils import extract_video_id, fetch_youtube_metadata

# Helper function to create metadata documents (refactored from utils or kept inline if simple)
def create_metadata_documents(metadata: Dict[str, Any], video_id: str):
    from langchain_core.documents import Document
    
    docs = []
    
    # Title document
    if "title" in metadata:
        docs.append(Document(
            page_content=f"Video Title: {metadata['title']}",
            metadata={
                "video_id": video_id,
                "type": "metadata",
                "source": "title",
                "importance": "high"
            }
        ))
        
    # Description document
    if "description" in metadata:
        docs.append(Document(
            page_content=f"Video Description: {metadata['description']}",
            metadata={
                "video_id": video_id,
                "type": "metadata",
                "source": "description",
                "importance": "medium"
            }
        ))
        
    # Channel document
    if "channel_name" in metadata:
        docs.append(Document(
            page_content=f"Channel: {metadata['channel_name']}",
            metadata={
                "video_id": video_id,
                "type": "metadata",
                "source": "channel",
                "importance": "low"
            }
        ))
        
    return docs

def process_video(video_url: str) -> Dict[str, Any]:
    """
    Process a YouTube video and create vector store.
    
    1. Extracts video ID
    2. Fetches metadata
    3. Fetches transcript
    4. Chunks transcript
    5. Creates embeddings and vector store
    
    Args:
        video_url: URL of the YouTube video
        
    Returns:
        Dict: Processing results and status
    """
    # Extract video ID
    video_id = extract_video_id(video_url)
    
    # Check if already processed
    if video_id in vector_stores:
        return {
            "video_id": video_id,
            "title": video_info[video_id].get("title", "Unknown"),
            "transcript_length": video_info[video_id].get("transcript_length", 0),
            "chunks_created": video_info[video_id].get("chunks_created", 0),
            "status": "already_processed"
        }
    
    # Fetch metadata
    print(f"Fetching metadata for video {video_id}...")
    metadata = fetch_youtube_metadata(video_id)
    video_metadata[video_id] = metadata
    
    # Get transcript
    try:
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id, languages=["en"])
        
        # Store transcript with timestamps
        transcript_with_timestamps = []
        for snippet in transcript_obj.snippets:
            transcript_with_timestamps.append({
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration
            })
        video_transcripts[video_id] = transcript_with_timestamps
        
        transcript = " ".join(snippet.text for snippet in transcript_obj.snippets)
    except TranscriptsDisabled:
        raise ValueError("No captions available for this video")
    except Exception as e:
        raise ValueError(f"Error fetching transcript: {str(e)}")
    
    # Split transcript into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    transcript_chunks = splitter.create_documents([transcript])
    
    # Add metadata to chunks
    for idx, chunk in enumerate(transcript_chunks):
        chunk.metadata.update({
            "video_id": video_id,
            "type": "transcript",
            "source": "youtube_transcript",
            "chunk_index": idx,
            "total_chunks": len(transcript_chunks)
        })
    
    # Create metadata documents
    metadata_docs = create_metadata_documents(metadata, video_id)
    
    # Combine all documents
    all_documents = transcript_chunks + metadata_docs
    
    print(f"Created {len(transcript_chunks)} transcript chunks and {len(metadata_docs)} metadata documents")
    
    # Create embeddings and vector store using Ollama
    embeddings = OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    vector_store = FAISS.from_documents(all_documents, embeddings)
    
    # Store results
    vector_stores[video_id] = vector_store
    video_info[video_id] = {
        "title": metadata.get("title", f"Video {video_id}"),
        "transcript_length": len(transcript),
        "chunks_created": len(all_documents),
        "url": video_url,
        "channel": metadata.get("channel_name", "Unknown"),
        "publish_date": metadata.get("publish_date", "Unknown"),
        "description": metadata.get("description", "")[:200]
    }
    
    return {
        "video_id": video_id,
        "title": video_info[video_id]["title"],
        "transcript_length": len(transcript),
        "chunks_created": len(all_documents),
        "status": "processed",
        "channel": video_info[video_id].get("channel"),
        "publish_date": video_info[video_id].get("publish_date")
    }
