"""Configuration management for the research agent."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    anthropic_api_key: str
    tavily_api_key: str

    # Model settings
    model_name: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 0.7

    # ChromaDB settings
    chroma_persist_directory: str = "./data/chroma"
    collection_name: str = "research_memory"

    # Agent settings
    max_iterations: int = 10
    reflection_threshold: int = 3

    # Database settings
    database_path: str = "./data/research.db"

    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = ""
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

