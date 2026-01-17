"""
Add Task MCP Tool
Creates a new todo task for the authenticated user
"""

from typing import Optional, Dict, Any
from sqlmodel import Session
from app.models import Task
from datetime import date, datetime


def add_task(
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    user_id: Optional[str] = None,  # Injected from auth context (Task 4.8)
    session: Optional[Session] = None  # Injected database session (Task 4.8)
) -> Dict[str, Any]:
    """
    Create a new todo task for the authenticated user.

    This tool creates a task in the database and returns the created task details.
    The user_id is injected from the authenticated session context.

    Args:
        title: Task title (1-200 characters, required)
        description: Optional task description (can be None)
        due_date: Optional due date in ISO format (YYYY-MM-DD), "today", "tomorrow", or natural language
        priority: Optional priority level ("low", "medium", "high"). Defaults to "medium"
        category: Optional category ("personal", "work", "study", "health", "shopping", "other"). Defaults to "other"
        user_id: Authenticated user ID (injected from context, not from agent)

    Returns:
        Dict containing:
        - success (bool): True if task created successfully
        - task_id (int): ID of the created task
        - task (dict): Task details including all fields

        On error:
        - success (bool): False
        - error (str): Error message

    Examples:
        >>> add_task(title="Buy groceries", due_date="2026-01-10", priority="high", category="shopping", user_id="user123")
        {"success": true, "task_id": 42, "task": {...}}

        >>> add_task(title="Meeting", due_date="today", priority="high", category="work", user_id="user123")
        {"success": true, "task_id": 43, "task": {...}}
    """
    try:
        # Validation: title is required and must be 1-200 characters
        if not title:
            return {
                "success": False,
                "error": "Title is required and cannot be empty"
            }

        if len(title) > 200:
            return {
                "success": False,
                "error": "Title must be 1-200 characters"
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

        # Parse due_date if provided
        parsed_due_date = None
        if due_date:
            try:
                # Handle natural language dates
                due_date_lower = due_date.lower().strip()
                today = date.today()

                if due_date_lower == "today":
                    parsed_due_date = today
                elif due_date_lower == "tomorrow":
                    from datetime import timedelta
                    parsed_due_date = today + timedelta(days=1)
                else:
                    # Try parsing as ISO date (YYYY-MM-DD)
                    parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid date format: '{due_date}'. Use YYYY-MM-DD, 'today', or 'tomorrow'"
                }

        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        task_priority = (priority or "medium").lower()
        if task_priority not in valid_priorities:
            return {
                "success": False,
                "error": f"Invalid priority: '{priority}'. Use 'low', 'medium', or 'high'"
            }

        # Validate category
        valid_categories = ["personal", "work", "study", "health", "shopping", "other"]
        task_category = (category or "other").lower()
        if task_category not in valid_categories:
            return {
                "success": False,
                "error": f"Invalid category: '{category}'. Use one of: {', '.join(valid_categories)}"
            }

        # Use injected session (no 'with' block needed, managed by FastAPI)
        # Create new task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
            due_date=parsed_due_date,
            priority=task_priority,
            category=task_category
        )

        # Save to database
        session.add(task)
        session.commit()
        session.refresh(task)

        # Return structured response
        return {
            "success": True,
            "task_id": task.id,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "category": task.category,
                "created_at": task.created_at.isoformat()
            }
        }

    except Exception as e:
        # Handle any unexpected errors
        return {
            "success": False,
            "error": f"Failed to create task: {str(e)}"
        }
