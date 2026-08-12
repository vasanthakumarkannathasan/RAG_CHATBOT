from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import os
from src.config.settings import PDF_DIRECTORY
from src.services.database import get_indexed_documents, delete_document_by_source, sync_database_with_files
from src.services.indexing import index_directory
from src.utils.logger import logger

router = APIRouter()

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to the data folder.
    Supported formats: PDF (.pdf), Word (.docx, .doc), PowerPoint (.pptx, .ppt)
    The document will not be indexed automatically.
    """
    try:
        # Validate file type
        supported_extensions = ['.pdf', '.docx', '.doc', '.pptx', '.ppt']
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in supported_extensions:
            return {
                "success": False,
                "message": f"Unsupported file format. Supported formats: {', '.join(supported_extensions)}",
                "data": {}
            }
        
        # Save file to data directory
        file_path = PDF_DIRECTORY / file.filename
        
        # Check if file already exists
        if file_path.exists():
            return {
                "success": False,
                "message": f"File '{file.filename}' already exists",
                "data": {}
            }
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Uploaded file: {file.filename}")
        
        return {
            "success": True,
            "message": f"File '{file.filename}' uploaded successfully",
            "data": {
                "filename": file.filename,
                "uploaded": True
            }
        }
    
    except Exception as ex:
        logger.exception(f"Failed to upload file: {ex}")
        return {
            "success": False,
            "message": f"Failed to upload file: {str(ex)}",
            "data": {}
        }

@router.post("/documents/upload-and-index")
async def upload_and_index_document(file: UploadFile = File(...)):
    """
    Upload a document and immediately index it.
    Supported formats: PDF (.pdf), Word (.docx, .doc), PowerPoint (.pptx, .ppt)
    This combines upload + indexing in one step.
    """
    try:
        # Validate file type
        supported_extensions = ['.pdf', '.docx', '.doc', '.pptx', '.ppt']
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in supported_extensions:
            return {
                "success": False,
                "message": f"Unsupported file format. Supported formats: {', '.join(supported_extensions)}",
                "data": {}
            }
        
        # Save file to data directory
        file_path = PDF_DIRECTORY / file.filename
        
        # Save uploaded file (overwrite if exists - will skip duplicates during indexing)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Uploaded file: {file.filename}")
        
        # Index the directory (will skip duplicate chunks)
        index_result = index_directory()
        
        logger.info(f"Indexed file: {file.filename} - {index_result}")
        
        return {
            "success": True,
            "message": f"File '{file.filename}' uploaded and indexed successfully",
            "data": {
                "filename": file.filename,
                "uploaded": True,
                "indexed": True,
                "chunks_added": index_result.get('chunk_count', 0),
                "duplicates_skipped": index_result.get('skipped_duplicates', 0)
            }
        }
    
    except Exception as ex:
        logger.exception(f"Failed to upload and index file: {ex}")
        return {
            "success": False,
            "message": f"Failed to upload and index file: {str(ex)}",
            "data": {}
        }

@router.get("/documents/list")
def list_indexed_documents():
    """
    Get list of all indexed documents with their statistics.
    Shows filename, chunk count, and page count for each document.
    """
    try:
        documents = get_indexed_documents()
        
        return {
            "success": True,
            "message": "Indexed documents retrieved successfully",
            "data": {
                "documents": documents,
                "total_files": len(documents)
            }
        }
    
    except Exception as ex:
        logger.exception(f"Failed to list indexed documents: {ex}")
        return {
            "success": False,
            "message": f"Failed to list indexed documents: {str(ex)}",
            "data": {}
        }


@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """
    Delete a document from both the data folder and vector database.
    This removes the file and all its embeddings.
    """
    try:
        file_path = PDF_DIRECTORY / filename
        
        # Check if file exists
        if not file_path.exists():
            # File doesn't exist, but try to clean up embeddings anyway
            logger.warning(f"File not found in data folder: {filename}, attempting to clean up embeddings")
        else:
            # Delete the physical file
            os.remove(file_path)
            logger.info(f"Deleted file from data folder: {filename}")
        
        # Delete embeddings from vector database
        chunks_deleted = delete_document_by_source(filename)
        
        return {
            "success": True,
            "message": f"Document '{filename}' deleted successfully",
            "data": {
                "filename": filename,
                "file_deleted": file_path.exists() == False,
                "chunks_deleted": chunks_deleted
            }
        }
    
    except Exception as ex:
        logger.exception(f"Failed to delete document '{filename}': {ex}")
        return {
            "success": False,
            "message": f"Failed to delete document '{filename}': {str(ex)}",
            "data": {}
        }


@router.post("/documents/sync")
async def sync_documents():
    """
    Sync the vector database with the data folder.
    Removes embeddings for documents that no longer exist in the data folder.
    Call this after manually deleting files from the data folder.
    """
    try:
        sync_result = sync_database_with_files()
        
        if sync_result['orphaned_documents'] > 0:
            message = f"Sync completed: Removed {sync_result['orphaned_documents']} orphaned documents ({sync_result['chunks_deleted']} chunks)"
        else:
            message = "Sync completed: Database is already in sync with data folder"
        
        return {
            "success": True,
            "message": message,
            "data": sync_result
        }
    
    except Exception as ex:
        logger.exception(f"Failed to sync documents: {ex}")
        return {
            "success": False,
            "message": f"Failed to sync documents: {str(ex)}",
            "data": {}
        }
