from functools import lru_cache

import chromadb
from langchain_chroma import Chroma

import src.config.settings as settings
from src.services.embedding import get_embedding_model

from src.exceptions.database_exception import (
    DatabaseException,
)
from src.utils.logger import logger
from src.utils.performance import measure_performance

@lru_cache(maxsize=1)
@measure_performance("ChromaDB Client Initialization")
def get_chroma_client():
    try:    
        return chromadb.PersistentClient(
            path=str(settings.VECTOR_DB_PATH)
        )
    except Exception as ex:
        logger.exception(f"Exception in get_chroma_client() in ChromaDB - {ex}")
        raise DatabaseException(f"Failed to initialize ChromaDB client: {ex}") from ex

@lru_cache(maxsize=1)
@measure_performance("Vector Database Initialization")
def get_vector_db() -> Chroma:
    try:
        return Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=get_embedding_model(),
            persist_directory=str(settings.VECTOR_DB_PATH)
        )
    except Exception as ex:
        logger.exception(f"Exception in get_vector_db() in ChromaDB - {ex}")
        raise DatabaseException(f"Failed to initialize vector database: {ex}") from ex

def list_collections():
    try:
        client = get_chroma_client()
        return [c.name for c in client.list_collections()]
    except Exception as ex:
        logger.exception(f"Exception in list_collections() in ChromaDB - {ex}")
        raise DatabaseException(f"Failed to list collections: {ex}") from ex

def delete_collections(name: str):
    try:
        client = get_chroma_client()
        client.delete_collection(name)
    except Exception as ex:
        logger.exception(f"Exception in delete_collections() in ChromaDB - {ex}")
        raise DatabaseException(f"Failed to delete collection '{name}': {ex}") from ex

def get_collection_count():
    try:
        vector_db = get_vector_db()
        return vector_db._collection.count()
    except Exception as ex:
        logger.exception(f"Exception in get_collection_count() in ChromaDB - {ex}")
        raise DatabaseException(f"Failed to get collection count: {ex}") from ex

def get_existing_hashes() -> set:
    """Get all existing chunk hashes from the database for deduplication."""
    try:
        vector_db = get_vector_db()
        collection = vector_db._collection
        
        # Get all documents with metadata
        results = collection.get(include=['metadatas'])
        
        # Extract chunk_hash from metadata
        existing_hashes = set()
        if results and 'metadatas' in results:
            for metadata in results['metadatas']:
                if metadata and 'chunk_hash' in metadata:
                    existing_hashes.add(metadata['chunk_hash'])
        
        return existing_hashes
    except Exception as ex:
        logger.exception(f"Exception in get_existing_hashes(): {ex}")
        raise DatabaseException(f"Failed to get existing hashes: {ex}") from ex

def get_indexed_documents() -> list[dict]:
    """Get list of all indexed documents with their statistics."""
    try:
        vector_db = get_vector_db()
        collection = vector_db._collection
        
        # Get all documents with metadata
        results = collection.get(include=['metadatas'])
        
        # Group by source (filename)
        documents_info = {}
        if results and 'metadatas' in results:
            for metadata in results['metadatas']:
                if metadata and 'source' in metadata:
                    source = metadata['source']
                    if source not in documents_info:
                        documents_info[source] = {
                            'filename': source,
                            'chunk_count': 0,
                            'pages': set()
                        }
                    documents_info[source]['chunk_count'] += 1
                    if 'page' in metadata:
                        documents_info[source]['pages'].add(metadata['page'])
        
        # Convert to list and format
        documents_list = []
        for doc_info in documents_info.values():
            documents_list.append({
                'filename': doc_info['filename'],
                'chunk_count': doc_info['chunk_count'],
                'page_count': len(doc_info['pages']) if doc_info['pages'] else 0
            })
        
        # Sort by filename
        documents_list.sort(key=lambda x: x['filename'])
        
        return documents_list
    except Exception as ex:
        logger.exception(f"Exception in get_indexed_documents(): {ex}")
        raise DatabaseException(f"Failed to get indexed documents: {ex}") from ex


@measure_performance("Delete Document from Vector DB")
def delete_document_by_source(filename: str) -> int:
    """Delete all chunks of a document from the vector database by source filename."""
    try:
        vector_db = get_vector_db()
        collection = vector_db._collection
        
        # Get all document IDs with matching source
        results = collection.get(
            where={"source": filename},
            include=['metadatas']
        )
        
        if results and 'ids' in results and results['ids']:
            # Delete all chunks with this source
            collection.delete(ids=results['ids'])
            deleted_count = len(results['ids'])
            logger.info(f"Deleted {deleted_count} chunks for document: {filename}")
            return deleted_count
        else:
            logger.info(f"No chunks found for document: {filename}")
            return 0
            
    except Exception as ex:
        logger.exception(f"Exception in delete_document_by_source('{filename}'): {ex}")
        raise DatabaseException(f"Failed to delete document '{filename}': {ex}") from ex


@measure_performance("Sync Vector DB with Data Folder")
def sync_database_with_files() -> dict:
    """Remove embeddings for documents that no longer exist in the data folder."""
    try:
        # Get list of indexed documents from vector DB
        indexed_docs = get_indexed_documents()
        
        # Get list of actual files in data folder
        supported_extensions = ['.pdf', '.docx', '.doc', '.pptx', '.ppt']
        actual_files = set()
        for ext in supported_extensions:
            for file_path in settings.PDF_DIRECTORY.glob(f'*{ext}'):
                actual_files.add(file_path.name)
        
        # Find orphaned documents (in DB but not in data folder)
        orphaned_docs = []
        for doc in indexed_docs:
            if doc['filename'] not in actual_files:
                orphaned_docs.append(doc['filename'])
        
        # Delete orphaned documents
        deleted_stats = []
        total_chunks_deleted = 0
        
        for filename in orphaned_docs:
            chunks_deleted = delete_document_by_source(filename)
            deleted_stats.append({
                'filename': filename,
                'chunks_deleted': chunks_deleted
            })
            total_chunks_deleted += chunks_deleted
        
        logger.info(f"Sync completed: Removed {len(orphaned_docs)} orphaned documents ({total_chunks_deleted} chunks)")
        
        return {
            'orphaned_documents': len(orphaned_docs),
            'chunks_deleted': total_chunks_deleted,
            'deleted_files': deleted_stats,
            'remaining_files': len(actual_files)
        }
        
    except Exception as ex:
        logger.exception(f"Exception in sync_database_with_files(): {ex}")
        raise DatabaseException(f"Failed to sync database with files: {ex}") from ex