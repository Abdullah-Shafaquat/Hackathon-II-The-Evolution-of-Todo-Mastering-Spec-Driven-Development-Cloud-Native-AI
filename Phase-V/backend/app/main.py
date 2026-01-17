"""
FastAPI Main Application
Entry point for the Phase V Todo AI Assistant backend

T-V-07: Updated for event-driven architecture with Dapr integration
From: speckit.plan - Event-Driven Architecture
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import create_db_and_tables
from app.middleware.cors import configure_cors
from app.routes import auth_router, tasks_router, chat_router
from app.events import get_event_publisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    Creates database tables on startup (if database is available)
    Initializes event publisher for Dapr integration
    """
    # Startup: Create database tables (skip if database not available)
    try:
        logger.info("Creating database tables...")
        create_db_and_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.warning(f"Could not create database tables: {e}")
        logger.info("Server will start without database. Configure DATABASE_URL in .env")

    # T-V-07: Initialize event publisher
    try:
        publisher = get_event_publisher()
        is_healthy = await publisher.check_health()
        if is_healthy:
            logger.info("Dapr sidecar is healthy, event publishing enabled")
        else:
            logger.warning("Dapr sidecar not available, event publishing will be disabled")
    except Exception as e:
        logger.warning(f"Could not initialize event publisher: {e}")

    yield

    # Shutdown: Cleanup (if needed)
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Full-stack todo application with authentication and database persistence",
    lifespan=lifespan
)

# Configure CORS middleware
configure_cors(app)

# Register API routes
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns server status and configuration info

    T-V-07: Includes Dapr sidecar health status

    Returns:
        dict: Health status and application metadata
    """
    # Check Dapr sidecar health
    dapr_status = "not configured"
    try:
        publisher = get_event_publisher()
        if publisher.enabled:
            is_healthy = await publisher.check_health()
            dapr_status = "healthy" if is_healthy else "unhealthy"
        else:
            dapr_status = "disabled"
    except Exception:
        dapr_status = "error"

    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if settings.DATABASE_URL else "not configured",
        "dapr": dapr_status
    }


@app.get("/")
async def root():
    """
    Root endpoint
    Returns API information
    """
    return {
        "message": "Phase V Todo AI Assistant API",
        "version": settings.APP_VERSION,
        "phase": "V - Event-Driven Architecture",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "auth": "/api/auth (signup, login)",
            "tasks": "/api/tasks (CRUD operations with event publishing)",
            "chat": "/api/{user_id}/chat (AI assistant)"
        }
    }
