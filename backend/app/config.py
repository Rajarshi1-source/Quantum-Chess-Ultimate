"""
Quantum Chess Ultimate - Configuration Management
Uses pydantic-settings for environment variable management.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
import sys


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    DATABASE_URL: str # No default - required env var
    
    @field_validator("DATABASE_URL")
    @classmethod
    def database_url_must_be_set(cls, v: str) -> str:
        if not v or "YOUR_PASSWORD_HERE" in v:
            print("ERROR: DATABASE_URL is not configured.  Copy .env.example to .env")
            sys.exit(1)
        return v

    # Quantum Engine
    QUANTUM_SHOTS: int = 1000
    MAX_SEARCH_DEPTH: int = 4
    DEFAULT_SUPERPOSITION_PROB: float = 0.5

    # Logging
    LOG_LEVEL: str = "info"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
