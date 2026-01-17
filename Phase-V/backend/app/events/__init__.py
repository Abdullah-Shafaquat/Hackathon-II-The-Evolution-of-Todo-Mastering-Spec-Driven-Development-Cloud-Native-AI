# T-V-07: Event-Driven Architecture
# From: speckit.plan - Event Producers
"""
Event publishing module for Dapr Pub/Sub integration.

This module provides:
- Event schemas for task operations
- Event publisher using Dapr sidecar
- Topics configuration
"""

from .schemas import (
    TaskEvent,
    TaskCreatedEvent,
    TaskUpdatedEvent,
    TaskDeletedEvent,
    TaskCompletedEvent,
    TaskChanges,
    EventType,
    Topics
)
from .publisher import EventPublisher, get_event_publisher

__all__ = [
    "TaskEvent",
    "TaskCreatedEvent",
    "TaskUpdatedEvent",
    "TaskDeletedEvent",
    "TaskCompletedEvent",
    "TaskChanges",
    "EventType",
    "Topics",
    "EventPublisher",
    "get_event_publisher"
]
