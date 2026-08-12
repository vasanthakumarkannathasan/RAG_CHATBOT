from langchain_core.documents import Document
from src.services.database import get_vector_db
from src.exceptions.database_exception import DatabaseException
from src.utils.logger import logger
from src.utils.performance import measure_performance


@measure_performance("Document Retrieval")
def retrieve_documents(
    question: str,
    k: int = 2, 
    source: str | None = None
):
    try:
        vector_db = get_vector_db()
        search_kwargs = {
            "k": k
        }
        if source:
            # Filter by exact filename match
            search_kwargs["filter"] = {
                "source": source
            }
        retriever = vector_db.as_retriever(
            search_kwargs=search_kwargs
        )        
        return retriever.invoke(question)
    except Exception as ex:
        logger.exception(f"Failed to retrieve documents for question: {question}")
        raise DatabaseException(f"Failed to retrieve documents: {ex}") from ex