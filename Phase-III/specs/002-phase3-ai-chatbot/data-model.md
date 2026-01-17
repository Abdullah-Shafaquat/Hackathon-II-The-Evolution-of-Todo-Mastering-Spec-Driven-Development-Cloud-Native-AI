# Data Model: Phase III AI Chatbot

**Version**: 1.0.0
**Database**: Neon Serverless PostgreSQL
**ORM**: SQLModel
**Extends**: Phase II schema (users, tasks)

## Overview

Phase III adds two new tables for chat functionality:
1. **conversations** - Chat sessions between users and AI
2. **messages** - Individual messages within conversations

All new tables follow Phase II patterns: user isolation, timestamps, SQLModel compatibility.

---

## Schema Diagram

```
┌──────────────────┐
│      users       │ (Phase II - existing)
├──────────────────┤
│ id (PK)          │───┐
│ email            │   │
│ name             │   │
│ password_hash    │   │
│ created_at       │   │
│ updated_at       │   │
└──────────────────┘   │
                       │
                       │ 1:N
                       │
         ┌─────────────┴──────────────┐
         │                            │
         ▼                            ▼
┌──────────────────┐         ┌──────────────────┐
│      tasks       │         │  conversations   │ (Phase III - new)
├──────────────────┤         ├──────────────────┤
│ id (PK)          │         │ id (PK, UUID)    │───┐
│ user_id (FK)     │         │ user_id (FK)     │   │
│ title            │         │ created_at       │   │
│ description      │         │ updated_at       │   │ 1:N
│ completed        │         └──────────────────┘   │
│ created_at       │                                │
│ updated_at       │                                ▼
└──────────────────┘                        ┌──────────────────┐
                                            │     messages     │ (Phase III - new)
                                            ├──────────────────┤
                                            │ id (PK)          │
                                            │ user_id (FK)     │
                                            │ conversation_id  │
                                            │ role             │
                                            │ content          │
                                            │ created_at       │
                                            └──────────────────┘
```

---

## Table Definitions

### 1. conversations

Represents a chat session between a user and the AI assistant.

**Table Name**: `conversations`

**Columns**:

| Column       | Type        | Constraints                  | Description                        |
|--------------|-------------|------------------------------|------------------------------------|
| id           | UUID        | PRIMARY KEY                  | Unique conversation identifier     |
| user_id      | VARCHAR(255)| FOREIGN KEY → users.id, NOT NULL, INDEX | Owner of the conversation     |
| created_at   | TIMESTAMP   | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Conversation start time       |
| updated_at   | TIMESTAMP   | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last message timestamp        |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for fast filtering by user)
- INDEX on `(user_id, updated_at DESC)` (for listing recent conversations)

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions.

    Each conversation belongs to exactly one user.
    All queries MUST filter by user_id for data isolation.
    """
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Business Rules**:
1. Conversations belong to exactly one user (user_id)
2. Deleting a user cascades to delete all their conversations
3. updated_at timestamp updated whenever new message is added
4. Conversations are never shared between users

---

### 2. messages

Represents individual messages within a conversation (user or assistant).

**Table Name**: `messages`

**Columns**:

| Column          | Type        | Constraints                           | Description                           |
|-----------------|-------------|---------------------------------------|---------------------------------------|
| id              | INTEGER     | PRIMARY KEY, AUTO_INCREMENT           | Unique message identifier             |
| user_id         | VARCHAR(255)| FOREIGN KEY → users.id, NOT NULL, INDEX | Owner of the conversation (denormalized) |
| conversation_id | UUID        | FOREIGN KEY → conversations.id, NOT NULL, INDEX | Parent conversation            |
| role            | VARCHAR(50) | NOT NULL, CHECK (role IN ('user', 'assistant')) | Message sender              |
| content         | TEXT        | NOT NULL                              | Message text content                  |
| created_at      | TIMESTAMP   | NOT NULL, DEFAULT CURRENT_TIMESTAMP   | Message timestamp                     |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `conversation_id` (for loading conversation history)
- INDEX on `(conversation_id, created_at ASC)` (for ordered message retrieval)
- INDEX on `user_id` (for user-level filtering)

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- `conversation_id` REFERENCES `conversations(id)` ON DELETE CASCADE

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

class Message(SQLModel, table=True):
    """Message model for chat messages.

    Each message belongs to a conversation and has a role (user or assistant).
    user_id is denormalized for efficient filtering and cascade deletion.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", index=True)
    role: Literal["user", "assistant"] = Field(max_length=50)
    content: str = Field(min_length=1, max_length=50000)  # Max ~50K chars
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Business Rules**:
1. Messages belong to exactly one conversation
2. Role must be either "user" or "assistant"
3. Messages are append-only (no editing after creation)
4. Deleting a conversation cascades to delete all its messages
5. Deleting a user cascades to delete all their messages
6. Messages ordered by created_at within conversation

---

## Database Migration (SQL)

### Create Tables

```sql
-- Phase III: Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for filtering conversations by user
CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Index for listing recent conversations
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

-- Phase III: Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    conversation_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- Index for loading conversation history
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);

-- Index for ordered message retrieval
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);

-- Index for user-level filtering
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

### Rollback (Drop Tables)

```sql
-- Rollback Phase III changes
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
```

---

## Pydantic Schemas (Request/Response)

### ConversationCreate

```python
from pydantic import BaseModel

class ConversationCreate(BaseModel):
    """Schema for creating a new conversation.

    user_id is injected from auth context, not from request.
    """
    pass  # No client-provided fields; user_id from JWT
```

### MessageCreate

```python
from pydantic import BaseModel, Field
from typing import Optional
import uuid

class MessageCreate(BaseModel):
    """Schema for sending a chat message."""
    conversation_id: Optional[uuid.UUID] = Field(None, description="Existing conversation ID (omit for new)")
    message: str = Field(..., min_length=1, max_length=5000, description="User message content")
```

### MessageResponse

```python
from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    """Schema for individual message in response."""
    id: int
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
```

### ConversationResponse

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List
import uuid

class ConversationResponse(BaseModel):
    """Schema for conversation with messages."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]

    class Config:
        from_attributes = True
```

### ChatResponse

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
import uuid

class ChatResponse(BaseModel):
    """Schema for chat API response."""
    conversation_id: uuid.UUID
    response: str
    tool_calls: List[Dict[str, Any]]
    created_at: datetime
```

---

## TypeScript Interfaces (Frontend)

### Conversation

```typescript
interface Conversation {
  id: string;  // UUID
  created_at: string;  // ISO 8601
  updated_at: string;
  message_count?: number;
  last_message?: string;
}
```

### Message

```typescript
interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;  // ISO 8601
}
```

### ChatRequest

```typescript
interface ChatRequest {
  conversation_id?: string;  // UUID, optional for new conversation
  message: string;
}
```

### ChatResponse

```typescript
interface ToolCall {
  tool: string;
  arguments: Record<string, any>;
  result: {
    success: boolean;
    [key: string]: any;
  };
}

interface ChatResponse {
  conversation_id: string;  // UUID
  response: string;
  tool_calls: ToolCall[];
  created_at: string;  // ISO 8601
}
```

---

## Query Patterns

### Create Conversation and First Message

```python
from sqlmodel import Session
from app.models import Conversation, Message
import uuid

def create_conversation_with_message(
    user_id: str,
    message_content: str,
    session: Session
) -> tuple[Conversation, Message]:
    # Create conversation
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.flush()  # Get conversation.id

    # Create first message
    message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=message_content
    )
    session.add(message)
    session.commit()
    session.refresh(conversation)
    session.refresh(message)

    return conversation, message
```

### Load Conversation History

```python
from sqlmodel import Session, select
from app.models import Message
import uuid

def get_conversation_messages(
    conversation_id: uuid.UUID,
    user_id: str,
    session: Session,
    limit: int = 50
) -> List[Message]:
    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.user_id == user_id)  # Security: verify ownership
        .order_by(Message.created_at.asc())
        .limit(limit)
    )
    return session.exec(query).all()
```

### List User Conversations

```python
from sqlmodel import Session, select
from app.models import Conversation

def list_user_conversations(
    user_id: str,
    session: Session,
    limit: int = 20
) -> List[Conversation]:
    query = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    return session.exec(query).all()
```

### Delete Conversation (Cascade to Messages)

```python
from sqlmodel import Session
from app.models import Conversation
import uuid

def delete_conversation(
    conversation_id: uuid.UUID,
    user_id: str,
    session: Session
) -> bool:
    conversation = session.get(Conversation, conversation_id)

    if not conversation:
        return False

    # Verify ownership
    if conversation.user_id != user_id:
        raise PermissionError("Access denied")

    session.delete(conversation)  # Messages cascade delete
    session.commit()
    return True
```

---

## Data Validation Rules

### Conversations

1. **id**: Valid UUID format (auto-generated)
2. **user_id**: Must exist in users table
3. **created_at/updated_at**: Automatic timestamps, not client-provided

### Messages

1. **conversation_id**: Must exist in conversations table and belong to user
2. **role**: Must be exactly "user" or "assistant"
3. **content**: Required, 1-50,000 characters
4. **user_id**: Must match conversation owner

---

## Performance Considerations

### Indexing Strategy

1. **conversations.user_id**: Fast filtering by user
2. **messages.conversation_id**: Fast message loading
3. **messages.(conversation_id, created_at)**: Ordered retrieval

### Query Optimization

1. Limit message history to recent N messages (e.g., 50)
2. Paginate conversation lists
3. Use connection pooling for concurrent requests
4. Consider read replicas for heavy read workloads

### Storage Estimates

- **Conversation**: ~100 bytes per row
- **Message**: ~500 bytes average per row (depends on content length)
- **100 users, 10 conversations each, 50 messages per conversation**: ~2.5 MB

---

## Testing Checklist

### Schema Tests

- [ ] Conversations table created with correct columns
- [ ] Messages table created with correct columns
- [ ] Foreign keys enforce referential integrity
- [ ] Cascade delete works (user → conversations → messages)
- [ ] Indexes improve query performance
- [ ] Role CHECK constraint enforces valid values

### Model Tests

- [ ] Conversation model creates with auto-generated UUID
- [ ] Message model validates role enum
- [ ] Timestamps auto-populate on creation
- [ ] Foreign key validation prevents orphaned records

### Query Tests

- [ ] List conversations filters by user_id
- [ ] Load messages filters by user_id and conversation_id
- [ ] Messages returned in chronological order
- [ ] Pagination works correctly
- [ ] Deleting conversation cascades to messages

---

**Last Updated**: 2026-01-04
**Status**: Ready for Implementation
