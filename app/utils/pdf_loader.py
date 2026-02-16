"""
PDF document loader utility
"""
from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)


class PDFLoaderUtil:
    """Utility class for loading PDF documents"""
    
    @staticmethod
    def load_pdf(file_path: str) -> List[Document]:
        """
        Load PDF file and extract text
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of Document objects
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} pages from {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
            raise ValueError(f"Failed to load PDF: {str(e)}")
