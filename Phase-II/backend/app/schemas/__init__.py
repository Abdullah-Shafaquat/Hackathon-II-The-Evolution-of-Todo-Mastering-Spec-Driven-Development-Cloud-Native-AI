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
]
