"""
API routes for chat operations
"""
from fastapi import APIRouter, HTTPException
from app.services.chat_service import chat_service
from app.models.chat_model import QueryRequest, QueryResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/query", response_model=QueryResponse)
async def query_documents(query: QueryRequest):
    """
    Query documents using RAG pipeline
    
    Args:
        query: QueryRequest with user question
        
    Returns:
        QueryResponse with answer and sources
    """
    try:
        result = await chat_service.process_query(query)
        return result
    except Exception as e:
        logger.error(f"Error in query endpoint: {e}", exc_info=True)
        # Return error as QueryResponse instead of HTTP error
        from datetime import datetime
        return QueryResponse(
            answer="Sorry, I encountered an error processing your question. Please make sure you have uploaded a document first, then try again.",
            sources=None,
            timestamp=datetime.utcnow()
        )


@router.get("/history")
async def get_chat_history(limit: int = 50):
    """
    Get chat history
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of chat history records
    """
    try:
        history = await chat_service.get_chat_history(limit)
        return {"history": history}
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
