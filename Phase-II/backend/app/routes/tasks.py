"""
Task Routes
CRUD operations for todo tasks
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime
from typing import Dict

from app.database import get_session
from app.models import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskListResponse
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
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user

    Returns tasks sorted by creation date (newest first) with statistics
    """
    user_id = current_user["user_id"]

    # Query tasks for current user, sorted by created_at DESC
    tasks = session.exec(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    ).all()

    # Calculate statistics
    total = len(tasks)
    completed = sum(1 for task in tasks if task.completed)
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
