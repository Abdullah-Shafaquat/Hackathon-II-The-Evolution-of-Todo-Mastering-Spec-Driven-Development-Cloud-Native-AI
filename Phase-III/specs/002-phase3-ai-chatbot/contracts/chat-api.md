# Chat API Contract

**Version**: 1.0.0
**Base URL**: `{BACKEND_URL}/api`
**Authentication**: JWT Bearer Token (required for all endpoints)

## Overview

The Chat API provides a stateless conversational interface for task management. All endpoints require JWT authentication and maintain conversation state in the database (not server memory).

---

## Endpoints

### 1. Send Chat Message

Creates a new message in a conversation and returns AI-generated response.

**Endpoint**: `POST /api/{user_id}/chat`

**Authentication**: Required (JWT token in `Authorization: Bearer {token}`)

**Path Parameters**:
- `user_id` (string, required): Authenticated user's ID (must match JWT token user_id)

**Request Body**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",  // Optional UUID, omit for new conversation
  "message": "Add a task to buy groceries"                     // Required, 1-5000 characters
}
```

**Response (200 OK)**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "I've added 'Buy groceries' to your tasks.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "title": "Buy groceries",
        "description": null
      },
      "result": {
        "success": true,
        "task_id": 42
      }
    }
  ],
  "created_at": "2026-01-04T10:30:00Z"
}
```

**Response Fields**:
- `conversation_id` (string): UUID of the conversation (new or existing)
- `response` (string): AI-generated natural language response
- `tool_calls` (array): List of MCP tools invoked by AI agent
  - `tool` (string): Name of the tool called
  - `arguments` (object): Parameters passed to the tool
  - `result` (object): Tool execution result
- `created_at` (string): ISO 8601 timestamp of response

**Error Responses**:

**400 Bad Request** - Invalid request format
```json
{
  "detail": "Message is required and must be 1-5000 characters"
}
```

**401 Unauthorized** - Missing or invalid JWT token
```json
{
  "detail": "Invalid authentication credentials"
}
```

**403 Forbidden** - Conversation belongs to different user
```json
{
  "detail": "Access denied. This conversation belongs to another user"
}
```

**404 Not Found** - Conversation ID not found
```json
{
  "detail": "Conversation with id 550e8400-e29b-41d4-a716-446655440000 not found"
}
```

**500 Internal Server Error** - OpenAI API error or server error
```json
{
  "detail": "I'm temporarily unavailable. Please try again in a moment"
}
```

**503 Service Unavailable** - OpenAI API rate limit
```json
{
  "detail": "Service is busy. Please try again in a few seconds",
  "retry_after": 5
}
```

---

### 2. Get Conversation History

Retrieves all messages in a conversation.

**Endpoint**: `GET /api/{user_id}/conversations/{conversation_id}`

**Authentication**: Required

**Path Parameters**:
- `user_id` (string, required): Authenticated user's ID
- `conversation_id` (string, required): UUID of the conversation

**Query Parameters**:
- `limit` (integer, optional): Max messages to return (default: 50, max: 100)
- `offset` (integer, optional): Number of messages to skip (default: 0)

**Response (200 OK)**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2026-01-04T10:30:00Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "I've added 'Buy groceries' to your tasks.",
      "created_at": "2026-01-04T10:30:02Z"
    }
  ],
  "total": 2,
  "has_more": false
}
```

**Error Responses**: Same as Send Chat Message (401, 403, 404)

---

### 3. List User Conversations

Retrieves all conversations for the authenticated user.

**Endpoint**: `GET /api/{user_id}/conversations`

**Authentication**: Required

**Path Parameters**:
- `user_id` (string, required): Authenticated user's ID

**Query Parameters**:
- `limit` (integer, optional): Max conversations to return (default: 20, max: 50)
- `offset` (integer, optional): Number of conversations to skip (default: 0)

**Response (200 OK)**:
```json
{
  "conversations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "created_at": "2026-01-04T10:30:00Z",
      "updated_at": "2026-01-04T10:35:00Z",
      "message_count": 12,
      "last_message": "I've marked task 3 as complete."
    },
    {
      "id": "660f9511-f3ac-52e5-b827-557766551111",
      "created_at": "2026-01-03T14:20:00Z",
      "updated_at": "2026-01-03T14:25:00Z",
      "message_count": 6,
      "last_message": "You have 5 pending tasks."
    }
  ],
  "total": 2,
  "has_more": false
}
```

**Error Responses**: 401 Unauthorized

---

### 4. Delete Conversation

Deletes a conversation and all its messages.

**Endpoint**: `DELETE /api/{user_id}/conversations/{conversation_id}`

**Authentication**: Required

**Path Parameters**:
- `user_id` (string, required): Authenticated user's ID
- `conversation_id` (string, required): UUID of the conversation

**Response (204 No Content)**: Empty body on success

**Error Responses**: 401, 403, 404

---

## Request/Response Examples

### Example 1: Create Task with New Conversation

**Request**:
```bash
POST /api/user123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "I need to remember to call mom tonight"
}
```

**Response**:
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "response": "Got it! I've created a task to call mom tonight for you.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "title": "Call mom tonight",
        "description": null
      },
      "result": {
        "success": true,
        "task_id": 15
      }
    }
  ],
  "created_at": "2026-01-04T10:30:00Z"
}
```

---

### Example 2: List Tasks in Existing Conversation

**Request**:
```bash
POST /api/user123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Show me all my tasks"
}
```

**Response**:
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "response": "You have 3 tasks:\n1. Buy groceries (pending)\n2. Call mom tonight (pending)\n3. Finish project report (completed)",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "arguments": {
        "filter": "all"
      },
      "result": {
        "success": true,
        "tasks": [
          {"id": 14, "title": "Buy groceries", "completed": false},
          {"id": 15, "title": "Call mom tonight", "completed": false},
          {"id": 16, "title": "Finish project report", "completed": true}
        ],
        "total": 3,
        "completed": 1,
        "pending": 2
      }
    }
  ],
  "created_at": "2026-01-04T10:32:00Z"
}
```

---

### Example 3: Mark Task Complete

**Request**:
```bash
POST /api/user123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Mark task 14 as complete"
}
```

**Response**:
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "response": "Done! I've marked task 14 as complete.",
  "tool_calls": [
    {
      "tool": "complete_task",
      "arguments": {
        "task_id": 14
      },
      "result": {
        "success": true,
        "task": {
          "id": 14,
          "title": "Buy groceries",
          "completed": true
        }
      }
    }
  ],
  "created_at": "2026-01-04T10:33:00Z"
}
```

---

### Example 4: Error - Task Not Found

**Request**:
```bash
POST /api/user123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Delete task 999"
}
```

**Response**:
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "response": "I couldn't find task 999. Try 'show my tasks' to see all your tasks.",
  "tool_calls": [
    {
      "tool": "delete_task",
      "arguments": {
        "task_id": 999
      },
      "result": {
        "success": false,
        "error": "Task with id 999 not found"
      }
    }
  ],
  "created_at": "2026-01-04T10:34:00Z"
}
```

---

## Validation Rules

### Request Validation

1. **message**: Required, string, 1-5000 characters
2. **conversation_id**: Optional, valid UUID format
3. **user_id** (path param): Must match JWT token user_id
4. **Authorization header**: Required, format `Bearer {token}`

### Response Guarantees

1. All timestamps in ISO 8601 format (UTC)
2. Conversation IDs are always valid UUIDs
3. Tool calls array may be empty if no tools invoked
4. Response message is always present and non-empty

---

## Rate Limiting

- **Chat endpoint**: 30 requests per minute per user
- **List conversations**: 60 requests per minute per user
- **Get conversation history**: 60 requests per minute per user

Exceeded rate limit returns 429 Too Many Requests:
```json
{
  "detail": "Rate limit exceeded. Try again in 30 seconds",
  "retry_after": 30
}
```

---

## WebSocket Support (Future)

Currently NOT supported. All communication is HTTP-based (request/response).

Future versions may add:
- `ws://api/ws/{user_id}/chat` - Real-time bidirectional chat
- Server-sent events for streaming responses

---

## Testing Checklist

- [ ] Create task via natural language
- [ ] List tasks with different filters
- [ ] Mark task complete
- [ ] Update task details
- [ ] Delete task
- [ ] Handle non-existent task gracefully
- [ ] Create new conversation (omit conversation_id)
- [ ] Continue existing conversation
- [ ] Prevent access to other user's conversation (403)
- [ ] Handle malformed conversation_id (400)
- [ ] Handle OpenAI API errors (500/503)
- [ ] Verify JWT authentication requirement (401)
- [ ] Test conversation persistence across multiple requests
- [ ] Verify tool_calls populated correctly
- [ ] Test message validation (empty, too long)

---

**Last Updated**: 2026-01-04
**Status**: Ready for Implementation
