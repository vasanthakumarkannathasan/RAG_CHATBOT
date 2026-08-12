from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
import src.config.settings as settings
from src.exceptions.embedding_exception import (EmbeddingException, )
from src.utils.logger import logger
from src.utils.performance import measure_performance

@lru_cache(maxsize=1)
@measure_performance("Embedding Model Loading")
def get_embedding_model():
    try:
        return HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )

    except Exception as ex:
        logger.exception(f"Unable to load embedding model: {ex}")
        raise EmbeddingException(f"Failed to load embedding model: {ex}") from ex