from fastapi import APIRouter
from src.services.indexing import index_directory

router = APIRouter(
    prefix="/index",
    tags=["Index"]
)

@router.post("")
def index_documents():
    result = index_directory()
    return {
        "success": True,
        "message": "Documents indexed successfully",
        "data": result
    }