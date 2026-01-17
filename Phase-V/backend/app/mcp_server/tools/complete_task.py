"""
Complete Task MCP Tool
Marks a task as complete for the authenticated user
"""

from typing import Dict, Any, Optional
from sqlmodel import Session
from app.models import Task
from datetime import datetime


def complete_task(
    task_id: int,
    user_id: Optional[str] = None,  # Injected from auth context (Task 4.8)
    session: Optional[Session] = None  # Injected database session (Task 4.8)
) -> Dict[str, Any]:
    """
    Mark a task as complete for the authenticated user.

    This tool updates a task's completion status to True. It verifies that
    the task belongs to the authenticated user before updating.

    Args:
        task_id: ID of the task to mark as complete (required)
        user_id: Authenticated user ID (injected from context, not from agent)

    Returns:
        Dict containing:
        - success (bool): True if task was completed successfully
        - task (dict): Updated task details with id, title, completed, updated_at

        On error:
        - success (bool): False
        - error (str): Error message (task not found, access denied, etc.)

    Examples:
        >>> complete_task(task_id=42, user_id="user123")
        {"success": true, "task": {"id": 42, "title": "Buy milk", ...}}

        >>> complete_task(task_id=999, user_id="user123")
        {"success": false, "error": "Task with id 999 not found"}
    """
    try:
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

        # Update task
        task.completed = True
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
            "error": f"Failed to complete task: {str(e)}"
        }
