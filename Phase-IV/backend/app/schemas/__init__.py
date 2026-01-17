"""
Schemas Package
Exports all Pydantic schemas for API contracts
"""

from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    AuthResponse,
    UserResponse
)

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse
)

from app.schemas.conversation import (
    ConversationResponse
)

from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    ChatResponse
)

__all__ = [
    # Auth schemas
    "SignupRequest",
    "LoginRequest",
    "AuthResponse",
    "UserResponse",
    # Task schemas
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskListResponse",
    # Conversation schemas
    "ConversationResponse",
    # Message schemas
    "MessageCreate",
    "MessageResponse",
    "ChatResponse",
]
