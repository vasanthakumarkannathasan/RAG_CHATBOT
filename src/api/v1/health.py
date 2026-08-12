from fastapi import APIRouter
from src.services.database_service import get_database_info

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("")
def health():
    database = get_database_info()
    return {
        "success": True,
        "message": "Health check successful",
        "data": {
            "status": "UP",
            "database": database
        }
    }