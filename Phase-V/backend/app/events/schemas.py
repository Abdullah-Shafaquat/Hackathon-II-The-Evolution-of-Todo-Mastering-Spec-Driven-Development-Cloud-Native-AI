# T-V-07: Event Schemas for Task Operations
# From: speckit.plan - Event-Driven Architecture
"""
Event schemas following CloudEvents specification.

Events are versioned and include:
- event_type: Type of operation
- version: Schema version for evolution
- timestamp: When event occurred
- data: Event payload with task details
"""

from datetime import datetime, date
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class EventType(str, Enum):
    """Task event types"""
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_DELETED = "task.deleted"
    TASK_COMPLETED = "task.completed"
    TASK_UNCOMPLETED = "task.uncompleted"
    REMINDER_SCHEDULED = "reminder.scheduled"
    REMINDER_TRIGGERED = "reminder.triggered"


class Topics(str, Enum):
    """Kafka topic names"""
    TASK_EVENTS = "task-events"
    REMINDERS = "reminders"
    TASK_UPDATES = "task-updates"


class TaskData(BaseModel):
    """Task data payload for events"""
    task_id: int
    user_id: str
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    category: str = "other"
    status: str = "pending"
    due_date: Optional[str] = None  # ISO format date string
    completed: bool = False

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None,
            datetime: lambda v: v.isoformat() if v else None
        }


class TaskChanges(BaseModel):
    """Track what changed in an update event"""
    title: Optional[Dict[str, str]] = None  # {"old": "x", "new": "y"}
    description: Optional[Dict[str, Optional[str]]] = None
    priority: Optional[Dict[str, str]] = None
    category: Optional[Dict[str, str]] = None
    status: Optional[Dict[str, str]] = None
    due_date: Optional[Dict[str, Optional[str]]] = None
    completed: Optional[Dict[str, bool]] = None


class TaskEvent(BaseModel):
    """Base event schema following CloudEvents spec"""
    # CloudEvents required fields
    specversion: str = "1.0"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "todo-backend"
    type: str  # EventType value

    # CloudEvents optional fields
    datacontenttype: str = "application/json"
    time: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    # Custom extension fields
    version: str = "1.0"  # Schema version for evolution

    # Event data
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for publishing"""
        return self.model_dump()


class TaskCreatedEvent(TaskEvent):
    """Event published when a task is created"""
    type: str = EventType.TASK_CREATED.value

    @classmethod
    def from_task(cls, task_id: int, user_id: str, title: str,
                  description: Optional[str] = None,
                  priority: str = "medium",
                  category: str = "other",
                  status: str = "pending",
                  due_date: Optional[date] = None,
                  completed: bool = False) -> "TaskCreatedEvent":
        """Create event from task data"""
        data = TaskData(
            task_id=task_id,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            category=category,
            status=status,
            due_date=due_date.isoformat() if due_date else None,
            completed=completed
        )
        return cls(data=data.model_dump())


class TaskUpdatedEvent(TaskEvent):
    """Event published when a task is updated"""
    type: str = EventType.TASK_UPDATED.value

    @classmethod
    def from_changes(cls, task_id: int, user_id: str,
                     changes: TaskChanges) -> "TaskUpdatedEvent":
        """Create event from task changes"""
        return cls(
            data={
                "task_id": task_id,
                "user_id": user_id,
                "changes": changes.model_dump(exclude_none=True)
            }
        )


class TaskDeletedEvent(TaskEvent):
    """Event published when a task is deleted"""
    type: str = EventType.TASK_DELETED.value

    @classmethod
    def from_task(cls, task_id: int, user_id: str) -> "TaskDeletedEvent":
        """Create event from task ID"""
        return cls(
            data={
                "task_id": task_id,
                "user_id": user_id
            }
        )


class TaskCompletedEvent(TaskEvent):
    """Event published when a task is marked complete"""
    type: str = EventType.TASK_COMPLETED.value

    @classmethod
    def from_task(cls, task_id: int, user_id: str, title: str,
                  completed: bool = True) -> "TaskCompletedEvent":
        """Create event from task completion"""
        return cls(
            type=EventType.TASK_COMPLETED.value if completed else EventType.TASK_UNCOMPLETED.value,
            data={
                "task_id": task_id,
                "user_id": user_id,
                "title": title,
                "completed": completed
            }
        )


class ReminderScheduledEvent(TaskEvent):
    """Event published when a reminder is scheduled"""
    type: str = EventType.REMINDER_SCHEDULED.value

    @classmethod
    def from_task(cls, task_id: int, user_id: str, title: str,
                  due_date: date, remind_at: datetime) -> "ReminderScheduledEvent":
        """Create event for reminder scheduling"""
        return cls(
            data={
                "task_id": task_id,
                "user_id": user_id,
                "title": title,
                "due_date": due_date.isoformat(),
                "remind_at": remind_at.isoformat() + "Z"
            }
        )
