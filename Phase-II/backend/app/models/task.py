"""
Task Model
Represents todo items belonging to users
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Task(SQLModel, table=True):
    """Task model for todo items.

    Each task belongs to exactly one user (user_id foreign key).
    All queries MUST filter by user_id to ensure data isolation.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment
    user_id: str = Field(foreign_key="users.id", index=True)   # FK to users
    title: str = Field(min_length=1, max_length=200)           # Required, 1-200 chars
    description: Optional[str] = Field(default=None)           # Optional text
    completed: bool = Field(default=False)                     # Default pending
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config for SQLModel."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }
