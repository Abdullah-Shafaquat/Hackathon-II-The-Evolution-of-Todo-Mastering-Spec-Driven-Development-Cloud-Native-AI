"""
Update Task MCP Tool
Modifies task title, description, or completion status
"""

from typing import Dict, Any, Optional
from sqlmodel import Session
from app.models import Task
from datetime import datetime


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    user_id: Optional[str] = None,  # Injected from auth context (Task 4.8)
    session: Optional[Session] = None  # Injected database session (Task 4.8)
) -> Dict[str, Any]:
    """
    Update a task's details for the authenticated user.

    This tool updates one or more fields of an existing task. At least one
    field (title, description, or completed) must be provided. It verifies
    that the task belongs to the authenticated user before updating.

    Args:
        task_id: ID of the task to update (required)
        title: New task title (1-200 characters, optional)
        description: New task description (optional, can be None to clear)
        completed: New completion status (True/False, optional)
        user_id: Authenticated user ID (injected from context, not from agent)

    Returns:
        Dict containing:
        - success (bool): True if task was updated successfully
        - task (dict): Updated task details

        On error:
        - success (bool): False
        - error (str): Error message

    Examples:
        >>> update_task(task_id=42, title="Buy milk ASAP", user_id="user123")
        {"success": true, "task": {"id": 42, "title": "Buy milk ASAP", ...}}

        >>> update_task(task_id=42, completed=True, user_id="user123")
        {"success": true, "task": {"id": 42, "completed": true, ...}}

        >>> update_task(task_id=42, user_id="user123")
        {"success": false, "error": "At least one field must be provided"}
    """
    try:
        # Validation: at least one update field must be provided
        if title is None and description is None and completed is None:
            return {
                "success": False,
                "error": "At least one field (title, description, or completed) must be provided"
            }

        # Validation: user_id must be provided (injected by context)
        if not user_id:
            return {
                "success": False,
                "error": "Authentication required: user_id not found in context"
            }

        # Validation: session must be provided (injected by context)
        if session is None:
            return {
                "success": False,
                "error": "Database session not found in context"
            }

        # Use injected session
        # Get task by ID
        task = session.get(Task, task_id)

        # Error: Task not found
        if not task:
            return {
                "success": False,
                "error": f"Task with id {task_id} not found"
            }

        # Error: Access denied (task belongs to different user)
        if task.user_id != user_id:
            return {
                "success": False,
                "error": "Access denied. This task belongs to another user"
            }

        # Update title if provided
        if title is not None:
            # Validate title length
            if len(title) < 1 or len(title) > 200:
                return {
                    "success": False,
                    "error": "Title must be 1-200 characters"
                }
            task.title = title

        # Update description if provided (can be None to clear)
        if description is not None:
            task.description = description

        # Update completion status if provided
        if completed is not None:
            task.completed = completed

        # Always update the updated_at timestamp
        task.updated_at = datetime.utcnow()

        # Save changes
        session.add(task)
        session.commit()
        session.refresh(task)

        # Return structured response
        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat()
            }
        }

    except Exception as e:
        # Handle any unexpected errors
        return {
            "success": False,
            "error": f"Failed to update task: {str(e)}"
        }
