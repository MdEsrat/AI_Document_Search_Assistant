"""
OpenAI Embeddings configuration
"""
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings


def get_embeddings() -> OpenAIEmbeddings:
    """Get OpenAI embeddings instance"""
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=settings.OPENAI_API_KEY
    )
