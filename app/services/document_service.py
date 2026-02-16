"""
Document processing service
"""
from fastapi import UploadFile
from typing import Dict
import os
import shutil
from datetime import datetime
from app.core.config import settings
from app.core.database import mongodb
from app.core.vector_store import vector_store_manager
from app.utils.pdf_loader import PDFLoaderUtil
from app.utils.text_splitter import text_splitter
from app.models.document_model import DocumentMetadata, DocumentUploadResponse
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for handling document operations"""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self._ensure_upload_directory()
        self.pdf_loader = PDFLoaderUtil()
    
    def _ensure_upload_directory(self):
        """Ensure upload directory exists"""
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def process_document(self, file: UploadFile) -> DocumentUploadResponse:
        """
        Process uploaded PDF document
        
        Args:
            file: Uploaded file
            
        Returns:
            DocumentUploadResponse
        """
        try:
            # Validate file type
            if not file.filename.endswith('.pdf'):
                return DocumentUploadResponse(
                    success=False,
                    message="Only PDF files are supported"
                )
            
            # Save file locally
            file_path = os.path.join(self.upload_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            file_size = os.path.getsize(file_path)
            logger.info(f"Saved file: {file.filename} ({file_size} bytes)")
            
            # Load PDF
            documents = self.pdf_loader.load_pdf(file_path)
            
            # Split into chunks
            chunks = text_splitter.split_documents(documents)
            
            # Add to vector store
            try:
                vector_store_manager.add_documents(chunks)
            except Exception as embed_error:
                error_msg = str(embed_error)
                logger.error(f"Error adding to vector store: {error_msg}")
                
                # Check for specific OpenAI errors
                if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg:
                    return DocumentUploadResponse(
                        success=False,
                        message="OpenAI API quota exceeded. Please add credits to your OpenAI account at https://platform.openai.com/settings/organization/billing"
                    )
                elif "rate_limit" in error_msg:
                    return DocumentUploadResponse(
                        success=False,
                        message="OpenAI API rate limit reached. Please wait a moment and try again."
                    )
                else:
                    return DocumentUploadResponse(
                        success=False,
                        message=f"Error processing document embeddings: {error_msg}"
                    )
            
            # Store metadata in MongoDB
            metadata = DocumentMetadata(
                filename=file.filename,
                file_path=file_path,
                file_size=file_size,
                num_chunks=len(chunks),
                status="processed"
            )
            
            collection = mongodb.get_collection("documents")
            document_id = None
            if collection is not None:
                result = await collection.insert_one(metadata.dict())
                document_id = str(result.inserted_id)
            else:
                logger.warning("MongoDB not available. Document metadata not stored.")
            
            logger.info(f"Document processed successfully: {file.filename}")
            
            return DocumentUploadResponse(
                success=True,
                message="Document uploaded and processed successfully",
                document_id=document_id,
                filename=file.filename,
                num_chunks=len(chunks)
            )
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return DocumentUploadResponse(
                success=False,
                message=f"Error processing document: {str(e)}"
            )
    
    async def get_all_documents(self):
        """Get all documents from MongoDB"""
        try:
            collection = mongodb.get_collection("documents")
            if collection is None:
                logger.warning("MongoDB not available. Returning empty document list.")
                return []
            documents = []
            async for doc in collection.find():
                doc["id"] = str(doc["_id"])
                del doc["_id"]
                documents.append(doc)
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    async def delete_document(self, document_id: str):
        """Delete document by ID"""
        try:
            from bson import ObjectId
            collection = mongodb.get_collection("documents")
            result = await collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise


# Global document service instance
document_service = DocumentService()
