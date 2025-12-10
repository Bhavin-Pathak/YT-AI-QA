"""Question answering routes"""
from fastapi import APIRouter, HTTPException, Body
from app.models.models import QuestionRequest, AnswerResponse, ConversationMessage
from app.services.chat_service import answer_question
from app.core.storage import conversation_sessions
from app.core.config import MAX_CONVERSATION_HISTORY

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/ask", response_model=AnswerResponse)
async def ask_question_endpoint(request: QuestionRequest):
    """Ask a question about a processed video"""
    try:
        result = answer_question(
            question=request.question,
            video_id=request.video_id,
            conversation_history=request.conversation_history
        )
        
        # Store conversation
        video_id = result["video_id"]
        if video_id not in conversation_sessions:
            conversation_sessions[video_id] = []
        
        conversation_sessions[video_id].append(ConversationMessage(role="user", content=request.question))
        conversation_sessions[video_id].append(ConversationMessage(role="assistant", content=result["answer"]))
        
        # Keep only recent messages
        if len(conversation_sessions[video_id]) > MAX_CONVERSATION_HISTORY:
            conversation_sessions[video_id] = conversation_sessions[video_id][-MAX_CONVERSATION_HISTORY:]
        
        return AnswerResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")


@router.get("/conversation/{video_id}")
async def get_conversation(video_id: str):
    """Get conversation history for a video"""
    if video_id not in conversation_sessions:
        return {"video_id": video_id, "conversation": []}
    
    return {
        "video_id": video_id,
        "conversation": conversation_sessions[video_id]
    }


@router.delete("/conversation/{video_id}")
async def clear_conversation(video_id: str):
    """Clear conversation history for a video"""
    if video_id in conversation_sessions:
        conversation_sessions[video_id] = []
        return {"message": f"Conversation cleared for video {video_id}"}
    else:
        raise HTTPException(status_code=404, detail="No conversation found for this video")
