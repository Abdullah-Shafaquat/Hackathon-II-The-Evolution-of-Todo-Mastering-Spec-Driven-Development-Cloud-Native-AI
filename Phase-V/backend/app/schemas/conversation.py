"""
Conversation Schemas
Pydantic schemas for conversation API request/response
"""

from pydantic import BaseModel
from datetime import datetime
import uuid


class ConversationResponse(BaseModel):
    """Schema for conversation response.

    Used for API responses when returning conversation metadata.
    Does not include messages - use separate endpoints to load conversation history.
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows SQLModel -> Pydantic conversion
