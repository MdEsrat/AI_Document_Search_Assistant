"""
API routes for document operations
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.document_service import document_service
from app.models.document_model import DocumentUploadResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a PDF document
    
    Args:
        file: PDF file to upload
        
    Returns:
        DocumentUploadResponse with processing status
    """
    try:
        result = await document_service.process_document(file)
        # Return result even if not successful (with error message)
        return result
    except Exception as e:
        logger.error(f"Error in upload endpoint: {e}", exc_info=True)
        # Return error as DocumentUploadResponse instead of HTTP exception
        return DocumentUploadResponse(
            success=False,
            message=f"Upload error: {str(e)}"
        )


@router.get("/")
async def get_documents():
    """
    Get all uploaded documents
    
    Returns:
        List of documents with metadata
    """
    try:
        documents = await document_service.get_all_documents()
        return {"documents": documents}
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_document_stats():
    """
    Get statistics about uploaded documents
    
    Returns:
        Document statistics
    """
    try:
        documents = await document_service.get_all_documents()
        total_size = sum(doc.get("file_size", 0) for doc in documents)
        total_chunks = sum(doc.get("num_chunks", 0) for doc in documents)
        
        return {
            "total_documents": len(documents),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_chunks": total_chunks,
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error retrieving document stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document by ID
    
    Args:
        document_id: Document ID to delete
        
    Returns:
        Success message
    """
    try:
        success = await document_service.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
