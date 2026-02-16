"""
ChromaDB vector store initialization and management
"""
from langchain_chroma import Chroma
from app.core.config import settings
import os
import logging

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manage ChromaDB vector store operations"""
    
    def __init__(self):
        self.persist_directory = settings.CHROMA_DIR
        
        # Use local embeddings (FREE) or OpenAI embeddings
        if settings.USE_LOCAL_MODELS or not settings.OPENAI_API_KEY:
            from app.core.local_embeddings import get_local_embeddings
            self.embeddings = get_local_embeddings()
            logger.info("Using FREE local embeddings (no API key needed)")
        else:
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                openai_api_key=settings.OPENAI_API_KEY
            )
            logger.info("Using OpenAI embeddings")
        
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure ChromaDB directory exists"""
        os.makedirs(self.persist_directory, exist_ok=True)
    
    def get_vector_store(self, collection_name: str = "documents") -> Chroma:
        """Get or create a vector store"""
        try:
            vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            logger.info(f"Vector store initialized: {collection_name}")
            return vector_store
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, documents, collection_name: str = "documents"):
        """Add documents to vector store"""
        try:
            vector_store = self.get_vector_store(collection_name)
            vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to vector store")
            return vector_store
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise


# Global vector store manager instance
vector_store_manager = VectorStoreManager()
