"""Task data model and validation"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# Custom Exceptions (T005)
class ValidationError(Exception):
    """Raised when task data fails validation."""
    pass


class TaskNotFoundError(Exception):
    """Raised when task ID does not exist."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


# Task Dataclass (T006)
@dataclass
class Task:
    """
    Represents a todo task with metadata.

    Attributes:
        id: Unique sequential identifier (> 0)
        title: Task title (1-100 characters after trim)
        description: Optional detailed description (max 500 chars)
        completed: Completion status (default False)
        created_at: Creation timestamp (immutable)
        updated_at: Last modification timestamp
    """
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate field constraints after initialization (T007)."""
        self._validate_id()
        self._validate_title()
        self._validate_description()
        self._validate_timestamps()

    def _validate_id(self) -> None:
        """Ensure ID is a positive integer (T008)."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")

    def _validate_title(self) -> None:
        """Ensure title meets length constraints (T008)."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 100:
            raise ValueError("Title must be 100 characters or less")

    def _validate_description(self) -> None:
        """Ensure description meets length constraints if present (T008)."""
        if self.description is not None and len(self.description) > 500:
            raise ValueError("Description must be 500 characters or less")

    def _validate_timestamps(self) -> None:
        """Ensure timestamp consistency (T008)."""
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot be before created_at")
