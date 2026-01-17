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
    - **due_date**: Optional due date
    - **priority**: Priority level (low, medium, high)
    - **category**: Task category (personal, work, study, health, shopping, other)

    Returns the created task with timestamps
    """
    user_id = current_user["user_id"]

    # Create new task
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        priority=task_data.priority or "medium",
        category=task_data.category or "other",
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

    # Convert Task objects to TaskResponse objects
    task_responses = [TaskResponse.model_validate(task) for task in tasks]

    # Calculate statistics (always from all tasks, not filtered)
    all_tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

    total = len(all_tasks)
    completed = sum(1 for task in all_tasks if task.completed)
    pending = total - completed

    return TaskListResponse(
        tasks=task_responses,
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
    - **due_date**: New due date (optional)
    - **priority**: New priority level (optional)
    - **category**: New category (optional)

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
        # Sync status with completed for backward compatibility
        task.status = "completed" if task_data.completed else "pending"
    if task_data.status is not None:
        task.status = task_data.status
        # Sync completed with status for backward compatibility
        task.completed = (task_data.status == "completed")
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.category is not None:
        task.category = task_data.category

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
