"""
Message Schemas
Pydantic schemas for chat message and chat API request/response
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid


class MessageCreate(BaseModel):
    """Schema for sending a chat message.

    Used for POST /api/{user_id}/chat requests.
    conversation_id is optional - if not provided, a new conversation is created.
    """
    conversation_id: Optional[uuid.UUID] = Field(
        None,
        description="Existing conversation ID (optional, creates new if not provided)"
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User message text (1-5000 characters)"
    )


class MessageResponse(BaseModel):
    """Schema for individual message in conversation history.

    Used when returning message history or individual messages.
    """
    id: int
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows SQLModel -> Pydantic conversion


class ChatResponse(BaseModel):
    """Schema for chat API response.

    Returned by POST /api/{user_id}/chat endpoint.
    Contains the AI's response, conversation ID, and any tool calls made.
    """
    conversation_id: uuid.UUID
    response: str  # AI-generated natural language response
    tool_calls: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of MCP tools invoked by AI agent"
    )
    created_at: datetime
