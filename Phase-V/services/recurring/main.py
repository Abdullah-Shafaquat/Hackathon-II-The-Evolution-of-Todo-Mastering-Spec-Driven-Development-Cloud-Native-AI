# T-V-09: Recurring Task Service
# From: speckit.plan - Recurring Task Service
"""
Recurring Task microservice that:
- Subscribes to task-events topic for task completions
- Checks if completed task has recurrence pattern
- Creates next occurrence via backend API
- Uses Dapr state store to track recurrence state
"""

import os
import json
import logging
from datetime import datetime, date, timedelta
from typing import Dict, Optional, Any
from contextlib import asynccontextmanager
from enum import Enum

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dateutil.relativedelta import relativedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
DAPR_HTTP_PORT = int(os.getenv("DAPR_HTTP_PORT", "3500"))
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
PUBSUB_NAME = "pubsub-kafka"
STATE_STORE_NAME = "statestore"


class RecurrencePattern(str, Enum):
    """Supported recurrence patterns"""
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class RecurrenceConfig(BaseModel):
    """Recurrence configuration for a task"""
    pattern: RecurrencePattern
    interval: int = 1  # e.g., every 2 weeks
    end_date: Optional[str] = None  # ISO format
    max_occurrences: Optional[int] = None
    occurrences_created: int = 0


def calculate_next_due_date(
    current_due_date: date,
    pattern: RecurrencePattern,
    interval: int = 1
) -> date:
    """Calculate the next due date based on recurrence pattern"""
    if pattern == RecurrencePattern.DAILY:
        return current_due_date + timedelta(days=interval)
    elif pattern == RecurrencePattern.WEEKLY:
        return current_due_date + timedelta(weeks=interval)
    elif pattern == RecurrencePattern.BIWEEKLY:
        return current_due_date + timedelta(weeks=2 * interval)
    elif pattern == RecurrencePattern.MONTHLY:
        return current_due_date + relativedelta(months=interval)
    elif pattern == RecurrencePattern.YEARLY:
        return current_due_date + relativedelta(years=interval)
    else:
        return current_due_date + timedelta(days=interval)


async def get_recurrence_state(task_id: int) -> Optional[Dict]:
    """Get recurrence state from Dapr state store"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/{STATE_STORE_NAME}/recurrence-{task_id}"
            )
            if response.status_code == 200 and response.text:
                return response.json()
            return None
    except Exception as e:
        logger.error(f"Error getting recurrence state: {e}")
        return None


async def save_recurrence_state(task_id: int, state: Dict) -> bool:
    """Save recurrence state to Dapr state store"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/{STATE_STORE_NAME}",
                json=[{
                    "key": f"recurrence-{task_id}",
                    "value": state
                }]
            )
            return response.status_code in (200, 204)
    except Exception as e:
        logger.error(f"Error saving recurrence state: {e}")
        return False


async def delete_recurrence_state(task_id: int) -> bool:
    """Delete recurrence state from Dapr state store"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/{STATE_STORE_NAME}/recurrence-{task_id}"
            )
            return response.status_code in (200, 204)
    except Exception as e:
        logger.error(f"Error deleting recurrence state: {e}")
        return False


async def create_next_task(
    user_id: str,
    title: str,
    description: Optional[str],
    priority: str,
    category: str,
    due_date: date,
    auth_token: Optional[str] = None
) -> Optional[Dict]:
    """Create the next occurrence of a recurring task via backend API"""
    try:
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        task_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "category": category,
            "due_date": due_date.isoformat()
        }

        # Use Dapr service invocation to call backend
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:{DAPR_HTTP_PORT}/v1.0/invoke/backend/method/api/tasks",
                json=task_data,
                headers=headers,
                timeout=30.0
            )

            if response.status_code == 201:
                logger.info(f"Created next occurrence of recurring task")
                return response.json()
            else:
                logger.error(f"Failed to create task: {response.status_code} - {response.text}")
                return None

    except Exception as e:
        logger.error(f"Error creating next task: {e}")
        return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Recurring task service starting...")
    logger.info(f"Dapr HTTP port: {DAPR_HTTP_PORT}")
    logger.info(f"Backend URL: {BACKEND_URL}")
    yield
    logger.info("Recurring task service shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Recurring Task Service",
    description="Phase V Recurring Task Service - Handles recurring task generation",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================================
# Dapr Subscription Endpoints
# ============================================================================

@app.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscription configuration"""
    subscriptions = [
        {
            "pubsubname": PUBSUB_NAME,
            "topic": "task-events",
            "route": "/events/task-events"
        }
    ]
    logger.info(f"Dapr subscriptions configured: {[s['topic'] for s in subscriptions]}")
    return JSONResponse(content=subscriptions)


@app.post("/events/task-events")
async def handle_task_events(request: Request):
    """
    Handle task events - specifically task.completed events.
    If the completed task is recurring, create the next occurrence.
    """
    try:
        event = await request.json()
        event_type = event.get("type", "")

        # Only process task.completed events
        if event_type != "task.completed":
            return {"status": "SUCCESS"}

        data = event.get("data", {})
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        completed = data.get("completed", False)

        if not completed or not task_id or not user_id:
            return {"status": "SUCCESS"}

        logger.info(f"Processing completed task {task_id} for recurrence check")

        # Check if task has recurrence state
        recurrence_state = await get_recurrence_state(task_id)

        if not recurrence_state:
            logger.debug(f"Task {task_id} has no recurrence configuration")
            return {"status": "SUCCESS"}

        logger.info(f"Task {task_id} has recurrence: {recurrence_state}")

        # Parse recurrence configuration
        config = RecurrenceConfig(**recurrence_state.get("config", {}))
        task_data = recurrence_state.get("task_data", {})

        # Check if we should create another occurrence
        should_create = True

        # Check end date
        if config.end_date:
            end_date = date.fromisoformat(config.end_date)
            if date.today() > end_date:
                logger.info(f"Recurrence ended for task {task_id} (past end date)")
                await delete_recurrence_state(task_id)
                should_create = False

        # Check max occurrences
        if config.max_occurrences and config.occurrences_created >= config.max_occurrences:
            logger.info(f"Recurrence ended for task {task_id} (max occurrences reached)")
            await delete_recurrence_state(task_id)
            should_create = False

        if should_create:
            # Calculate next due date
            current_due = date.fromisoformat(task_data.get("due_date", date.today().isoformat()))
            next_due = calculate_next_due_date(current_due, config.pattern, config.interval)

            # Create next task occurrence
            new_task = await create_next_task(
                user_id=user_id,
                title=task_data.get("title", "Recurring Task"),
                description=task_data.get("description"),
                priority=task_data.get("priority", "medium"),
                category=task_data.get("category", "other"),
                due_date=next_due
            )

            if new_task:
                # Update recurrence state for new task
                new_state = {
                    "config": {
                        **config.model_dump(),
                        "occurrences_created": config.occurrences_created + 1
                    },
                    "task_data": {
                        **task_data,
                        "due_date": next_due.isoformat()
                    },
                    "parent_task_id": task_id
                }
                await save_recurrence_state(new_task.get("id"), new_state)
                logger.info(f"Created next occurrence: task {new_task.get('id')} due {next_due}")

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"Error handling task event: {e}")
        return {"status": "RETRY"}


# ============================================================================
# Dapr Binding Endpoints (Cron)
# ============================================================================

@app.post("/recurring-scheduler")
async def handle_cron_trigger(request: Request):
    """
    Handle cron trigger from Dapr binding.
    This runs periodically to check for tasks needing reminder events.
    """
    try:
        logger.info("Cron trigger received - checking recurring tasks")

        # In a production system, this would:
        # 1. Query tasks with due dates approaching
        # 2. Publish reminder events for those tasks
        # For now, just log the trigger

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"Error handling cron trigger: {e}")
        return {"status": "RETRY"}


# ============================================================================
# API Endpoints for Recurrence Management
# ============================================================================

class SetRecurrenceRequest(BaseModel):
    """Request to set recurrence for a task"""
    task_id: int
    pattern: RecurrencePattern
    interval: int = 1
    end_date: Optional[str] = None
    max_occurrences: Optional[int] = None
    task_data: Dict[str, Any]


@app.post("/recurrence")
async def set_recurrence(request: SetRecurrenceRequest):
    """Set recurrence configuration for a task"""
    try:
        state = {
            "config": {
                "pattern": request.pattern.value,
                "interval": request.interval,
                "end_date": request.end_date,
                "max_occurrences": request.max_occurrences,
                "occurrences_created": 0
            },
            "task_data": request.task_data
        }

        success = await save_recurrence_state(request.task_id, state)

        if success:
            logger.info(f"Set recurrence for task {request.task_id}: {request.pattern}")
            return {"status": "ok", "message": f"Recurrence set for task {request.task_id}"}
        else:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Failed to save recurrence state"}
            )

    except Exception as e:
        logger.error(f"Error setting recurrence: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.get("/recurrence/{task_id}")
async def get_recurrence(task_id: int):
    """Get recurrence configuration for a task"""
    state = await get_recurrence_state(task_id)
    if state:
        return state
    return JSONResponse(
        status_code=404,
        content={"status": "error", "message": "No recurrence found for task"}
    )


@app.delete("/recurrence/{task_id}")
async def remove_recurrence(task_id: int):
    """Remove recurrence configuration for a task"""
    success = await delete_recurrence_state(task_id)
    if success:
        return {"status": "ok", "message": f"Recurrence removed for task {task_id}"}
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Failed to remove recurrence"}
    )


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "recurring-service",
        "version": "1.0.0"
    }


@app.get("/status")
async def get_status():
    """Get service status"""
    return {
        "status": "running",
        "dapr_port": DAPR_HTTP_PORT,
        "backend_url": BACKEND_URL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
