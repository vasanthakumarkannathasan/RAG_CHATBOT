from fastapi import APIRouter
from src.models.chat.request import ChatRequest
from src.models.chat.response import ChatResponse
from src.services.chat_service import chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post(
    "",
    response_model=ChatResponse
)
def chat_api(request: ChatRequest):
    result = chat(
        question=request.question,
        source=request.source,
        session_id=request.session_id
    )
    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"]
    )

