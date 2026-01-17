"""
Delete Task MCP Tool
Deletes a task for the authenticated user by ID or title
"""

from typing import Dict, Any, Optional, Union
from sqlmodel import Session, select
from app.models import Task


def delete_task(
    task_id: Optional[int] = None,
    title: Optional[str] = None,
    user_id: Optional[str] = None,  # Injected from auth context (Task 4.8)
    session: Optional[Session] = None  # Injected database session (Task 4.8)
) -> Dict[str, Any]:
    """
    Delete a task for the authenticated user by ID or title.

    This tool permanently removes a task from the database. It verifies that
    the task belongs to the authenticated user before deleting. You can specify
    either task_id OR title (not both).

    Args:
        task_id: ID of the task to delete (optional, use if you know the ID)
        title: Title of the task to delete (optional, will delete the first matching task)
        user_id: Authenticated user ID (injected from context, not from agent)

    Returns:
        Dict containing:
        - success (bool): True if task was deleted successfully
        - message (str): Confirmation message with task details
        - deleted_task (dict): Details of the deleted task

        On error:
        - success (bool): False
        - error (str): Error message (task not found, access denied, etc.)

    Examples:
        >>> delete_task(task_id=42, user_id="user123")
        {"success": true, "message": "Task deleted successfully", "deleted_task": {...}}

        >>> delete_task(title="Buy groceries", user_id="user123")
        {"success": true, "message": "Task deleted successfully", "deleted_task": {...}}
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

        # Validation: Either task_id or title must be provided (but not both)
        if not task_id and not title:
            return {
                "success": False,
                "error": "Either task_id or title must be provided to delete a task"
            }

        if task_id and title:
            return {
                "success": False,
                "error": "Provide either task_id OR title, not both"
            }

        # Use injected session
        task = None

        # Find task by ID
        if task_id:
            task = session.get(Task, task_id)
            if not task:
                return {
                    "success": False,
                    "error": f"Task with id {task_id} not found"
                }

        # Find task by title
        elif title:
            query = select(Task).where(
                Task.user_id == user_id,
                Task.title.ilike(f"%{title}%")  # Case-insensitive partial match
            ).order_by(Task.created_at.desc())

            tasks = session.exec(query).all()

            if not tasks:
                return {
                    "success": False,
                    "error": f"No task found matching title: '{title}'"
                }

            if len(tasks) > 1:
                # Multiple matches - provide list of options
                task_list = ", ".join([f'"{t.title}" (ID: {t.id})' for t in tasks[:5]])
                return {
                    "success": False,
                    "error": f"Multiple tasks found matching '{title}': {task_list}. Please specify by ID or use a more specific title."
                }

            task = tasks[0]

        # Error: Access denied (task belongs to different user)
        if task.user_id != user_id:
            return {
                "success": False,
                "error": "Access denied. This task belongs to another user"
            }

        # Store task info before deleting
        deleted_task_info = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }

        # Delete task
        session.delete(task)
        session.commit()

        # Return success confirmation
        return {
            "success": True,
            "message": f"Task '{task.title}' deleted successfully",
            "deleted_task": deleted_task_info
        }

    except Exception as e:
        # Handle any unexpected errors
        return {
            "success": False,
            "error": f"Failed to delete task: {str(e)}"
        }
