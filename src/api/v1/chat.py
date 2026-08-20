"""Chat API endpoints for Enterprise RAG"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.services.chat_service import chat
from src.services.memory import ConversationMemory
from src.exceptions.base_exception import EnterpriseRAGException
from src.utils.logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory storage for conversation sessions (for demo purposes)
# In production, use Redis or a database
conversation_sessions = {}


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str
    session_id: Optional[str] = None
    source: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    success: bool
    message: str
    data: dict


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process a chat question and return an answer.
    
    Args:
        request: ChatRequest containing question, session_id, source filter, and stream flag
    
    Returns:
        ChatResponse with answer, session_id, and sources
    """
    try:
        # Get or create conversation memory for this session
        session_id = request.session_id or "default"
        
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = ConversationMemory()
        
        memory = conversation_sessions[session_id]
        
        # Add user message to memory
        memory.add_user_message(request.question)
        
        # Get conversation history for context
        conversation_history = memory.get_messages()
        
        # Get chat response with new dict format
        result = chat(
            question=request.question,
            source=request.source,
            session_id=session_id,
            conversation_history=conversation_history
        )
        
        # Add assistant response to memory
        memory.add_assistant_message(result["answer"])
        
        # Format sources for response
        sources = [
            f"{src['document']} (Page {src['page']})"
            for src in result["sources"]
        ]
        
        return ChatResponse(
            success=True,
            message="Chat response generated successfully",
            data={
                "answer": result["answer"],
                "session_id": session_id,
                "sources": sources
            }
        )
    
    except EnterpriseRAGException as ex:
        logger.error(f"Chat error: {ex}")
        raise HTTPException(status_code=500, detail=str(ex))
    
    except Exception as ex:
        logger.exception(f"Unexpected error: {ex}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """
    Clear conversation memory for a specific session.
    
    Args:
        session_id: The session ID to clear
    
    Returns:
        Success message
    """
    if session_id in conversation_sessions:
        conversation_sessions[session_id].clear()
        return {
            "success": True,
            "message": f"Session {session_id} cleared successfully",
            "data": {
                "session_id": session_id,
                "cleared": True
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")


@router.get("/sessions")
async def list_sessions():
    """
    List all active conversation sessions.
    
    Returns:
        List of session IDs and their message counts
    """
    sessions = {}
    for session_id, memory in conversation_sessions.items():
        sessions[session_id] = {
            "message_count": memory.get_message_count(),
            "is_empty": memory.is_empty()
        }
    return {
        "success": True,
        "message": "Sessions retrieved successfully",
        "data": {
            "sessions": sessions,
            "total_sessions": len(sessions)
        }
    }
