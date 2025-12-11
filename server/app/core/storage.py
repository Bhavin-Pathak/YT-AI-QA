"""In-memory storage for vector stores and video data"""
from typing import Dict, Any, List
from app.models.models import ConversationMessage

# Global storage (in production, use a database)
# Global storage dictionaries (in production, these should be replaced by a persistent database like PostgreSQL/Redis/Milvus)
vector_stores: Dict[str, Any] = {}  # In-memory FAISS vector stores keyed by video_id
video_info: Dict[str, Dict] = {}    # Basic video information (title, length, etc.) keyed by video_id
video_transcripts: Dict[str, List[Dict]] = {}  # Full transcripts with timestamp data keyed by video_id
video_metadata: Dict[str, Dict] = {}  # Raw YouTube metadata (view count, author, etc.) keyed by video_id
web_vector_stores: Dict[str, Any] = {}  # (Optional) Vector stores for web search results, keyed by video_id
conversation_sessions: Dict[str, List[ConversationMessage]] = {}  # Chat history for context-aware RAG, keyed by session/video_id
