from src.exceptions.base_exception import EnterpriseRAGException

class DatabaseException(EnterpriseRAGException):
    """Raised for ChromaDB related errors."""
    pass