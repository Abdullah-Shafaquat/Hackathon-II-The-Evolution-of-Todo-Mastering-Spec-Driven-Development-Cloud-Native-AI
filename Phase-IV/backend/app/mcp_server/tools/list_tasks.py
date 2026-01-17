"""
List Tasks MCP Tool
Retrieves user's tasks with optional filtering by completion status
"""

from typing import Dict, Any, Optional, Literal
from sqlmodel import Session, select
from app.models import Task
from datetime import date


def list_tasks(
    filter: Literal["all", "pending", "completed", "today"] = "all",
    category: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
    user_id: Optional[str] = None,  # Injected from auth context (Task 4.8)
    session: Optional[Session] = None  # Injected database session (Task 4.8)
) -> Dict[str, Any]:
    """
    List tasks for the authenticated user with optional filtering and sorting.

    This tool retrieves tasks from the database with optional filtering by
    completion status, date, category, or status. It also calculates statistics (total, completed, pending)
    from all user tasks regardless of the filter applied.

    Args:
        filter: Filter by completion status or date
            - "all": Return all tasks (default)
            - "pending": Return only incomplete tasks
            - "completed": Return only completed tasks
            - "today": Return only tasks due today
        category: Optional filter by category (personal, work, study, health, shopping, other)
        status: Optional filter by task status (pending, in_progress, completed)
        sort_by: Optional sort order
            - "date": Sort by due date (ascending, overdue first)
            - "priority": Sort by priority (high -> medium -> low)
            - "status": Sort by status (pending -> in_progress -> completed)
            - "recent": Sort by creation date (most recent first)
        user_id: Authenticated user ID (injected from context, not from agent)

    Returns:
        Dict containing:
        - success (bool): True if query succeeded
        - tasks (list): Array of task objects with all fields
        - total (int): Total number of user's tasks
        - completed (int): Number of completed tasks
        - pending (int): Number of pending tasks

        On error:
        - success (bool): False
        - error (str): Error message

    Examples:
        >>> list_tasks(filter="all", user_id="user123")
        {"success": true, "tasks": [...], "total": 10, "completed": 3, "pending": 7}

        >>> list_tasks(filter="today", sort_by="priority", user_id="user123")
        {"success": true, "tasks": [today's high priority tasks first], ...}

        >>> list_tasks(category="work", status="in_progress", user_id="user123")
        {"success": true, "tasks": [in-progress work tasks only], ...}
    """
    try:
        # Validation: filter must be valid value
        valid_filters = ["all", "pending", "completed", "today"]
        if filter not in valid_filters:
            return {
                "success": False,
                "error": f"Invalid filter value. Use 'all', 'pending', 'completed', or 'today'"
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
        # Build filtered query
        query = select(Task).where(Task.user_id == user_id)

        if filter == "completed":
            query = query.where(Task.completed == True)
        elif filter == "pending":
            query = query.where(Task.completed == False)
        elif filter == "today":
            # Filter tasks due today
            today = date.today()
            query = query.where(Task.due_date == today)

        # Filter by category if specified
        if category:
            valid_categories = ["personal", "work", "study", "health", "shopping", "other"]
            if category.lower() in valid_categories:
                query = query.where(Task.category == category.lower())

        # Filter by status if specified
        if status:
            valid_statuses = ["pending", "in_progress", "completed"]
            if status.lower() in valid_statuses:
                query = query.where(Task.status == status.lower())

        # Apply sorting based on sort_by parameter
        from sqlalchemy import case

        if sort_by == "priority":
            # Sort by priority: high -> medium -> low
            priority_order = case(
                (Task.priority == "high", 1),
                (Task.priority == "medium", 2),
                (Task.priority == "low", 3),
                else_=4
            )
            query = query.order_by(priority_order, Task.due_date.asc().nullslast(), Task.created_at.desc())
        elif sort_by == "status":
            # Sort by status: pending -> in_progress -> completed
            status_order = case(
                (Task.status == "pending", 1),
                (Task.status == "in_progress", 2),
                (Task.status == "completed", 3),
                else_=4
            )
            query = query.order_by(status_order, Task.created_at.desc())
        elif sort_by == "recent":
            # Sort by creation date: most recent first
            query = query.order_by(Task.created_at.desc())
        else:
            # Default: sort by due date (date sort or no sort specified)
            # Overdue tasks first, then by due date ascending, then by creation date
            query = query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc())

        # Execute filtered query
        filtered_tasks = session.exec(query).all()

        # Calculate statistics from ALL user tasks (not filtered)
        all_tasks_query = select(Task).where(Task.user_id == user_id)
        all_tasks = session.exec(all_tasks_query).all()

        total = len(all_tasks)
        completed_count = sum(1 for t in all_tasks if t.completed)
        pending_count = total - completed_count

        # Return structured response
        return {
            "success": True,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "status": t.status,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "priority": t.priority,
                    "category": t.category,
                    "created_at": t.created_at.isoformat()
                }
                for t in filtered_tasks
            ],
            "total": total,
            "completed": completed_count,
            "pending": pending_count
        }

    except Exception as e:
        # Handle any unexpected errors
        return {
            "success": False,
            "error": f"Failed to list tasks: {str(e)}"
        }
