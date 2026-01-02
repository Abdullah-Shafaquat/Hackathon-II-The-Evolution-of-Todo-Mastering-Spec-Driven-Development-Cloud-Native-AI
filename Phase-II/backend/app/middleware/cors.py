"""
CORS Middleware Configuration
Handles Cross-Origin Resource Sharing for frontend-backend communication
"""

from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def configure_cors(app):
    """
    Configure CORS middleware for the FastAPI application

    Allows requests from the frontend URL with credentials (cookies, auth headers)
    Required for JWT token-based authentication across different origins

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],  # Specific frontend URL
        allow_credentials=True,  # Allow cookies and authorization headers
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all headers
    )
