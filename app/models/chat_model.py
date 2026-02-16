"""
Chat data models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QueryRequest(BaseModel):
    """Query request model"""
    question: str = Field(..., min_length=1, description="User question")
    

class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    sources: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistory(BaseModel):
    """Chat history model for MongoDB"""
    question: str
    answer: str
    sources: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None


class ChatHistoryResponse(BaseModel):
    """Chat history response model"""
    id: str
    question: str
    answer: str
    timestamp: datetime
