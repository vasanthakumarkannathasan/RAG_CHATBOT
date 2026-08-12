from fastapi import APIRouter
from src.services.database_service import get_database_info
from src.services.database_service import reset_database

router = APIRouter(
    prefix="/database",
    tags=["Database"]
)

@router.get("")
def database_info():
    info = get_database_info()
    return {
        "success": True,
        "message": "Database info retrieved successfully",
        "data": info
    }

@router.delete("")
def clear_database():
    success = reset_database()
    return {
        "success": success,
        "message": "Database cleared successfully" if success else "Database not found",
        "data": {
            "cleared": success
        }
    }