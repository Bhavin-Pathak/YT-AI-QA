"""Configuration settings for the RAG YouTube Assistant"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

# YouTube API Key (optional)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# RAG parameters
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
DEFAULT_K = 3
MAX_K = 6
MIN_K = 2

# Context compression settings
MAX_CONTEXT_LENGTH = 1500
COMPRESSION_ENABLED = True

# Conversation settings
MAX_CONVERSATION_MESSAGES = 5
MAX_CONVERSATION_HISTORY = 10

# Summary settings
SUMMARY_INTERVAL_SECONDS = 480  # 8 minutes
MAX_SUMMARY_SEGMENTS = 10

# Web search settings
WEB_SEARCH_RESULTS = 5
WEB_SEARCH_TOP_PAGES = 2
MAX_WEBPAGE_CONTENT = 3000
