"""In-memory storage for vector stores and video data"""
from typing import Dict, Any, List
from app.models.models import ConversationMessage

# Global storage (in production, use a database)
vector_stores: Dict[str, Any] = {}
video_info: Dict[str, Dict] = {}
video_transcripts: Dict[str, List[Dict]] = {}  # Store full transcripts with timestamps
video_metadata: Dict[str, Dict] = {}  # Store YouTube metadata
web_vector_stores: Dict[str, Any] = {}  # Store web search results per video
conversation_sessions: Dict[str, List[ConversationMessage]] = {}  # Store conversation history per video
