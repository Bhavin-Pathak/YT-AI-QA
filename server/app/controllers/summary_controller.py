"""Summary generation routes"""
from fastapi import APIRouter, HTTPException, Body
from app.models.models import SummaryResponse
from app.services.summary_service import generate_summary
from typing import Dict

router = APIRouter(prefix="/summaries", tags=["summary"])


# Routes for summary generation
# This endpoint matches the frontend requirement to POST to /summaries/generate

@router.post("/generate", response_model=SummaryResponse)
async def generate_summary_endpoint(payload: Dict[str, str] = Body(...)):
    """
    Generate comprehensive timestamped summary for a processed video.
    
    Args:
        payload: Dict containing 'video_id'.
        
    Returns:
        SummaryResponse: Structured summary with timestamps.
    """
    video_id = payload.get("video_id")
    if not video_id:
        raise HTTPException(status_code=400, detail="video_id is required")
        
    try:
        result = generate_summary(video_id)
        return SummaryResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@router.get("/{video_id}")
async def get_summary_endpoint(video_id: str):
    """Get summary if exists (placeholder if needed)"""
    # Previously implemented?
    # Logic same as generate mostly if caching is used.
    # For now just generate.
    pass
