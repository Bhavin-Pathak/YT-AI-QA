"""Main FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import video_controller, chat_controller, summary_controller

app = FastAPI(
    title="YT-AI-QA",
    description="Fast API for YouTube video analysis using Ollama",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(video_controller.router)
app.include_router(chat_controller.router)
app.include_router(summary_controller.router)


@app.get("/")
async def root():
    return {
        "message": "YT-AI-QA API (Refactored)",
        "status": "server is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "server is running"}
