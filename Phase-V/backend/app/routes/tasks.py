"""
Task Routes
CRUD operations for todo tasks with event publishing

T-V-07: Updated to publish events via Dapr Pub/Sub
From: speckit.plan - Event-Driven Architecture
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlmodel import Session, select
from datetime import datetime
from typing import Dict, Optional
import logging

from app.database import get_session
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.middleware.auth import get_current_user
from app.events import (
    get_event_publisher,
    TaskCreatedEvent,
    TaskUpdatedEvent,
    TaskDeletedEvent,
    TaskCompletedEvent,
    TaskChanges
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
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

    T-V-07: Publishes task.created event to Kafka via Dapr
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

    # T-V-07: Publish task.created event (non-blocking)
    async def publish_created_event():
        try:
            publisher = get_event_publisher()
            event = TaskCreatedEvent.from_task(
                task_id=task.id,
                user_id=user_id,
                title=task.title,
                description=task.description,
                priority=task.priority,
                category=task.category,
                status=task.status or "pending",
                due_date=task.due_date,
                completed=task.completed
            )
            await publisher.publish_to_task_events(event)
            logger.info(f"Published task.created event for task {task.id}")
        except Exception as e:
            logger.error(f"Failed to publish task.created event: {e}")

    background_tasks.add_task(publish_created_event)

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
    background_tasks: BackgroundTasks,
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

    T-V-07: Publishes task.updated event to Kafka via Dapr
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

    # T-V-07: Track changes for event publishing
    changes = TaskChanges()
    was_completed = task.completed

    # Update fields if provided and track changes
    if task_data.title is not None and task_data.title != task.title:
        changes.title = {"old": task.title, "new": task_data.title}
        task.title = task_data.title
    if task_data.description is not None and task_data.description != task.description:
        changes.description = {"old": task.description, "new": task_data.description}
        task.description = task_data.description
    if task_data.completed is not None and task_data.completed != task.completed:
        changes.completed = {"old": task.completed, "new": task_data.completed}
        task.completed = task_data.completed
        # Sync status with completed for backward compatibility
        task.status = "completed" if task_data.completed else "pending"
    if task_data.status is not None and task_data.status != task.status:
        changes.status = {"old": task.status, "new": task_data.status}
        task.status = task_data.status
        # Sync completed with status for backward compatibility
        task.completed = (task_data.status == "completed")
    if task_data.due_date is not None:
        old_due = task.due_date.isoformat() if task.due_date else None
        new_due = task_data.due_date.isoformat() if task_data.due_date else None
        if old_due != new_due:
            changes.due_date = {"old": old_due, "new": new_due}
        task.due_date = task_data.due_date
    if task_data.priority is not None and task_data.priority != task.priority:
        changes.priority = {"old": task.priority, "new": task_data.priority}
        task.priority = task_data.priority
    if task_data.category is not None and task_data.category != task.category:
        changes.category = {"old": task.category, "new": task_data.category}
        task.category = task_data.category

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    # T-V-07: Publish task.updated event (non-blocking)
    async def publish_updated_event():
        try:
            publisher = get_event_publisher()

            # Check if task was completed/uncompleted
            if changes.completed is not None:
                completed_event = TaskCompletedEvent.from_task(
                    task_id=task.id,
                    user_id=user_id,
                    title=task.title,
                    completed=task.completed
                )
                await publisher.publish_to_task_events(completed_event)
                logger.info(f"Published task.{'completed' if task.completed else 'uncompleted'} event for task {task.id}")

            # Always publish update event
            event = TaskUpdatedEvent.from_changes(
                task_id=task.id,
                user_id=user_id,
                changes=changes
            )
            await publisher.publish_to_task_events(event)
            logger.info(f"Published task.updated event for task {task.id}")
        except Exception as e:
            logger.error(f"Failed to publish task.updated event: {e}")

    background_tasks.add_task(publish_updated_event)

    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: int,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status (complete <-> incomplete)

    Returns 404 if task doesn't exist
    Returns 403 if task belongs to another user

    T-V-07: Publishes task.completed/uncompleted event to Kafka via Dapr
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
    task.status = "completed" if task.completed else "pending"
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    # T-V-07: Publish task.completed/uncompleted event (non-blocking)
    async def publish_completion_event():
        try:
            publisher = get_event_publisher()
            event = TaskCompletedEvent.from_task(
                task_id=task.id,
                user_id=user_id,
                title=task.title,
                completed=task.completed
            )
            await publisher.publish_to_task_events(event)
            logger.info(f"Published task.{'completed' if task.completed else 'uncompleted'} event for task {task.id}")
        except Exception as e:
            logger.error(f"Failed to publish task completion event: {e}")

    background_tasks.add_task(publish_completion_event)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task

    Returns 204 No Content on success
    Returns 404 if task doesn't exist
    Returns 403 if task belongs to another user

    T-V-07: Publishes task.deleted event to Kafka via Dapr
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

    # Store task ID before deletion for event
    deleted_task_id = task.id

    # Delete task
    session.delete(task)
    session.commit()

    # T-V-07: Publish task.deleted event (non-blocking)
    async def publish_deleted_event():
        try:
            publisher = get_event_publisher()
            event = TaskDeletedEvent.from_task(
                task_id=deleted_task_id,
                user_id=user_id
            )
            await publisher.publish_to_task_events(event)
            logger.info(f"Published task.deleted event for task {deleted_task_id}")
        except Exception as e:
            logger.error(f"Failed to publish task.deleted event: {e}")

    background_tasks.add_task(publish_deleted_event)

    return None
