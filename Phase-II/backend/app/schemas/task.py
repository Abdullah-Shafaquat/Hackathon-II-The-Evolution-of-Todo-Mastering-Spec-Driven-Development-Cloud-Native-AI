"""
Task Schemas
Pydantic models for task API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Task description")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }


class TaskUpdate(BaseModel):
    """Request schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None)
    completed: Optional[bool] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and fruits",
                "description": "Milk, eggs, bread, apples",
                "completed": False
            }
        }


class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
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
                        "created_at": "2025-12-30T10:00:00Z",
                        "updated_at": "2025-12-30T10:00:00Z"
                    }
                ],
                "total": 5,
                "completed": 2,
                "pending": 3
            }
        }
