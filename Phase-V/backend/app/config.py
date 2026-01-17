"""
Application Configuration
Manages environment variables and application settings using Pydantic BaseSettings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database Configuration
    # Note: Use postgresql:// (psycopg2) for sync operations, not postgresql+asyncpg://
    DATABASE_URL: str = "postgresql://neondb_owner:npg_iKdfhC9Iz5uN@ep-shiny-bar-adtgsazt-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

    # Authentication & Security
    BETTER_AUTH_SECRET: str = "your-secret-key-min-32-characters-long-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    # CORS Configuration
    FRONTEND_URL: str = "https://todo-frontend-app-zeta.vercel.app"
    ALLOWED_ORIGINS: str = "http://localhost:3000,https://todo-frontend-app-zeta.vercel.app,https://noorulsehar-ai-todo-app.hf.space"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Application Metadata
    APP_NAME: str = "Phase III Todo AI Assistant"
    APP_VERSION: str = "3.0.0"

    # Phase III: Gemini AI Configuration
    GEMINI_API_KEY: str  # Required: Google Gemini API key for AI agent
    GEMINI_MODEL: str = "gemini-1.5-flash"  # Model for AI agent (free tier)
    MAX_CONVERSATION_MESSAGES: int = 50  # Max messages loaded per request

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
