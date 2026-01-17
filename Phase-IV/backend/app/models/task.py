"""
Task Model
Represents todo items belonging to users
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCategory(str, Enum):
    """Task categories"""
    PERSONAL = "personal"
    WORK = "work"
    STUDY = "study"
    HEALTH = "health"
    SHOPPING = "shopping"
    OTHER = "other"


class TaskStatus(str, Enum):
    """Task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


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
    completed: bool = Field(default=False)                     # Default pending (kept for backward compatibility)
    status: str = Field(default="pending")                     # Task status: pending, in_progress, completed
    due_date: Optional[date] = Field(default=None)             # Optional due date
    priority: str = Field(default="medium")                    # Priority: low, medium, high
    category: str = Field(default="other")                     # Category: personal, work, study, etc.
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
                "status": "pending",
                "due_date": "2026-01-10",
                "priority": "high",
                "category": "shopping",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }
