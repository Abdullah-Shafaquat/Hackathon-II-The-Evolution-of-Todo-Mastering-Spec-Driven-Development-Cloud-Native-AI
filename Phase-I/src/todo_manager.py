"""Business logic for CRUD operations"""

from datetime import datetime
from typing import List, Optional, Dict
from src.models import Task, ValidationError, TaskNotFoundError


# Global State (T009)
tasks: List[Task] = []  # List of all active tasks
next_id: int = 1        # Sequential ID counter (never reused)


def add_task(title: str, description: Optional[str] = None) -> Task:
    """
    Create a new task with auto-generated ID and timestamps (T022).

    Args:
        title: Task title (will be trimmed, must be 1-100 chars after trim) (T023)
        description: Optional description (max 500 characters) (T024)

    Returns:
        The newly created Task instance (T025)

    Raises:
        ValidationError: If title is empty (after trim) or > 100 chars
        ValidationError: If description > 500 chars
    """
    global next_id

    # Trim and validate title (T023)
    title = title.strip()
    if not title:
        raise ValidationError("Title cannot be empty. Please enter a title.")
    if len(title) > 100:
        raise ValidationError("Title must be 100 characters or less")

    # Validate description (T024)
    if description is not None:
        if description.strip() == "":
            description = None
        elif len(description) > 500:
            raise ValidationError("Description must be 500 characters or less")

    # Create task with auto-generated ID and timestamps (T025)
    now = datetime.now()
    task = Task(
        id=next_id,
        title=title,
        description=description,
        completed=False,
        created_at=now,
        updated_at=now
    )

    # Append to global list and increment ID (T026, T027)
    tasks.append(task)
    next_id += 1

    return task


def get_all_tasks() -> List[Task]:
    """
    Return all tasks sorted by creation date (newest first) (T041).

    Returns:
        List of all tasks in descending order by created_at
    """
    return sorted(tasks, key=lambda t: t.created_at, reverse=True)


def get_task_statistics() -> Dict[str, int]:
    """
    Compute summary statistics for all tasks (T042).

    Returns:
        Dictionary with keys "total", "completed", "pending"
    """
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    pending = total - completed

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }


def get_task_by_id(task_id: int) -> Task:
    """
    Retrieve a task by its unique ID (T059).

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        The task with matching ID

    Raises:
        TaskNotFoundError: If no task exists with the given ID
    """
    for task in tasks:
        if task.id == task_id:
            return task
    raise TaskNotFoundError(task_id)


def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
    """
    Update a task's title and/or description (T061).

    Args:
        task_id: The ID of the task to update
        title: New title (None = keep current)
        description: New description (None = keep current, "." = clear to None)

    Returns:
        The updated task

    Raises:
        TaskNotFoundError: If no task exists with the given ID
        ValidationError: If new title or description fail validation
    """
    # Find task
    task = get_task_by_id(task_id)

    # Determine new values (T062, T063)
    new_title = title.strip() if title is not None else task.title
    new_description = task.description

    # Handle description update (T064)
    if description is not None:
        if description == ".":
            new_description = None
        else:
            new_description = description

    # Validate new title
    if not new_title:
        raise ValidationError("Title cannot be empty. Please enter a title.")
    if len(new_title) > 100:
        raise ValidationError("Title must be 100 characters or less")

    # Validate new description
    if new_description is not None and len(new_description) > 500:
        raise ValidationError("Description must be 500 characters or less")

    # Update timestamp (T065)
    now = datetime.now()

    # Create new task instance with updated values (T066)
    updated_task = Task(
        id=task.id,
        title=new_title,
        description=new_description,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=now
    )

    # Replace in list
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = updated_task
            break

    return updated_task


def delete_task(task_id: int) -> None:
    """
    Delete a task by ID (T079).

    Args:
        task_id: The ID of the task to delete

    Raises:
        TaskNotFoundError: If no task exists with the given ID
    """
    # Find and remove task (T080)
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return

    # Task not found (T081)
    raise TaskNotFoundError(task_id)


def toggle_task_completion(task_id: int) -> Task:
    """
    Toggle a task's completion status (T095).

    Args:
        task_id: The ID of the task to toggle

    Returns:
        The updated task with toggled completed status

    Raises:
        TaskNotFoundError: If no task exists with the given ID
    """
    # Find task
    task = get_task_by_id(task_id)

    # Toggle completion and update timestamp (T096, T097)
    now = datetime.now()
    toggled_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=not task.completed,  # Flip boolean
        created_at=task.created_at,
        updated_at=now
    )

    # Replace in list (T098)
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = toggled_task
            break

    return toggled_task
