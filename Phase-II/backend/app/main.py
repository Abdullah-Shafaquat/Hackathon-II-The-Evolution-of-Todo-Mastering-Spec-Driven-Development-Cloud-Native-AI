"""
FastAPI Main Application
Entry point for the Phase II Todo App backend
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.database import create_db_and_tables
from app.middleware.cors import configure_cors
from app.routes import auth_router, tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    Creates database tables on startup (if database is available)
    """
    # Startup: Create database tables (skip if database not available)
    try:
        print("Creating database tables...")
        create_db_and_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        print("Server will start without database. Configure DATABASE_URL in .env")

    yield

    # Shutdown: Cleanup (if needed)
    print("Shutting down application...")


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


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns server status and configuration info

    Returns:
        dict: Health status and application metadata
    """
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if settings.DATABASE_URL else "not configured"
    }


@app.get("/")
async def root():
    """
    Root endpoint
    Returns API information
    """
    return {
        "message": "Phase II Todo App API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "auth": "/api/auth (signup, login)",
            "tasks": "/api/tasks (CRUD operations)"
        }
    }
