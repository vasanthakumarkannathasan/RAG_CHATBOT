from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.exceptions.pdf_exception import PDFException
from src.utils.logger import logger
from src.utils.performance import measure_performance
import hashlib

def generate_chunk_hash(content: str, source: str, page: int = 0) -> str:
    """
    Generate SHA256 hash for a chunk to enable deduplication.
    Combines content, source, and page for unique identification.
    """
    hash_input = f"{content}|{source}|{page}".encode('utf-8')
    return hashlib.sha256(hash_input).hexdigest()

@measure_performance("Document Chunking")
def split_documents(
        documents: list[Document],
        chunk_size: int = 500,
        chunk_overlap: int = 100
) -> list[Document]:
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        chunks = text_splitter.split_documents(documents)
        
        # Add SHA256 hash to each chunk for deduplication
        for chunk in chunks:
            source = chunk.metadata.get('source', 'unknown')
            page = chunk.metadata.get('page', 0)
            chunk_hash = generate_chunk_hash(chunk.page_content, source, page)
            chunk.metadata['chunk_hash'] = chunk_hash
        
        return chunks
    except Exception as ex:
        logger.exception(f"Failed to split documents into chunks: {ex}")
        raise PDFException(f"Failed to split documents: {ex}") from ex