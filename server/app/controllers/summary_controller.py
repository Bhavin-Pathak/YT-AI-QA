"""Summary generation routes"""
from fastapi import APIRouter, HTTPException, Body
from app.models.models import SummaryResponse
from app.services.summary_service import generate_summary
from typing import Dict

router = APIRouter(prefix="/summaries", tags=["summary"])


# Note: Added /generate to match frontend if needed, or keep {video_id}
# Based on old routes: @router.post("/{video_id}")
# Based on Frontend Analysis: summaryAPI.generateSummary calls POST /summaries/generate with body {video_id}
# Wait, let me check the frontend analysis again.
# Frontend: POST /summaries/generate body={video_id} (line 100 in APIService.js, but URL is /summaries/generate)
# Old route: prefix="/summary", route POST "/{video_id}"
# Mismatch? Frontend calls /summaries/generate. Old route was /summary.
# I need to match the Frontend. 
# Frontend uses: `${API_BASE_URL}/summaries/generate` with { video_id: videoId }
# I will change prefix to "/summaries" and add "/generate" route.

@router.post("/generate", response_model=SummaryResponse)
async def generate_summary_endpoint(payload: Dict[str, str] = Body(...)):
    """Generate comprehensive timestamped summary for a processed video"""
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
