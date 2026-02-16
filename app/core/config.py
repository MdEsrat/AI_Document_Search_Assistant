"""
Configuration management using environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration (Optional)
    OPENAI_API_KEY: str = ""
    
    # MongoDB Configuration
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "document_search_db"
    
    # Application Configuration
    UPLOAD_DIR: str = "data/uploads"
    CHROMA_DIR: str = "data/chroma"
    
    # LangChain Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Model Configuration
    USE_LOCAL_MODELS: bool = True  # Set to False to use OpenAI
    
    # Local Model Configuration (Free, no API key needed)
    LOCAL_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # OpenAI Model Configuration (Only if USE_LOCAL_MODELS = False)
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.0
    
    # API Configuration
    API_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
