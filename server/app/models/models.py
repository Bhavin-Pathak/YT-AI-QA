"""Pydantic models for request/response validation"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class VideoRequest(BaseModel):
    video_url: str


class ConversationMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class QuestionRequest(BaseModel):
    """
    Schema for question asking request.
    Includes the question and optional context like video ID and history.
    """
    question: str
    video_id: Optional[str] = None
    conversation_history: Optional[List[ConversationMessage]] = []


class VideoResponse(BaseModel):
    video_id: str
    title: str
    transcript_length: int
    chunks_created: int
    status: str
    channel: Optional[str] = None
    publish_date: Optional[str] = None


class AnswerResponse(BaseModel):
    question: str
    answer: str
    context: List[str]
    sources: List[Dict[str, Any]]
    video_id: str
    answer_type: Optional[str] = "video_content"  # "video_content" or "hybrid"
    metadata_used: Optional[Dict[str, Any]] = None


class HighlightPoint(BaseModel):
    timestamp: str
    main_point: str
    sub_points: List[str]


class SummaryResponse(BaseModel):
    video_id: str
    overall_summary: str
    highlights: List[HighlightPoint]
    status: str


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
