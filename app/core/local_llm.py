"""
Local LLM alternative (FREE, no API key needed)
Uses extractive QA approach
"""
from typing import List
import logging

logger = logging.getLogger(__name__)


class LocalLLM:
    """Simple extractive QA without external API"""
    
    def __init__(self):
        self.name = "Local Extractive QA"
    
    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer using simple extractive approach
        For production, you can integrate Ollama or other local LLMs
        """
        if not context or context.strip() == "":
            return "I don't have any document content to answer your question. Please upload a PDF document first."
        
        # Simple extractive answer - find most relevant sentences
        sentences = [s.strip() for s in context.split('.') if s.strip()]
        
        if not sentences:
            return "I found the document but couldn't extract meaningful content. The document might be empty or image-based."
        
        # Return the most relevant context (first few sentences as answer)
        # In a real system, you'd use a proper extractive QA model
        num_sentences = min(3, len(sentences))
        answer = '. '.join(sentences[:num_sentences]) + '.'
        
        return f"Based on the uploaded documents:\n\n{answer}\n\n(Note: Using local processing. For better answers, add OpenAI API key or use Ollama.)"
    
    def invoke(self, text: str) -> str:
        """LangChain-compatible invoke method"""
        return text  # For LCEL compatibility
