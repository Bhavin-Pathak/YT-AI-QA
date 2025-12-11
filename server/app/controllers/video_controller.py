"""Video processing routes"""
from fastapi import APIRouter, HTTPException
from app.models.models import VideoRequest, VideoResponse
from app.services.video_service import process_video
from app.core.storage import vector_stores, video_info

# Router configuration
router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/process", response_model=VideoResponse)
async def process_video_endpoint(request: VideoRequest):
    """
    Process a YouTube video and create vector store.
    
    Args:
        request: VideoRequest object containing the YouTube URL.
        
    Returns:
        VideoResponse: Details of the processed video including processing stats.
    """
    try:
        result = process_video(request.video_url)
        return VideoResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/list")
async def get_processed_videos():
    """
    Get list of all currently processed videos in memory.
    
    Returns:
        dict: List of video objects.
    """
    return {
        "videos": [
            {
                "video_id": vid,
                "info": info,
                "processed": True
            }
            for vid, info in video_info.items()
        ]
    }


@router.delete("/{video_id}")
async def delete_video(video_id: str):
    """Delete a processed video from memory"""
    if video_id in vector_stores:
        del vector_stores[video_id]
        del video_info[video_id]
        return {"message": f"Video {video_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Video not found")
