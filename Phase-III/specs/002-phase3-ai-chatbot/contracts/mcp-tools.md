# MCP Tools Specification

**Version**: 1.0.0
**MCP SDK**: Official Python MCP SDK
**Integration**: FastAPI Backend

## Overview

MCP (Model Context Protocol) tools expose task operations as callable functions for the OpenAI Agents SDK. All tools are stateless, store data in the database, and validate user authentication.

---

## Tool Architecture

### Design Principles

1. **Stateless**: No server memory state; all state in database
2. **Authenticated**: Receive user_id from auth context (not client input)
3. **Database-Direct**: Query/modify tasks table directly (not via HTTP routes)
4. **Structured Returns**: Return success/error with typed data
5. **Idempotent**: Safe to retry (where applicable)

### Authentication Flow

```
OpenAI Agent → MCP Tool Call → Extract user_id from context → Database Query with user_id filter → Return result
```

**Critical**: user_id MUST come from authenticated session, never from tool parameters.

---

## Tool Definitions

### 1. add_task

Creates a new task for the authenticated user.

**Tool Name**: `add_task`

**Description**: "Create a new todo task with a title and optional description"

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Task title (1-200 characters)",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "description": "Optional task description",
      "nullable": true
    }
  },
  "required": ["title"]
}
```

**Returns**:
```json
{
  "success": true,
  "task_id": 42,
  "task": {
    "id": 42,
    "title": "Buy groceries",
    "description": null,
    "completed": false,
    "created_at": "2026-01-04T10:30:00Z"
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Title must be 1-200 characters"
}
```

**Implementation Notes**:
- Extract user_id from auth context
- Create Task model instance with user_id
- Set completed=False, timestamps auto-generated
- Commit to database, return task_id

---

### 2. list_tasks

Retrieves tasks for the authenticated user with optional filtering.

**Tool Name**: `list_tasks`

**Description**: "List all tasks for the user, optionally filtered by completion status"

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "filter": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "description": "Filter tasks by status",
      "default": "all"
    }
  },
  "required": []
}
```

**Returns**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": 42,
      "title": "Buy groceries",
      "description": null,
      "completed": false,
      "created_at": "2026-01-04T10:30:00Z"
    },
    {
      "id": 43,
      "title": "Call mom",
      "description": "Birthday wishes",
      "completed": true,
      "created_at": "2026-01-03T14:20:00Z"
    }
  ],
  "total": 2,
  "completed": 1,
  "pending": 1
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Invalid filter value. Use 'all', 'pending', or 'completed'"
}
```

**Implementation Notes**:
- Extract user_id from auth context
- Query: `SELECT * FROM tasks WHERE user_id = ? [AND completed = ?] ORDER BY created_at DESC`
- Calculate statistics from all user's tasks (not filtered subset)
- Return tasks array + statistics

---

### 3. complete_task

Marks a task as complete (or toggles completion status).

**Tool Name**: `complete_task`

**Description**: "Mark a task as complete by its ID"

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "ID of the task to mark complete"
    }
  },
  "required": ["task_id"]
}
```

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": 42,
    "title": "Buy groceries",
    "completed": true,
    "updated_at": "2026-01-04T10:35:00Z"
  }
}
```

**Error Response - Task Not Found**:
```json
{
  "success": false,
  "error": "Task with id 42 not found"
}
```

**Error Response - Access Denied** (task belongs to different user):
```json
{
  "success": false,
  "error": "Access denied. This task belongs to another user"
}
```

**Implementation Notes**:
- Extract user_id from auth context
- Query task by ID
- Verify task.user_id == authenticated user_id
- Set completed=True, update updated_at timestamp
- Commit and return updated task

**Alternative**: Could toggle completion (if completed, mark incomplete)

---

### 4. delete_task

Removes a task from the database.

**Tool Name**: `delete_task`

**Description**: "Delete a task by its ID"

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "ID of the task to delete"
    }
  },
  "required": ["task_id"]
}
```

**Returns**:
```json
{
  "success": true,
  "message": "Task 42 deleted successfully"
}
```

**Error Response - Task Not Found**:
```json
{
  "success": false,
  "error": "Task with id 42 not found"
}
```

**Error Response - Access Denied**:
```json
{
  "success": false,
  "error": "Access denied. This task belongs to another user"
}
```

**Implementation Notes**:
- Extract user_id from auth context
- Query task by ID
- Verify task.user_id == authenticated user_id
- Delete from database
- Return success confirmation

**Warning**: Irreversible operation. Consider soft delete in production.

---

### 5. update_task

Updates task title, description, or completion status.

**Tool Name**: `update_task`

**Description**: "Update a task's title, description, or completion status"

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "ID of the task to update"
    },
    "title": {
      "type": "string",
      "description": "New task title (1-200 characters)",
      "minLength": 1,
      "maxLength": 200,
      "nullable": true
    },
    "description": {
      "type": "string",
      "description": "New task description",
      "nullable": true
    },
    "completed": {
      "type": "boolean",
      "description": "New completion status",
      "nullable": true
    }
  },
  "required": ["task_id"]
}
```

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": 42,
    "title": "Buy groceries and snacks",
    "description": "Milk, eggs, bread, chips",
    "completed": false,
    "updated_at": "2026-01-04T10:40:00Z"
  }
}
```

**Error Response - Task Not Found**:
```json
{
  "success": false,
  "error": "Task with id 42 not found"
}
```

**Error Response - No Fields Provided**:
```json
{
  "success": false,
  "error": "At least one field (title, description, or completed) must be provided"
}
```

**Error Response - Access Denied**:
```json
{
  "success": false,
  "error": "Access denied. This task belongs to another user"
}
```

**Implementation Notes**:
- Extract user_id from auth context
- Query task by ID
- Verify task.user_id == authenticated user_id
- Update only provided fields (null/undefined fields ignored)
- Update updated_at timestamp
- Commit and return updated task

---

## MCP Server Configuration

### Server Metadata

```json
{
  "name": "todo-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for todo task management operations",
  "tools": [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task"
  ]
}
```

### Integration with OpenAI Agents SDK

```python
# Pseudo-code for agent configuration
agent = Agent(
    name="Todo Assistant",
    model="gpt-4",
    instructions="You are a helpful todo management assistant...",
    tools=[
        add_task,
        list_tasks,
        complete_task,
        delete_task,
        update_task
    ]
)
```

---

## Context Injection

### User Authentication Context

MCP tools receive user context from FastAPI dependency injection:

```python
from app.middleware.auth import get_current_user

def add_task(title: str, description: Optional[str], user_id: str):
    # user_id injected from auth middleware, not from parameters
    task = Task(user_id=user_id, title=title, description=description)
    # ... rest of implementation
```

**Critical Security Rule**: user_id is NEVER accepted as a tool parameter. It is always extracted from the authenticated session context.

---

## Error Handling

### Error Categories

1. **Validation Errors** (400-level)
   - Invalid parameters (empty title, invalid filter)
   - Missing required fields

2. **Authorization Errors** (403-level)
   - Task belongs to different user
   - Access denied

3. **Not Found Errors** (404-level)
   - Task ID does not exist

4. **Database Errors** (500-level)
   - Connection failures
   - Transaction rollback errors

### Error Response Format

All errors return structured JSON:
```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "TASK_NOT_FOUND",  // Optional machine-readable code
  "details": {}  // Optional additional context
}
```

---

## Testing Checklist

### Unit Tests (per tool)

**add_task**:
- [ ] Creates task with title only
- [ ] Creates task with title and description
- [ ] Rejects empty title
- [ ] Rejects title > 200 characters
- [ ] Associates task with correct user_id

**list_tasks**:
- [ ] Returns all tasks when filter="all"
- [ ] Returns only pending tasks when filter="pending"
- [ ] Returns only completed tasks when filter="completed"
- [ ] Returns empty array for user with no tasks
- [ ] Calculates statistics correctly
- [ ] Filters by authenticated user_id only

**complete_task**:
- [ ] Marks task as complete
- [ ] Returns 404 for non-existent task_id
- [ ] Returns 403 for task belonging to different user
- [ ] Updates updated_at timestamp

**delete_task**:
- [ ] Deletes task successfully
- [ ] Returns 404 for non-existent task_id
- [ ] Returns 403 for task belonging to different user
- [ ] Does not affect other users' tasks

**update_task**:
- [ ] Updates title only
- [ ] Updates description only
- [ ] Updates completed status only
- [ ] Updates multiple fields simultaneously
- [ ] Returns 400 when no fields provided
- [ ] Returns 404 for non-existent task_id
- [ ] Returns 403 for task belonging to different user

### Integration Tests

- [ ] Tools integrate with OpenAI Agents SDK
- [ ] Auth context injection works correctly
- [ ] Database transactions commit properly
- [ ] Concurrent tool calls handle correctly (no race conditions)

---

## Implementation Guidelines

### File Structure

```
backend/
├── app/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py          # MCP server setup
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── complete_task.py
│   │   │   ├── delete_task.py
│   │   │   └── update_task.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── tool_responses.py  # Response type definitions
```

### Code Standards

1. **Type Hints**: All functions must have complete type annotations
2. **Docstrings**: Each tool function must have detailed docstring
3. **Error Handling**: Use try/except with specific exceptions
4. **Logging**: Log all tool invocations with user_id (for auditing)
5. **Validation**: Use Pydantic models for parameter validation

---

## OpenAI Agents SDK Integration

### Agent Instructions

```
You are a helpful todo management assistant. You can help users:
- Create new tasks
- View all tasks or filter by status
- Mark tasks as complete
- Update task details
- Delete tasks

When users ask to create a task, extract the task title from their message.
Be conversational and friendly. Confirm actions clearly.
If a user's request is ambiguous, ask clarifying questions.
```

### Tool Usage Examples

**User**: "Add a task to buy groceries"
**Agent**: Calls `add_task(title="Buy groceries")`
**Response**: "I've added 'Buy groceries' to your tasks."

**User**: "Show me all my tasks"
**Agent**: Calls `list_tasks(filter="all")`
**Response**: "You have 3 tasks: [lists tasks]"

**User**: "Mark task 5 as done"
**Agent**: Calls `complete_task(task_id=5)`
**Response**: "Done! I've marked task 5 as complete."

---

**Last Updated**: 2026-01-04
**Status**: Ready for Implementation
