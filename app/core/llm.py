"""
OpenAI LLM configuration
"""
from langchain_openai import ChatOpenAI
from app.core.config import settings


def get_llm() -> ChatOpenAI:
    """Get OpenAI LLM instance"""
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=settings.TEMPERATURE,
        openai_api_key=settings.OPENAI_API_KEY
    )
