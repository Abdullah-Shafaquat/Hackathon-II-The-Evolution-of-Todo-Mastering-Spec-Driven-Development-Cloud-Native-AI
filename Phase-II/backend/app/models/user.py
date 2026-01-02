"""
User Model
Represents authenticated users in the system managed by Better Auth
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    """User model managed by Better Auth.

    This model represents authenticated users in the system.
    Better Auth handles creation, password hashing, and validation.
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # Better Auth UUID as string
    email: str = Field(unique=True, index=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=100)
    password_hash: str = Field(exclude=True)  # Never serialized
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config for SQLModel."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }
