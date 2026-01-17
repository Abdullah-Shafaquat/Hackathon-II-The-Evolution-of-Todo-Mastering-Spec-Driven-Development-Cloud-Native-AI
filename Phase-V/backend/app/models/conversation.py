"""
Conversation Model
Represents chat sessions between users and AI assistant
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions.

    Each conversation belongs to exactly one user (user_id foreign key).
    All queries MUST filter by user_id to ensure data isolation.
    Stores conversation metadata; actual messages are in messages table.
    """
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # FK to users
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        """Pydantic config for SQLModel."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "660f9511-f3ac-52e5-b827-557766551111",
                "created_at": "2026-01-04T10:00:00Z",
                "updated_at": "2026-01-04T10:30:00Z"
            }
        }
