from langchain_chroma import Chroma
from src.services.embedding import get_embedding_model
from src.config.settings import (
    COLLECTION_NAME,
    VECTOR_DB_PATH,
)
from src.utils.logger import logger
import shutil
from pathlib import Path


def get_vector_db():
    """Get or initialize vector database connection"""
    try:
        logger.info(f"Initializing vector database: {COLLECTION_NAME}")
        embeddings = get_embedding_model()
        db = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=VECTOR_DB_PATH,
        )
        logger.info("Vector database initialized successfully")
        return db
    except Exception as ex:
        logger.exception(f"Failed to initialize vector database: {ex}")
        raise

def get_database_info():
    """Get database information including collection name and document count"""
    try:
        logger.info("Retrieving database information")
        vector_db = get_vector_db()
        collection = vector_db._collection
        count = collection.count()
        
        logger.info(f"Database info: Collection={COLLECTION_NAME}, Documents={count}")
        
        return {
            "collection": COLLECTION_NAME,
            "documents": count
        }
    except Exception as ex:
        logger.exception(f"Failed to get database info: {ex}")
        raise


def reset_database():
    """Reset database by removing all data"""
    try:
        db_path = Path(VECTOR_DB_PATH)
        
        if db_path.exists():
            logger.warning(f"Resetting database at: {db_path}")
            shutil.rmtree(db_path)
            logger.info("Database reset completed successfully")
            return True
        else:
            logger.warning(f"Database path does not exist: {db_path}")
            return False
            
    except Exception as ex:
        logger.exception(f"Failed to reset database: {ex}")
        raise