# T-V-08: Notification Service
# From: speckit.plan - Notification Service
"""
Notification microservice that:
- Subscribes to task-events and reminders topics via Dapr
- Broadcasts notifications to connected WebSocket clients
- Manages user notification preferences
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Set
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = int(os.getenv("DAPR_HTTP_PORT", "3500"))
PUBSUB_NAME = "pubsub-kafka"


class ConnectionManager:
    """Manages WebSocket connections per user"""

    def __init__(self):
        # Map of user_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        logger.info(f"User {user_id} connected. Active connections: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a WebSocket connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected")

    async def send_to_user(self, user_id: str, message: dict):
        """Send a notification to all connections for a user"""
        if user_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to user {user_id}: {e}")
                    disconnected.add(connection)

            # Clean up disconnected sockets
            for conn in disconnected:
                self.active_connections[user_id].discard(conn)

            logger.info(f"Sent notification to user {user_id}: {message.get('type')}")
        else:
            logger.debug(f"User {user_id} has no active connections")

    async def broadcast(self, message: dict):
        """Send a notification to all connected users"""
        for user_id in list(self.active_connections.keys()):
            await self.send_to_user(user_id, message)


# Global connection manager
manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Notification service starting...")
    logger.info(f"Dapr HTTP port: {DAPR_HTTP_PORT}")
    yield
    logger.info("Notification service shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Notification Service",
    description="Phase V Notification Service - Consumes events and sends real-time notifications",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================================
# Dapr Subscription Endpoints
# ============================================================================

@app.get("/dapr/subscribe")
async def subscribe():
    """
    Dapr subscription configuration.
    Tells Dapr which topics this service subscribes to.
    """
    subscriptions = [
        {
            "pubsubname": PUBSUB_NAME,
            "topic": "task-events",
            "route": "/events/task-events"
        },
        {
            "pubsubname": PUBSUB_NAME,
            "topic": "reminders",
            "route": "/events/reminders"
        },
        {
            "pubsubname": PUBSUB_NAME,
            "topic": "task-updates",
            "route": "/events/task-updates"
        }
    ]
    logger.info(f"Dapr subscriptions configured: {[s['topic'] for s in subscriptions]}")
    return JSONResponse(content=subscriptions)


@app.post("/events/task-events")
async def handle_task_events(request: Request):
    """
    Handle events from the task-events topic.
    Sends notifications for task created, completed, deleted events.
    """
    try:
        # Parse CloudEvent
        event = await request.json()
        logger.info(f"Received task event: {event.get('type')}")

        event_type = event.get("type", "")
        data = event.get("data", {})
        user_id = data.get("user_id")

        if not user_id:
            logger.warning("Event missing user_id, skipping notification")
            return {"status": "SKIP"}

        # Create notification based on event type
        notification = None

        if event_type == "task.created":
            notification = {
                "type": "task.created",
                "title": "New Task Created",
                "message": f"Task '{data.get('title')}' has been created",
                "task_id": data.get("task_id"),
                "timestamp": datetime.utcnow().isoformat()
            }

        elif event_type == "task.completed":
            notification = {
                "type": "task.completed",
                "title": "Task Completed",
                "message": f"Task '{data.get('title')}' has been marked as complete",
                "task_id": data.get("task_id"),
                "timestamp": datetime.utcnow().isoformat()
            }

        elif event_type == "task.uncompleted":
            notification = {
                "type": "task.uncompleted",
                "title": "Task Reopened",
                "message": f"Task '{data.get('title')}' has been reopened",
                "task_id": data.get("task_id"),
                "timestamp": datetime.utcnow().isoformat()
            }

        elif event_type == "task.deleted":
            notification = {
                "type": "task.deleted",
                "title": "Task Deleted",
                "message": "A task has been deleted",
                "task_id": data.get("task_id"),
                "timestamp": datetime.utcnow().isoformat()
            }

        elif event_type == "task.updated":
            changes = data.get("changes", {})
            if changes:
                change_summary = ", ".join(changes.keys())
                notification = {
                    "type": "task.updated",
                    "title": "Task Updated",
                    "message": f"Task updated: {change_summary}",
                    "task_id": data.get("task_id"),
                    "changes": changes,
                    "timestamp": datetime.utcnow().isoformat()
                }

        # Send notification to user
        if notification:
            await manager.send_to_user(user_id, notification)
            logger.info(f"Notification sent to user {user_id}: {notification['type']}")

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"Error handling task event: {e}")
        return {"status": "RETRY"}


@app.post("/events/reminders")
async def handle_reminders(request: Request):
    """
    Handle events from the reminders topic.
    Sends reminder notifications to users.
    """
    try:
        event = await request.json()
        logger.info(f"Received reminder event: {event.get('type')}")

        data = event.get("data", {})
        user_id = data.get("user_id")

        if not user_id:
            logger.warning("Reminder event missing user_id")
            return {"status": "SKIP"}

        notification = {
            "type": "reminder",
            "title": "Task Reminder",
            "message": f"Reminder: {data.get('title')} is due soon",
            "task_id": data.get("task_id"),
            "due_date": data.get("due_date"),
            "timestamp": datetime.utcnow().isoformat()
        }

        await manager.send_to_user(user_id, notification)
        logger.info(f"Reminder sent to user {user_id}")

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"Error handling reminder event: {e}")
        return {"status": "RETRY"}


@app.post("/events/task-updates")
async def handle_task_updates(request: Request):
    """
    Handle events from the task-updates topic.
    Used for real-time sync across multiple clients.
    """
    try:
        event = await request.json()
        logger.info(f"Received task update event")

        data = event.get("data", {})
        user_id = data.get("user_id")

        if not user_id:
            return {"status": "SKIP"}

        # Broadcast sync event to all user's connections
        sync_message = {
            "type": "sync",
            "action": "refresh",
            "timestamp": datetime.utcnow().isoformat()
        }

        await manager.send_to_user(user_id, sync_message)

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error(f"Error handling task update event: {e}")
        return {"status": "RETRY"}


# ============================================================================
# WebSocket Endpoint
# ============================================================================

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time notifications.
    Clients connect here to receive push notifications.
    """
    await manager.connect(websocket, user_id)
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to notification service",
            "timestamp": datetime.utcnow().isoformat()
        })

        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Handle ping/pong for keepalive
            if data == "ping":
                await websocket.send_text("pong")
            else:
                # Echo back any other messages (for debugging)
                logger.debug(f"Received from {user_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "notification-service",
        "version": "1.0.0",
        "active_connections": sum(len(conns) for conns in manager.active_connections.values())
    }


@app.get("/status")
async def get_status():
    """Get service status and statistics"""
    return {
        "status": "running",
        "connected_users": len(manager.active_connections),
        "total_connections": sum(len(conns) for conns in manager.active_connections.values()),
        "dapr_port": DAPR_HTTP_PORT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
