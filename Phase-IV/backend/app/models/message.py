"""
Message Model
Represents individual chat messages in conversations
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


class Message(SQLModel, table=True):
    """Message model for chat messages.

    Each message belongs to a conversation and has a role (user or assistant).
    user_id is denormalized for efficient filtering and cascade deletion.
    All queries MUST filter by user_id to ensure data isolation.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)  # Auto-increment
    user_id: str = Field(foreign_key="users.id", index=True)  # FK to users (denormalized)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", index=True)  # FK to conversations
    role: str = Field(max_length=50)  # Message sender: "user" or "assistant"
    content: str = Field(min_length=1, max_length=50000)  # Message text (max ~50K chars)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        """Pydantic config for SQLModel."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "conversation_id": "660f9511-f3ac-52e5-b827-557766551111",
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2026-01-04T10:30:00Z"
            }
        }
