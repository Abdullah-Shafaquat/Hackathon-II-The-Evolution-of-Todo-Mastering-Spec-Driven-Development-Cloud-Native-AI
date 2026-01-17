# T-V-10: Audit Service
# From: speckit.plan - Audit Service
"""
Audit microservice that:
- Subscribes to all Kafka topics
- Stores complete audit history in database
- Provides query API for audit records
- Generates activity reports
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
DAPR_HTTP_PORT = int(os.getenv("DAPR_HTTP_PORT", "3500"))
DATABASE_URL = os.getenv("DATABASE_URL", "")
PUBSUB_NAME = "pubsub-kafka"


# ============================================================================
# Database Models
# ============================================================================

class AuditLog(SQLModel, table=True):
    """Audit log entry stored in database"""
    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(index=True)  # CloudEvent ID
    event_type: str = Field(index=True)
    topic: str = Field(index=True)
    user_id: Optional[str] = Field(default=None, index=True)
    entity_type: str = Field(index=True)  # "task", "conversation", etc.
    entity_id: Optional[int] = Field(default=None, index=True)
    action: str  # "created", "updated", "deleted", "completed"
    old_data: Optional[str] = None  # JSON string
    new_data: Optional[str] = None  # JSON string
    event_metadata: Optional[str] = None  # JSON string for extra info (renamed from 'metadata' which is reserved)
    source: str = "backend"
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Database engine (created on startup)
engine = None


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session


def create_tables():
    """Create database tables"""
    if engine:
        SQLModel.metadata.create_all(engine)
        logger.info("Audit tables created")


# ============================================================================
# Pydantic Models
# ============================================================================

class AuditLogResponse(BaseModel):
    """Response model for audit log entries"""
    id: int
    event_id: str
    event_type: str
    topic: str
    user_id: Optional[str]
    entity_type: str
    entity_id: Optional[int]
    action: str
    old_data: Optional[Dict]
    new_data: Optional[Dict]
    event_metadata: Optional[Dict]
    source: str
    timestamp: datetime

    class Config:
        from_attributes = True


class AuditStats(BaseModel):
    """Audit statistics"""
    total_events: int
    events_by_type: Dict[str, int]
    events_by_action: Dict[str, int]
    events_today: int
    unique_users: int


# ============================================================================
# Helper Functions
# ============================================================================

def parse_event_to_audit(event: Dict, topic: str) -> AuditLog:
    """Parse a CloudEvent into an AuditLog entry"""
    event_type = event.get("type", "unknown")
    data = event.get("data", {})

    # Determine action from event type
    action = "unknown"
    if "created" in event_type:
        action = "created"
    elif "updated" in event_type:
        action = "updated"
    elif "deleted" in event_type:
        action = "deleted"
    elif "completed" in event_type:
        action = "completed"
    elif "uncompleted" in event_type:
        action = "uncompleted"

    # Determine entity type
    entity_type = "unknown"
    if "task" in event_type:
        entity_type = "task"
    elif "reminder" in event_type:
        entity_type = "reminder"
    elif "conversation" in event_type:
        entity_type = "conversation"

    # Extract changes for update events
    old_data = None
    new_data = None
    if action == "updated" and "changes" in data:
        changes = data.get("changes", {})
        old_data = {k: v.get("old") for k, v in changes.items() if isinstance(v, dict)}
        new_data = {k: v.get("new") for k, v in changes.items() if isinstance(v, dict)}
    elif action == "created":
        new_data = data

    return AuditLog(
        event_id=event.get("id", ""),
        event_type=event_type,
        topic=topic,
        user_id=data.get("user_id"),
        entity_type=entity_type,
        entity_id=data.get("task_id") or data.get("entity_id"),
        action=action,
        old_data=json.dumps(old_data) if old_data else None,
        new_data=json.dumps(new_data) if new_data else None,
        event_metadata=json.dumps(event.get("metadata")) if event.get("metadata") else None,
        source=event.get("source", "backend"),
        timestamp=datetime.fromisoformat(event.get("time", "").replace("Z", "+00:00"))
        if event.get("time") else datetime.utcnow()
    )


async def save_audit_log(audit: AuditLog) -> bool:
    """Save audit log to database"""
    if not engine:
        logger.warning("Database not configured, skipping audit save")
        return False

    try:
        with Session(engine) as session:
            session.add(audit)
            session.commit()
            logger.debug(f"Saved audit log: {audit.event_type}")
            return True
    except Exception as e:
        logger.error(f"Error saving audit log: {e}")
        return False


# ============================================================================
# Application Setup
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    global engine

    logger.info("Audit service starting...")
    logger.info(f"Dapr HTTP port: {DAPR_HTTP_PORT}")

    # Initialize database if configured
    if DATABASE_URL:
        try:
            engine = create_engine(DATABASE_URL, echo=False)
            create_tables()
            logger.info("Database connected and tables created")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            logger.warning("Audit service will run without database persistence")
    else:
        logger.warning("DATABASE_URL not configured, audit logs will not be persisted")

    yield

    logger.info("Audit service shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Audit Service",
    description="Phase V Audit Service - Records all system events for compliance and debugging",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================================
# Dapr Subscription Endpoints
# ============================================================================

@app.get("/dapr/subscribe")
async def subscribe():
    """Dapr subscription configuration - subscribe to all topics"""
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
    """Handle and audit task events"""
    try:
        event = await request.json()
        logger.info(f"Auditing task event: {event.get('type')}")

        audit = parse_event_to_audit(event, "task-events")
        await save_audit_log(audit)

        return {"status": "SUCCESS"}
    except Exception as e:
        logger.error(f"Error auditing task event: {e}")
        return {"status": "RETRY"}


@app.post("/events/reminders")
async def handle_reminders(request: Request):
    """Handle and audit reminder events"""
    try:
        event = await request.json()
        logger.info(f"Auditing reminder event: {event.get('type')}")

        audit = parse_event_to_audit(event, "reminders")
        await save_audit_log(audit)

        return {"status": "SUCCESS"}
    except Exception as e:
        logger.error(f"Error auditing reminder event: {e}")
        return {"status": "RETRY"}


@app.post("/events/task-updates")
async def handle_task_updates(request: Request):
    """Handle and audit task update events"""
    try:
        event = await request.json()
        logger.info(f"Auditing task update event")

        audit = parse_event_to_audit(event, "task-updates")
        await save_audit_log(audit)

        return {"status": "SUCCESS"}
    except Exception as e:
        logger.error(f"Error auditing task update event: {e}")
        return {"status": "RETRY"}


# ============================================================================
# Query API Endpoints
# ============================================================================

@app.get("/audit", response_model=List[AuditLogResponse])
async def query_audit_logs(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type (task, reminder)"),
    entity_id: Optional[int] = Query(None, description="Filter by entity ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    action: Optional[str] = Query(None, description="Filter by action (created, updated, deleted)"),
    from_date: Optional[datetime] = Query(None, description="Filter from date"),
    to_date: Optional[datetime] = Query(None, description="Filter to date"),
    limit: int = Query(100, le=1000, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Results offset")
):
    """Query audit logs with filters"""
    if not engine:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        with Session(engine) as session:
            query = select(AuditLog)

            # Apply filters
            if user_id:
                query = query.where(AuditLog.user_id == user_id)
            if entity_type:
                query = query.where(AuditLog.entity_type == entity_type)
            if entity_id:
                query = query.where(AuditLog.entity_id == entity_id)
            if event_type:
                query = query.where(AuditLog.event_type == event_type)
            if action:
                query = query.where(AuditLog.action == action)
            if from_date:
                query = query.where(AuditLog.timestamp >= from_date)
            if to_date:
                query = query.where(AuditLog.timestamp <= to_date)

            # Order and paginate
            query = query.order_by(AuditLog.timestamp.desc())
            query = query.offset(offset).limit(limit)

            results = session.exec(query).all()

            # Convert to response models
            return [
                AuditLogResponse(
                    id=r.id,
                    event_id=r.event_id,
                    event_type=r.event_type,
                    topic=r.topic,
                    user_id=r.user_id,
                    entity_type=r.entity_type,
                    entity_id=r.entity_id,
                    action=r.action,
                    old_data=json.loads(r.old_data) if r.old_data else None,
                    new_data=json.loads(r.new_data) if r.new_data else None,
                    event_metadata=json.loads(r.event_metadata) if r.event_metadata else None,
                    source=r.source,
                    timestamp=r.timestamp
                )
                for r in results
            ]

    except Exception as e:
        logger.error(f"Error querying audit logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audit/entity/{entity_type}/{entity_id}", response_model=List[AuditLogResponse])
async def get_entity_history(
    entity_type: str,
    entity_id: int,
    limit: int = Query(50, le=500)
):
    """Get complete audit history for a specific entity"""
    return await query_audit_logs(
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit
    )


@app.get("/audit/stats", response_model=AuditStats)
async def get_audit_stats(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    days: int = Query(7, le=90, description="Number of days to analyze")
):
    """Get audit statistics"""
    if not engine:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        with Session(engine) as session:
            # Base query
            base_query = select(AuditLog)
            if user_id:
                base_query = base_query.where(AuditLog.user_id == user_id)

            # Total events
            total = len(session.exec(base_query).all())

            # Events by type
            all_logs = session.exec(base_query).all()
            events_by_type = {}
            events_by_action = {}
            unique_users = set()

            today = datetime.utcnow().date()
            events_today = 0

            for log in all_logs:
                # Count by type
                events_by_type[log.event_type] = events_by_type.get(log.event_type, 0) + 1
                # Count by action
                events_by_action[log.action] = events_by_action.get(log.action, 0) + 1
                # Unique users
                if log.user_id:
                    unique_users.add(log.user_id)
                # Today's events
                if log.timestamp.date() == today:
                    events_today += 1

            return AuditStats(
                total_events=total,
                events_by_type=events_by_type,
                events_by_action=events_by_action,
                events_today=events_today,
                unique_users=len(unique_users)
            )

    except Exception as e:
        logger.error(f"Error getting audit stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if engine else "not configured"

    return {
        "status": "ok",
        "service": "audit-service",
        "version": "1.0.0",
        "database": db_status
    }


@app.get("/status")
async def get_status():
    """Get service status"""
    return {
        "status": "running",
        "dapr_port": DAPR_HTTP_PORT,
        "database_configured": bool(DATABASE_URL),
        "database_connected": engine is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
