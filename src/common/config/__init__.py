
"""
Common configuration module for AI Backlog Assistant
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # General settings
    APP_NAME: str = "AI Backlog Assistant"
    VERSION: str = "2.0.0"

    # Paths
    DATA_PATH: str = "data"
    LOGS_PATH: str = "logs"

    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database settings
    WEAVIATE_URL: str = "http://localhost:8080"
    POSTGRES_URL: str = "postgresql://user:password@localhost:5432/ai_backlog"
    DATABASE_URL: str = "sqlite:///./instance/site.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM settings
    OPENAI_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    WHISPER_MODEL: str = "base"
    EMBEDDING_MODEL_NAME: str = "intfloat/multilingual-e5-small"

    # Security settings
    SECRET_KEY: str = "your-very-secret-key-here-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

# Create settings instance
settings = Settings()
