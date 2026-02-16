"""
Document data models
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentMetadata(BaseModel):
    """Document metadata model"""
    filename: str
    file_path: str
    file_size: int
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    num_chunks: int
    status: str = "processed"


class DocumentResponse(BaseModel):
    """Document response model"""
    id: str
    filename: str
    upload_date: datetime
    num_chunks: int
    status: str
    message: str


class DocumentUploadResponse(BaseModel):
    """Upload response model"""
    success: bool
    message: str
    document_id: Optional[str] = None
    filename: Optional[str] = None
    num_chunks: Optional[int] = None
