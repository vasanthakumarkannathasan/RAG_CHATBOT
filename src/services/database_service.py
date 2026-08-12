from langchain_chroma import Chroma
from src.services.embedding import get_embedding_model
from src.config.settings import (
    COLLECTION_NAME,
    VECTOR_DB_PATH,
)


def get_vector_db():
    embeddings = get_embedding_model()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTOR_DB_PATH,
    )

def get_database_info():
    vector_db = get_vector_db()
    collection = vector_db._collection
    count = collection.count()
    return {
        "collection": COLLECTION_NAME,
        "documents": count
    }

import shutil
from pathlib import Path


def reset_database():
    db_path = Path(VECTOR_DB_PATH)
    if db_path.exists():
        shutil.rmtree(db_path)
        return True
    return False