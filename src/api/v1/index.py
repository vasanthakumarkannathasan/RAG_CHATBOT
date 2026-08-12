from fastapi import APIRouter
from src.services.indexing import index_directory

router = APIRouter(
    prefix="/index",
    tags=["Index"]
)

@router.post("")
def index_documents():
    index_directory()
    return {
        "success": True,
        "message": "Documents indexed successfully",
        "data": {
            "indexed": True
        }
    }