import src.config.settings as settings
from src.services.loader import load_document
from src.services.chunking import split_documents
from src.services.database import get_vector_db, get_existing_hashes, sync_database_with_files
from src.exceptions.database_exception import DatabaseException
from src.utils.logger import logger
from src.utils.performance import measure_performance

@measure_performance("Directory Indexing")
def index_directory():
    try:
        # First, sync database with data folder (remove orphaned embeddings)
        logger.info("Syncing database with data folder...")
        sync_result = sync_database_with_files()
        if sync_result['orphaned_documents'] > 0:
            logger.info(f"Cleaned up {sync_result['orphaned_documents']} orphaned documents ({sync_result['chunks_deleted']} chunks)")
        
        # Support multiple document formats
        supported_extensions = ['*.pdf', '*.docx', '*.doc', '*.pptx', '*.ppt']
        doc_files = []
        for ext in supported_extensions:
            doc_files.extend(settings.PDF_DIRECTORY.glob(ext))
        vector_db = get_vector_db()
        
        # Get existing hashes for deduplication
        existing_hashes = get_existing_hashes()
        logger.info(f"Found {len(existing_hashes)} existing chunks in database")

        total_documents = 0
        total_chunks = 0
        total_skipped = 0

        for doc_file in doc_files:
            documents = load_document(doc_file.name)
            chunks = split_documents(documents)
            
            # Filter out duplicate chunks based on hash
            new_chunks = []
            for chunk in chunks:
                chunk_hash = chunk.metadata.get('chunk_hash')
                if chunk_hash and chunk_hash not in existing_hashes:
                    new_chunks.append(chunk)
                    existing_hashes.add(chunk_hash)  # Add to set to avoid duplicates within same batch
                else:
                    total_skipped += 1
            
            # Only add new chunks
            if new_chunks:
                vector_db.add_documents(new_chunks)
                logger.info(f"Added {len(new_chunks)} new chunks from {doc_file.name} (skipped {len(chunks) - len(new_chunks)} duplicates)")
            else:
                logger.info(f"Skipped {doc_file.name} - all chunks already exist")
            
            total_documents += len(documents)
            total_chunks += len(new_chunks)

        return {
            "file_count": len(doc_files),
            "document_count": total_documents,
            "chunk_count": total_chunks,
            "skipped_duplicates": total_skipped,
            "orphaned_cleaned": sync_result['orphaned_documents']
        }
    except Exception as ex:
        logger.exception(f"Failed to index directory: {ex}")
        raise DatabaseException(f"Failed to index directory: {ex}") from ex