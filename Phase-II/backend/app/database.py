"""
Database Connection and Session Management
Handles SQLModel engine creation, session management, and database initialization
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from app.config import settings


# Create database engine with connection pooling
# Note: Use postgresql:// (psycopg2) not postgresql+asyncpg:// for sync operations
# SQLite doesn't support connection pooling parameters
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        echo=True,  # Log SQL queries (disable in production)
        connect_args={"check_same_thread": False}  # Required for SQLite
    )
else:
    # PostgreSQL with connection pooling
    engine = create_engine(
        settings.DATABASE_URL,
        echo=True,  # Log SQL queries (disable in production)
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,  # Recycle connections after 1 hour
    )


def create_db_and_tables():
    """
    Create all database tables defined by SQLModel models
    Called on application startup
    """
    # Import models to register them with SQLModel metadata
    from app.models import User, Task  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get database session
    Automatically handles session creation and cleanup

    Usage:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session
