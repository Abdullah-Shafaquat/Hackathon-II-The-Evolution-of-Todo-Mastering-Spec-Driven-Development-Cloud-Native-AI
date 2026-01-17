"""
Task Schemas
Pydantic models for task API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    due_date: Optional[date] = Field(None, description="Task due date")
    priority: Optional[str] = Field("medium", description="Priority: low, medium, high")
    category: Optional[str] = Field("other", description="Category: personal, work, study, health, shopping, other")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "due_date": "2026-01-15",
                "priority": "high",
                "category": "personal"
            }
        }


class TaskUpdate(BaseModel):
    """Request schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None)
    completed: Optional[bool] = Field(None)
    status: Optional[str] = Field(None, description="Status: pending, in_progress, completed")
    due_date: Optional[date] = Field(None, description="Task due date")
    priority: Optional[str] = Field(None, description="Priority: low, medium, high")
    category: Optional[str] = Field(None, description="Category: personal, work, study, health, shopping, other")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and fruits",
                "description": "Milk, eggs, bread, apples",
                "completed": False,
                "status": "in_progress",
                "due_date": "2026-01-20",
                "priority": "medium",
                "category": "personal"
            }
        }


class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    status: str
    due_date: Optional[date]
    priority: str
    category: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow validation from SQLModel objects
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "status": "pending",
                "due_date": "2026-01-15",
                "priority": "high",
                "category": "personal",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }


class TaskListResponse(BaseModel):
    """Response schema for task list with metadata."""
    tasks: list[TaskResponse]
    total: int
    completed: int
    pending: int

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "user_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "completed": False,
                        "status": "pending",
                        "due_date": "2026-01-15",
                        "priority": "high",
                        "category": "personal",
                        "created_at": "2025-12-30T10:00:00Z",
                        "updated_at": "2025-12-30T10:00:00Z"
                    }
                ],
                "total": 5,
                "completed": 2,
                "pending": 3
            }
        }
