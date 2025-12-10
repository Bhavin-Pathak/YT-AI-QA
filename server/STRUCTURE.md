# Backend Structure

The backend has been restructured into a modular, maintainable architecture.

## 📁 Directory Structure

```
backend/
├── main.py                      # FastAPI application entry point
├── config.py                    # Configuration and environment variables
├── models.py                    # Pydantic models for request/response
├── storage.py                   # In-memory storage (vector stores, etc.)
├── requirements.txt             # Python dependencies
│
├── routes/                      # API route handlers
│   ├── __init__.py
│   ├── video_routes.py          # Video processing endpoints
│   ├── question_routes.py       # Question answering endpoints
│   └── summary_routes.py        # Summary generation endpoints
│
├── services/                    # Business logic layer
│   ├── __init__.py
│   ├── video_processor.py       # Video processing service
│   ├── rag_service.py           # RAG question answering service
│   └── summary_service.py       # Summary generation service
│
└── utils/                       # Utility functions
    ├── __init__.py
    ├── youtube_utils.py         # YouTube-related utilities
    ├── web_utils.py             # Web search and scraping
    └── rag_utils.py             # RAG pipeline utilities
```

## 🔧 Components

### Core Files

- **`main.py`**: FastAPI app initialization, CORS middleware, route registration
- **`config.py`**: All configuration settings, environment variables, constants
- **`models.py`**: Pydantic models for API validation
- **`storage.py`**: In-memory data storage (use database in production)

### Routes (`routes/`)

API endpoints organized by functionality:
- **Video Routes**: `/videos/process`, `/videos/list`, `/videos/{id}`
- **Question Routes**: `/questions/ask`, `/questions/conversation/{id}`
- **Summary Routes**: `/summary/{id}`

### Services (`services/`)

Business logic separated from routes:
- **`video_processor.py`**: Handles video processing, transcript fetching, vector store creation
- **`rag_service.py`**: RAG pipeline, question classification, answer generation
- **`summary_service.py`**: Video summary generation with timestamps

### Utilities (`utils/`)

Reusable helper functions:
- **`youtube_utils.py`**: Video ID extraction, metadata fetching, timestamp formatting
- **`web_utils.py`**: Web search, webpage scraping
- **`rag_utils.py`**: Question classification, context compression, optimal k calculation

## 🚀 Running the Application

### Development

```bash
cd backend
python main.py
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

## 🔄 Migration from `start.py`

The old monolithic `start.py` (900+ lines) has been split into:
- 1 main file (50 lines)
- 3 route files (~50-100 lines each)
- 3 service files (~100-200 lines each)  
- 3 utility files (~50-150 lines each)
- 1 config file (~50 lines)
- 2 model files (~50 lines each)

### Benefits

✅ **Maintainability**: Each file has a single responsibility
✅ **Testability**: Services and utilities can be tested independently
✅ **Scalability**: Easy to add new features without modifying existing code
✅ **Readability**: Shorter files, clear organization
✅ **Collaboration**: Multiple developers can work on different modules
✅ **Reusability**: Utilities and services can be imported anywhere

## 📝 API Endpoints

### Video Processing
- `POST /videos/process` - Process a YouTube video
- `GET /videos/list` - List all processed videos
- `DELETE /videos/{video_id}` - Delete a video

### Question Answering
- `POST /questions/ask` - Ask a question about a video
- `GET /questions/conversation/{video_id}` - Get conversation history
- `DELETE /questions/conversation/{video_id}` - Clear conversation

### Summary
- `POST /summary/{video_id}` - Generate timestamped summary

### Health
- `GET /` - API info
- `GET /health` - Health check

## 🔧 Configuration

All settings are in `config.py`. Set environment variables in `.env`:

```env
HUGGINGFACE_API_TOKEN=your_token_here
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
YOUTUBE_API_KEY=optional
```

## 📦 Dependencies

Same as before - see `requirements.txt`. No new dependencies added.
