"""
Task Routes
CRUD operations for todo tasks
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from datetime import datetime
from typing import Dict, Optional

from app.database import get_session
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.middleware.auth import get_current_user


# Create router
router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user

    - **title**: Task title (1-200 characters, required)
    - **description**: Optional task description

    Returns the created task with timestamps
    """
    user_id = current_user["user_id"]

    # Create new task
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    filter: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user

    - **filter**: Optional filter by status (all, pending, completed)

    Returns tasks sorted by creation date (newest first) with statistics
    """
    user_id = current_user["user_id"]

    # Build query with filtering
    query = select(Task).where(Task.user_id == user_id)

    if filter == "completed":
        query = query.where(Task.completed == True)
    elif filter == "pending":
        query = query.where(Task.completed == False)
    # "all" or None shows everything

    query = query.order_by(Task.created_at.desc())

    # Execute query
    tasks = session.exec(query).all()

    # Calculate statistics (always from all tasks, not filtered)
    all_tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

    total = len(all_tasks)
    completed = sum(1 for task in all_tasks if task.completed)
    pending = total - completed

    return TaskListResponse(
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a single task by ID

    Returns 404 if task doesn't exist
    Returns 403 if task belongs to another user
    """
    user_id = current_user["user_id"]

    # Find task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This task belongs to another user"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task

    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **completed**: New completion status (optional)

    Returns 404 if task doesn't exist
    Returns 403 if task belongs to another user
    """
    user_id = current_user["user_id"]

    # Find task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This task belongs to another user"
        )

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: int,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status (complete <-> incomplete)

    Returns 404 if task doesn't exist
    Returns 403 if task belongs to another user
    """
    user_id = current_user["user_id"]

    # Find task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This task belongs to another user"
        )

    # Toggle completion
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task

    Returns 204 No Content on success
    Returns 404 if task doesn't exist
    Returns 403 if task belongs to another user
    """
    user_id = current_user["user_id"]

    # Find task
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This task belongs to another user"
        )

    # Delete task
    session.delete(task)
    session.commit()

    return None
