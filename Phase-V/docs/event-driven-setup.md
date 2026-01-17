# Phase V: Event-Driven Architecture Setup

## Overview

This document describes the event-driven architecture setup for Phase V, including:
- Redpanda (Kafka-compatible message broker)
- Dapr (Distributed Application Runtime)
- Redis (State store)

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Compose Stack                         │
│                                                                     │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐   │
│  │  Redpanda   │     │    Redis    │     │  Dapr Placement     │   │
│  │  (Kafka)    │     │   (State)   │     │    Service          │   │
│  │  :19092     │     │   :6379     │     │    :50006           │   │
│  └─────────────┘     └─────────────┘     └─────────────────────┘   │
│         │                   │                      │               │
│         └───────────────────┼──────────────────────┘               │
│                             │                                       │
│                    ┌────────┴────────┐                             │
│                    │ Dapr Components │                             │
│                    │ - pubsub-kafka  │                             │
│                    │ - statestore    │                             │
│                    │ - secretstore   │                             │
│                    └────────┬────────┘                             │
│                             │                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Application Services                      │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Backend (:8000)          │  Dapr Sidecar (:3500)    │   │   │
│  │  │  FastAPI + MCP            │  Event Publishing        │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Frontend (:3000)         │  Next.js                 │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────┐                                                   │
│  │  Redpanda   │  Kafka UI for monitoring                          │
│  │  Console    │  http://localhost:8080                            │
│  │  :8080      │                                                   │
│  └─────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Kafka Topics

| Topic | Purpose | Retention | Partitions |
|-------|---------|-----------|------------|
| `task-events` | All task CRUD operations | 7 days | 3 |
| `reminders` | Scheduled reminder triggers | 1 day | 3 |
| `task-updates` | Real-time sync across clients | 1 hour | 3 |

## Event Schemas

### TaskCreated Event
```json
{
  "event_type": "task.created",
  "version": "1.0",
  "timestamp": "2025-01-16T10:00:00Z",
  "data": {
    "task_id": 123,
    "user_id": "user-uuid",
    "title": "Task title",
    "description": "Task description",
    "priority": "high",
    "category": "work",
    "due_date": "2025-01-20",
    "status": "pending"
  }
}
```

### TaskUpdated Event
```json
{
  "event_type": "task.updated",
  "version": "1.0",
  "timestamp": "2025-01-16T11:00:00Z",
  "data": {
    "task_id": 123,
    "user_id": "user-uuid",
    "changes": {
      "status": {"old": "pending", "new": "completed"},
      "priority": {"old": "medium", "new": "high"}
    }
  }
}
```

### TaskDeleted Event
```json
{
  "event_type": "task.deleted",
  "version": "1.0",
  "timestamp": "2025-01-16T12:00:00Z",
  "data": {
    "task_id": 123,
    "user_id": "user-uuid"
  }
}
```

## Quick Start

### 1. Start Infrastructure Services

```bash
# Start Redpanda, Redis, and Dapr Placement
docker-compose up -d redpanda redis placement

# Wait for Redpanda to be healthy
docker-compose ps

# Initialize Kafka topics
./scripts/init-kafka-topics.sh
```

### 2. Start Application Services

```bash
# Start backend with Dapr sidecar
docker-compose up -d backend backend-dapr

# Start frontend
docker-compose up -d frontend
```

### 3. Verify Setup

```bash
# Check all services are running
docker-compose ps

# View Redpanda Console
open http://localhost:8080

# Test Dapr sidecar health
curl http://localhost:3500/v1.0/healthz
```

## Dapr Components

### Pub/Sub Component (pubsub-kafka)

Located at: `dapr/components/pubsub-redpanda.yaml`

Publishing events:
```bash
curl -X POST http://localhost:3500/v1.0/publish/pubsub-kafka/task-events \
  -H "Content-Type: application/json" \
  -d '{"event_type": "task.created", "data": {"task_id": 1}}'
```

### State Store Component (statestore)

Located at: `dapr/components/statestore-redis.yaml`

Storing state:
```bash
curl -X POST http://localhost:3500/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{"key": "conversation-123", "value": {"messages": []}}]'
```

Retrieving state:
```bash
curl http://localhost:3500/v1.0/state/statestore/conversation-123
```

### Secret Store Component (local-secret-store)

Located at: `dapr/components/secretstore-local.yaml`

Retrieving secrets:
```bash
curl http://localhost:3500/v1.0/secrets/local-secret-store/database
```

## Troubleshooting

### Redpanda not starting
```bash
# Check logs
docker-compose logs redpanda

# Verify resources (needs 1GB+ memory)
docker stats redpanda
```

### Dapr sidecar not connecting
```bash
# Check Dapr logs
docker-compose logs backend-dapr

# Verify component files
ls -la dapr/components/

# Test Dapr health
curl http://localhost:3500/v1.0/healthz
```

### Topics not created
```bash
# Manually create topics
docker exec redpanda rpk topic create task-events --partitions 3

# List existing topics
docker exec redpanda rpk topic list
```

## Ports Reference

| Service | Port | Description |
|---------|------|-------------|
| Backend API | 8000 | FastAPI REST API |
| Dapr Sidecar | 3500 | Dapr HTTP API |
| Frontend | 3000 | Next.js UI |
| Redpanda Kafka | 19092 | Kafka protocol (external) |
| Redpanda Console | 8080 | Kafka UI |
| Redis | 6379 | State store |
| Schema Registry | 18081 | Avro/JSON schemas |
| Dapr Placement | 50006 | Actor placement |

## Next Steps

1. **T-V-07**: Implement event producers in backend
2. **T-V-08**: Create Notification Service
3. **T-V-09**: Create Recurring Task Service
4. **T-V-10**: Create Audit Service
