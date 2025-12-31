"""
Application Configuration
Manages environment variables and application settings using Pydantic BaseSettings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/todo_db"

    # Authentication & Security
    BETTER_AUTH_SECRET: str = "your-secret-key-min-32-characters-long-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    # CORS Configuration
    FRONTEND_URL: str = "http://localhost:3000"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Application Metadata
    APP_NAME: str = "Phase II Todo App"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
