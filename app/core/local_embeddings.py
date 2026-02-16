"""
Local embeddings using HuggingFace models (FREE, no API key needed)
"""
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def get_local_embeddings() -> HuggingFaceEmbeddings:
    """
    Get HuggingFace embeddings (runs locally, completely free)
    Model: sentence-transformers/all-MiniLM-L6-v2
    """
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.LOCAL_EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if you have GPU
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.info(f"Local embeddings loaded: {settings.LOCAL_EMBEDDING_MODEL}")
        return embeddings
    except Exception as e:
        logger.error(f"Error loading local embeddings: {e}")
        raise
