# Tasks API Contract

**Feature**: `001-phase2-fullstack-web-app` | **API**: Task Management Endpoints
**Base URL**: `/api/tasks` | **Version**: 1.0.0

## Overview

This contract defines the task management API endpoints for CRUD operations on todo tasks. All endpoints require JWT authentication and enforce user isolation (users can only access their own tasks).

## Authentication

All task endpoints require JWT token in `Authorization` header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Missing/Invalid Token**: Returns `401 Unauthorized` with `{"detail": "Invalid or expired token"}`

## Endpoints

### GET /api/tasks

List all tasks for the authenticated user with optional filtering.

**Request**:
```http
GET /api/tasks?filter=all&sort=created_at&order=desc
Authorization: Bearer <token>
```

**Query Parameters**:
| Parameter | Type | Required | Values | Default | Description |
|-----------|------|----------|--------|---------|-------------|
| `filter` | string | ❌ No | `all`, `pending`, `completed` | `all` | Filter by completion status |
| `sort` | string | ❌ No | `created_at`, `updated_at`, `title` | `created_at` | Sort field |
| `order` | string | ❌ No | `asc`, `desc` | `desc` | Sort order |

**Success Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z"
    },
    {
      "id": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish homework",
      "description": null,
      "completed": true,
      "created_at": "2025-12-29T14:30:00Z",
      "updated_at": "2025-12-30T09:15:00Z"
    }
  ],
  "total": 2,
  "completed": 1,
  "pending": 1
}
```

**Response Schema** (TaskListResponse):
| Field | Type | Description |
|-------|------|-------------|
| `tasks` | array | List of task objects (see TaskResponse schema) |
| `total` | integer | Total number of tasks |
| `completed` | integer | Number of completed tasks |
| `pending` | integer | Number of pending tasks |

**TaskResponse Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Task ID (auto-increment) |
| `user_id` | string | Owner user ID (UUID) |
| `title` | string | Task title (1-200 characters) |
| `description` | string \| null | Task description (optional) |
| `completed` | boolean | Completion status |
| `created_at` | string | ISO 8601 creation timestamp |
| `updated_at` | string | ISO 8601 last update timestamp |

**Error Responses**:

```json
// 401 Unauthorized - Missing or invalid token
{
  "detail": "Invalid or expired token"
}

// 400 Bad Request - Invalid query parameter
{
  "detail": "Invalid filter value. Must be 'all', 'pending', or 'completed'"
}
```

**Status Codes**:
- `200 OK`: Tasks retrieved successfully (empty array if no tasks)
- `400 Bad Request`: Invalid query parameters
- `401 Unauthorized`: Missing or invalid JWT token

**Examples**:

```http
# Get all tasks (newest first)
GET /api/tasks

# Get only pending tasks
GET /api/tasks?filter=pending

# Get completed tasks sorted by title (A-Z)
GET /api/tasks?filter=completed&sort=title&order=asc
```

---

### GET /api/tasks/{id}

Get a specific task by ID.

**Request**:
```http
GET /api/tasks/1
Authorization: Bearer <token>
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Task ID |

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Response Schema**: TaskResponse (see above)

**Error Responses**:

```json
// 401 Unauthorized
{
  "detail": "Invalid or expired token"
}

// 403 Forbidden - Task belongs to different user
{
  "detail": "Access denied"
}

// 404 Not Found - Task doesn't exist
{
  "detail": "Task not found"
}
```

**Status Codes**:
- `200 OK`: Task retrieved successfully
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User doesn't own this task
- `404 Not Found`: Task ID doesn't exist

---

### POST /api/tasks

Create a new task.

**Request**:
```http
POST /api/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Request Schema** (TaskCreate):
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | ✅ Yes | 1-200 characters | Task title |
| `description` | string | ❌ No | No max length | Task description |

**Success Response (201 Created)**:
```json
{
  "id": 3,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-30T11:00:00Z",
  "updated_at": "2025-12-30T11:00:00Z"
}
```

**Response Schema**: TaskResponse (see above)

**Error Responses**:

```json
// 400 Bad Request - Missing title
{
  "detail": [
    {
      "field": "title",
      "message": "field required"
    }
  ]
}

// 400 Bad Request - Title too long
{
  "detail": [
    {
      "field": "title",
      "message": "ensure this value has at most 200 characters"
    }
  ]
}

// 400 Bad Request - Empty title
{
  "detail": "Title cannot be empty"
}

// 401 Unauthorized
{
  "detail": "Invalid or expired token"
}
```

**Status Codes**:
- `201 Created`: Task created successfully
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing or invalid JWT token

**Validation Rules**:
- `title`: Required, 1-200 characters (trimmed)
- `description`: Optional, any length (trimmed)
- `user_id`: Automatically set from JWT token
- `completed`: Automatically set to `false`
- `created_at`, `updated_at`: Automatically set to current timestamp

---

### PUT /api/tasks/{id}

Update an existing task (full update - all fields).

**Request**:
```http
PUT /api/tasks/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples",
  "completed": false
}
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Task ID to update |

**Request Schema** (TaskUpdate):
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | ❌ No | 1-200 characters | Task title |
| `description` | string \| null | ❌ No | No max length | Task description |
| `completed` | boolean | ❌ No | true/false | Completion status |

**Note**: All fields are optional. Only provided fields will be updated. `updated_at` timestamp automatically updated.

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples",
  "completed": false,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T11:30:00Z"
}
```

**Response Schema**: TaskResponse (see above)

**Error Responses**:

```json
// 400 Bad Request - Validation error
{
  "detail": "Title cannot be empty"
}

// 401 Unauthorized
{
  "detail": "Invalid or expired token"
}

// 403 Forbidden - Task belongs to different user
{
  "detail": "Access denied"
}

// 404 Not Found
{
  "detail": "Task not found"
}
```

**Status Codes**:
- `200 OK`: Task updated successfully
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User doesn't own this task
- `404 Not Found`: Task ID doesn't exist

---

### PATCH /api/tasks/{id}/complete

Toggle task completion status (convenience endpoint).

**Request**:
```http
PATCH /api/tasks/1/complete
Authorization: Bearer <token>
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Task ID to toggle |

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,  // Toggled from false to true
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Response Schema**: TaskResponse (see above)

**Behavior**:
- If task is pending (`completed: false`), mark as completed (`completed: true`)
- If task is completed (`completed: true`), mark as pending (`completed: false`)
- `updated_at` timestamp automatically updated

**Error Responses**: Same as PUT /api/tasks/{id}

**Status Codes**:
- `200 OK`: Completion status toggled successfully
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User doesn't own this task
- `404 Not Found`: Task ID doesn't exist

---

### DELETE /api/tasks/{id}

Delete a task permanently.

**Request**:
```http
DELETE /api/tasks/1
Authorization: Bearer <token>
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Task ID to delete |

**Success Response (204 No Content)**:
```http
HTTP/1.1 204 No Content
```

**No response body** - empty response with 204 status indicates successful deletion.

**Error Responses**:

```json
// 401 Unauthorized
{
  "detail": "Invalid or expired token"
}

// 403 Forbidden - Task belongs to different user
{
  "detail": "Access denied"
}

// 404 Not Found
{
  "detail": "Task not found"
}
```

**Status Codes**:
- `204 No Content`: Task deleted successfully
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User doesn't own this task
- `404 Not Found`: Task ID doesn't exist (or already deleted)

**Idempotency**: Deleting the same task twice returns `404 Not Found` on second attempt.

---

## User Isolation Enforcement

**Critical Security Requirement**: All task endpoints MUST filter by `user_id` from JWT token.

### Backend Implementation Pattern

```python
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.models import Task
from app.middleware.auth import get_current_user

@router.get("/tasks/{id}")
def get_task(
    id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Get task
    task = session.get(Task, id)

    # Check if task exists
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # CRITICAL: Verify user owns this task
    if task.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    return task
```

**Test Cases for User Isolation**:
1. ✅ User A can access User A's tasks → 200 OK
2. ❌ User A cannot access User B's tasks → 403 Forbidden
3. ❌ User A cannot update User B's tasks → 403 Forbidden
4. ❌ User A cannot delete User B's tasks → 403 Forbidden

---

## Error Response Format

All task endpoints follow consistent error format:

```typescript
interface APIError {
  detail: string | Array<{field: string, message: string}>
}
```

**Single Error**:
```json
{
  "detail": "Task not found"
}
```

**Validation Errors**:
```json
{
  "detail": [
    {"field": "title", "message": "field required"},
    {"field": "completed", "message": "value is not a valid boolean"}
  ]
}
```

---

## Frontend Integration

### API Client Example

```typescript
import { Task, TaskCreate, TaskUpdate, TaskListResponse } from '@/lib/types';

class TasksAPI {
  private baseURL = process.env.NEXT_PUBLIC_API_URL;

  private async request(endpoint: string, options: RequestInit = {}) {
    const token = localStorage.getItem('access_token');

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.status === 204 ? null : response.json();
  }

  async listTasks(filter: 'all' | 'pending' | 'completed' = 'all'): Promise<TaskListResponse> {
    return this.request(`/api/tasks?filter=${filter}`);
  }

  async getTask(id: number): Promise<Task> {
    return this.request(`/api/tasks/${id}`);
  }

  async createTask(data: TaskCreate): Promise<Task> {
    return this.request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateTask(id: number, data: TaskUpdate): Promise<Task> {
    return this.request(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async toggleComplete(id: number): Promise<Task> {
    return this.request(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }

  async deleteTask(id: number): Promise<void> {
    return this.request(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  }
}

export const tasksAPI = new TasksAPI();
```

---

## Testing

### List Tasks Test Cases

1. ✅ No tasks → 200 with empty array
2. ✅ Multiple tasks → 200 with tasks array
3. ✅ Filter by pending → 200 with only pending tasks
4. ✅ Filter by completed → 200 with only completed tasks
5. ✅ Sort by title ascending → 200 with sorted tasks
6. ❌ Invalid filter value → 400 validation error
7. ❌ Missing token → 401 unauthorized
8. ❌ Invalid token → 401 unauthorized

### Get Task Test Cases

1. ✅ Valid task ID owned by user → 200 with task
2. ❌ Task ID doesn't exist → 404 not found
3. ❌ Task ID belongs to different user → 403 forbidden
4. ❌ Missing token → 401 unauthorized
5. ❌ Invalid token → 401 unauthorized

### Create Task Test Cases

1. ✅ Valid task with title and description → 201 created
2. ✅ Valid task with title only → 201 created (description=null)
3. ❌ Missing title → 400 validation error
4. ❌ Empty title → 400 validation error
5. ❌ Title too long (>200 chars) → 400 validation error
6. ❌ Missing token → 401 unauthorized

### Update Task Test Cases

1. ✅ Update title only → 200 updated
2. ✅ Update description only → 200 updated
3. ✅ Update completed only → 200 updated
4. ✅ Update all fields → 200 updated
5. ❌ Empty title → 400 validation error
6. ❌ Task doesn't exist → 404 not found
7. ❌ Task belongs to different user → 403 forbidden
8. ❌ Missing token → 401 unauthorized

### Toggle Complete Test Cases

1. ✅ Pending task → 200 with completed=true
2. ✅ Completed task → 200 with completed=false
3. ❌ Task doesn't exist → 404 not found
4. ❌ Task belongs to different user → 403 forbidden
5. ❌ Missing token → 401 unauthorized

### Delete Task Test Cases

1. ✅ Valid task ID owned by user → 204 no content
2. ❌ Task doesn't exist → 404 not found
3. ❌ Task already deleted → 404 not found (idempotent)
4. ❌ Task belongs to different user → 403 forbidden
5. ❌ Missing token → 401 unauthorized

---

**Contract Status**: ✅ FINAL
**Last Updated**: 2025-12-30
**Version**: 1.0.0
