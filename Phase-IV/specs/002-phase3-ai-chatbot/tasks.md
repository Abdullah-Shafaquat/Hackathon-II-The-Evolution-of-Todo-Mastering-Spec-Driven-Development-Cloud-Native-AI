# Implementation Tasks: Phase III AI Chatbot

**Feature**: `002-phase3-ai-chatbot`
**Generated**: 2026-01-04
**Source**: [plan.md](./plan.md), [spec.md](./spec.md)

## Task Summary

**Total Tasks**: 38
**Estimated Effort**: 3-5 days (full-time development)

**Task Categories**:
- Environment Setup: 3 tasks
- Database Schema: 4 tasks
- Backend Models & Schemas: 4 tasks
- MCP Server & Tools: 9 tasks
- Chat API Endpoint: 5 tasks
- Frontend ChatKit: 8 tasks
- Integration & Testing: 3 tasks
- Documentation & Deployment: 2 tasks

---

## Phase 1: Environment Setup (3 tasks)

### Task 1.1: Configure OpenAI API Key

**Priority**: P0 (Blocker)
**Estimated Time**: 15 minutes
**Dependencies**: None

**Description**: Add OpenAI API key to backend environment configuration.

**Files to Modify**:
- `backend/.env.example`
- `backend/.env` (local only, not committed)
- `backend/app/config.py`

**Acceptance Criteria**:
- [ ] OPENAI_API_KEY added to .env.example with placeholder
- [ ] OPENAI_API_KEY loaded in Settings class (config.py:11-43)
- [ ] OPENAI_MODEL setting added (default: "gpt-4")
- [ ] MAX_CONVERSATION_MESSAGES setting added (default: 50)
- [ ] Backend starts without errors when OPENAI_API_KEY is set
- [ ] Settings.OPENAI_API_KEY accessible in application

**Implementation Notes**:
```python
# backend/app/config.py
class Settings(BaseSettings):
    # Existing settings...

    # NEW: Phase III - OpenAI Configuration
    OPENAI_API_KEY: str  # Required
    OPENAI_MODEL: str = "gpt-4"
    MAX_CONVERSATION_MESSAGES: int = 50
```

---

### Task 1.2: Install Backend Dependencies

**Priority**: P0 (Blocker)
**Estimated Time**: 10 minutes
**Dependencies**: None

**Description**: Install Python packages for MCP SDK and OpenAI Agents SDK.

**Files to Modify**:
- `backend/requirements.txt`

**Acceptance Criteria**:
- [ ] `mcp` package added to requirements.txt (official MCP SDK)
- [ ] `openai` package added (version 1.6.0+)
- [ ] `openai-agents-sdk` package added (version 0.2.0+)
- [ ] All packages install successfully: `pip install -r requirements.txt`
- [ ] No dependency conflicts

**Implementation Notes**:
```txt
# Add to backend/requirements.txt
mcp==0.1.0
openai==1.6.0
openai-agents-sdk==0.2.0
```

---

### Task 1.3: Install Frontend Dependencies

**Priority**: P0 (Blocker)
**Estimated Time**: 10 minutes
**Dependencies**: None

**Description**: Install OpenAI ChatKit for Next.js frontend.

**Files to Modify**:
- `frontend/package.json`

**Acceptance Criteria**:
- [ ] `@openai/chatkit` package added to package.json
- [ ] Package installs successfully: `npm install`
- [ ] No dependency conflicts
- [ ] TypeScript types available for ChatKit components

**Implementation Notes**:
```bash
cd frontend
npm install @openai/chatkit
```

---

## Phase 2: Database Schema (4 tasks)

### Task 2.1: Create Conversations Model

**Priority**: P0 (Blocker)
**Estimated Time**: 30 minutes
**Dependencies**: None

**Description**: Create SQLModel for conversations table.

**Files to Create**:
- `backend/app/models/conversation.py`

**Files to Modify**:
- `backend/app/models/__init__.py`

**Acceptance Criteria**:
- [ ] Conversation model defined with SQLModel (table=True)
- [ ] Fields: id (UUID, PK), user_id (FK to users.id), created_at, updated_at
- [ ] Foreign key to users table with CASCADE delete
- [ ] Indexes on user_id and (user_id, updated_at DESC)
- [ ] Model imported in models/__init__.py
- [ ] Type hints for all fields
- [ ] Docstring explaining purpose

**Implementation Notes**:
```python
# backend/app/models/conversation.py
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

**Reference**: [data-model.md](./data-model.md) lines 41-77

---

### Task 2.2: Create Messages Model

**Priority**: P0 (Blocker)
**Estimated Time**: 30 minutes
**Dependencies**: Task 2.1 (Conversations model)

**Description**: Create SQLModel for messages table.

**Files to Create**:
- `backend/app/models/message.py`

**Files to Modify**:
- `backend/app/models/__init__.py`

**Acceptance Criteria**:
- [ ] Message model defined with SQLModel (table=True)
- [ ] Fields: id (int, PK), user_id (FK), conversation_id (FK), role (Literal["user", "assistant"]), content (text), created_at
- [ ] Foreign keys to users and conversations with CASCADE delete
- [ ] Indexes on conversation_id and (conversation_id, created_at ASC)
- [ ] Role field uses Literal type for type safety
- [ ] Model imported in models/__init__.py
- [ ] Type hints for all fields
- [ ] Docstring explaining denormalized user_id

**Implementation Notes**:
```python
# backend/app/models/message.py
from sqlmodel import SQLModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

class Message(SQLModel, table=True):
    """Message model for chat messages.

    user_id is denormalized for efficient filtering and cascade deletion.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", index=True)
    role: Literal["user", "assistant"] = Field(max_length=50)
    content: str = Field(min_length=1, max_length=50000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Reference**: [data-model.md](./data-model.md) lines 81-127

---

### Task 2.3: Create Database Migration Script

**Priority**: P0 (Blocker)
**Estimated Time**: 45 minutes
**Dependencies**: Task 2.1, Task 2.2

**Description**: Create SQL migration to add conversations and messages tables.

**Files to Create**:
- `backend/migrations/003_add_conversations_messages.sql`
- `backend/scripts/migrate_phase3.py` (optional migration runner)

**Acceptance Criteria**:
- [ ] SQL script creates conversations table with correct schema
- [ ] SQL script creates messages table with correct schema
- [ ] All foreign keys defined with CASCADE delete
- [ ] All indexes created (user_id, conversation_id, composite indexes)
- [ ] CHECK constraint on messages.role (IN 'user', 'assistant')
- [ ] Migration script idempotent (CREATE TABLE IF NOT EXISTS)
- [ ] Rollback script included (DROP TABLE IF EXISTS)
- [ ] Test migration on local database successfully

**Implementation Notes**:
```sql
-- backend/migrations/003_add_conversations_messages.sql
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

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

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

**Reference**: [data-model.md](./data-model.md) lines 131-166

---

### Task 2.4: Run Database Migration

**Priority**: P0 (Blocker)
**Estimated Time**: 15 minutes
**Dependencies**: Task 2.3

**Description**: Execute migration to create tables in Neon database.

**Acceptance Criteria**:
- [ ] Connect to Neon database with DATABASE_URL
- [ ] Execute migration SQL successfully
- [ ] Verify conversations table exists: `\dt conversations`
- [ ] Verify messages table exists: `\dt messages`
- [ ] Verify all indexes created
- [ ] Verify foreign keys and constraints
- [ ] No errors in migration output

**Implementation Notes**:
```bash
# Option 1: Direct SQL execution
psql $DATABASE_URL < backend/migrations/003_add_conversations_messages.sql

# Option 2: Python migration runner (if created)
python backend/scripts/migrate_phase3.py
```

---

## Phase 3: Backend Models & Schemas (4 tasks)

### Task 3.1: Create Conversation Pydantic Schemas

**Priority**: P1
**Estimated Time**: 30 minutes
**Dependencies**: Task 2.1

**Description**: Create Pydantic schemas for conversation request/response.

**Files to Create**:
- `backend/app/schemas/conversation.py`

**Files to Modify**:
- `backend/app/schemas/__init__.py`

**Acceptance Criteria**:
- [ ] ConversationResponse schema with id, created_at, updated_at
- [ ] Schema uses Config.from_attributes = True for SQLModel conversion
- [ ] All fields have type hints
- [ ] Docstrings for each schema
- [ ] Schema imported in schemas/__init__.py

**Implementation Notes**:
```python
# backend/app/schemas/conversation.py
from pydantic import BaseModel
from datetime import datetime
import uuid

class ConversationResponse(BaseModel):
    """Schema for conversation response."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**Reference**: [data-model.md](./data-model.md) lines 202-212

---

### Task 3.2: Create Message Pydantic Schemas

**Priority**: P1
**Estimated Time**: 45 minutes
**Dependencies**: Task 2.2

**Description**: Create Pydantic schemas for message and chat request/response.

**Files to Create**:
- `backend/app/schemas/message.py`

**Files to Modify**:
- `backend/app/schemas/__init__.py`

**Acceptance Criteria**:
- [ ] MessageCreate schema with conversation_id (optional), message (required)
- [ ] MessageResponse schema with id, role, content, created_at
- [ ] ChatResponse schema with conversation_id, response, tool_calls, created_at
- [ ] Validation: message 1-5000 characters
- [ ] All schemas use proper type hints
- [ ] Config.from_attributes where needed
- [ ] Schemas imported in schemas/__init__.py

**Implementation Notes**:
```python
# backend/app/schemas/message.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

class MessageCreate(BaseModel):
    """Schema for sending a chat message."""
    conversation_id: Optional[uuid.UUID] = Field(None, description="Existing conversation ID")
    message: str = Field(..., min_length=1, max_length=5000, description="User message")

class MessageResponse(BaseModel):
    """Schema for individual message."""
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    """Schema for chat API response."""
    conversation_id: uuid.UUID
    response: str
    tool_calls: List[Dict[str, Any]]
    created_at: datetime
```

**Reference**: [data-model.md](./data-model.md) lines 168-234

---

### Task 3.3: Create TypeScript Interfaces

**Priority**: P1
**Estimated Time**: 30 minutes
**Dependencies**: Task 3.1, Task 3.2

**Description**: Create TypeScript interfaces matching backend schemas.

**Files to Create**:
- `frontend/lib/types/chat.ts`

**Acceptance Criteria**:
- [ ] Conversation interface with id (string/UUID), timestamps
- [ ] Message interface with id, role, content, created_at
- [ ] ChatRequest interface with conversation_id (optional), message
- [ ] ChatResponse interface with conversation_id, response, tool_calls, created_at
- [ ] ToolCall interface for tool execution results
- [ ] All fields properly typed
- [ ] Export all interfaces

**Implementation Notes**:
```typescript
// frontend/lib/types/chat.ts
export interface Conversation {
  id: string;  // UUID
  created_at: string;  // ISO 8601
  updated_at: string;
}

export interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface ChatRequest {
  conversation_id?: string;
  message: string;
}

export interface ToolCall {
  tool: string;
  arguments: Record<string, any>;
  result: {
    success: boolean;
    [key: string]: any;
  };
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
  created_at: string;
}
```

**Reference**: [data-model.md](./data-model.md) lines 236-266

---

### Task 3.4: Update Database Initialization

**Priority**: P1
**Estimated Time**: 15 minutes
**Dependencies**: Task 2.1, Task 2.2

**Description**: Ensure new models are imported for SQLModel metadata.

**Files to Modify**:
- `backend/app/database.py`
- `backend/app/main.py`

**Acceptance Criteria**:
- [ ] Conversation and Message models imported in database.py
- [ ] Models registered with SQLModel metadata
- [ ] Database connection includes new tables
- [ ] No errors on backend startup
- [ ] Tables appear in FastAPI docs metadata

**Implementation Notes**:
```python
# backend/app/database.py
from app.models import User, Task, Conversation, Message  # Add new imports
```

---

## Phase 4: MCP Server & Tools (9 tasks)

### Task 4.1: Create MCP Server Structure

**Priority**: P0 (Blocker)
**Estimated Time**: 30 minutes
**Dependencies**: Task 1.2 (MCP SDK installed)

**Description**: Set up MCP server directory structure and initialization.

**Files to Create**:
- `backend/app/mcp_server/__init__.py`
- `backend/app/mcp_server/server.py`
- `backend/app/mcp_server/tools/__init__.py`

**Acceptance Criteria**:
- [ ] MCP server directory created under app/
- [ ] server.py initializes MCP server with metadata
- [ ] Tools subdirectory for individual tool implementations
- [ ] Server exports tool registry
- [ ] No errors importing mcp package

**Implementation Notes**:
```python
# backend/app/mcp_server/server.py
from mcp import MCPServer

mcp_server = MCPServer(
    name="todo-mcp-server",
    version="1.0.0",
    description="MCP server for todo task management"
)

# Tool registry populated by individual tool modules
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 145-160

---

### Task 4.2: Implement add_task Tool

**Priority**: P0 (Blocker)
**Estimated Time**: 45 minutes
**Dependencies**: Task 4.1

**Description**: Create MCP tool for creating new tasks.

**Files to Create**:
- `backend/app/mcp_server/tools/add_task.py`

**Files to Modify**:
- `backend/app/mcp_server/tools/__init__.py`

**Acceptance Criteria**:
- [ ] Tool function accepts title (required), description (optional)
- [ ] user_id extracted from auth context (not parameters)
- [ ] Creates Task in database with user_id
- [ ] Returns structured response: {success, task_id, task}
- [ ] Validation: title 1-200 characters
- [ ] Error handling for validation failures
- [ ] Type hints for all parameters and return
- [ ] Docstring with parameter descriptions
- [ ] Tool registered with MCP server

**Implementation Notes**:
```python
# backend/app/mcp_server/tools/add_task.py
from typing import Optional, Dict, Any
from sqlmodel import Session
from app.models import Task
from app.database import get_session
from datetime import datetime

def add_task(
    title: str,
    description: Optional[str] = None,
    user_id: str = None,  # Injected from auth context
    session: Session = None  # Injected dependency
) -> Dict[str, Any]:
    """Create a new todo task.

    Args:
        title: Task title (1-200 characters)
        description: Optional task description
        user_id: Authenticated user ID (injected)
        session: Database session (injected)

    Returns:
        {success: bool, task_id: int, task: dict}
    """
    try:
        if not title or len(title) > 200:
            return {"success": False, "error": "Title must be 1-200 characters"}

        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 25-74

---

### Task 4.3: Implement list_tasks Tool

**Priority**: P0 (Blocker)
**Estimated Time**: 45 minutes
**Dependencies**: Task 4.1

**Description**: Create MCP tool for retrieving tasks with filtering.

**Files to Create**:
- `backend/app/mcp_server/tools/list_tasks.py`

**Files to Modify**:
- `backend/app/mcp_server/tools/__init__.py`

**Acceptance Criteria**:
- [ ] Tool accepts filter parameter (all/pending/completed)
- [ ] Queries tasks filtered by user_id
- [ ] Applies completion status filter
- [ ] Orders by created_at DESC
- [ ] Returns tasks array + statistics (total, completed, pending)
- [ ] Statistics calculated from all user tasks (not filtered subset)
- [ ] Error handling for invalid filter values
- [ ] Type hints and docstring

**Implementation Notes**:
```python
# backend/app/mcp_server/tools/list_tasks.py
from typing import Dict, Any, Literal
from sqlmodel import Session, select
from app.models import Task

def list_tasks(
    filter: Literal["all", "pending", "completed"] = "all",
    user_id: str = None,
    session: Session = None
) -> Dict[str, Any]:
    """List tasks with optional filtering.

    Args:
        filter: Filter by status (all, pending, completed)
        user_id: Authenticated user ID (injected)
        session: Database session (injected)

    Returns:
        {success: bool, tasks: list, total: int, completed: int, pending: int}
    """
    try:
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        if filter == "completed":
            query = query.where(Task.completed == True)
        elif filter == "pending":
            query = query.where(Task.completed == False)

        query = query.order_by(Task.created_at.desc())

        tasks = session.exec(query).all()

        # Calculate statistics from all tasks
        all_tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()

        total = len(all_tasks)
        completed = sum(1 for t in all_tasks if t.completed)
        pending = total - completed

        return {
            "success": True,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "created_at": t.created_at.isoformat()
                }
                for t in tasks
            ],
            "total": total,
            "completed": completed,
            "pending": pending
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 78-121

---

### Task 4.4: Implement complete_task Tool

**Priority**: P0 (Blocker)
**Estimated Time**: 40 minutes
**Dependencies**: Task 4.1

**Description**: Create MCP tool for marking tasks complete.

**Files to Create**:
- `backend/app/mcp_server/tools/complete_task.py`

**Files to Modify**:
- `backend/app/mcp_server/tools/__init__.py`

**Acceptance Criteria**:
- [ ] Tool accepts task_id parameter
- [ ] Queries task by ID
- [ ] Verifies task.user_id == authenticated user_id
- [ ] Sets completed=True, updates updated_at
- [ ] Returns updated task
- [ ] Error handling: task not found (404)
- [ ] Error handling: access denied (403)
- [ ] Type hints and docstring

**Implementation Notes**:
```python
# backend/app/mcp_server/tools/complete_task.py
from typing import Dict, Any
from sqlmodel import Session
from app.models import Task
from datetime import datetime

def complete_task(
    task_id: int,
    user_id: str = None,
    session: Session = None
) -> Dict[str, Any]:
    """Mark a task as complete.

    Args:
        task_id: ID of task to complete
        user_id: Authenticated user ID (injected)
        session: Database session (injected)

    Returns:
        {success: bool, task: dict} or {success: false, error: str}
    """
    try:
        task = session.get(Task, task_id)

        if not task:
            return {"success": False, "error": f"Task with id {task_id} not found"}

        if task.user_id != user_id:
            return {"success": False, "error": "Access denied. This task belongs to another user"}

        task.completed = True
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat()
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 125-173

---

### Task 4.5: Implement delete_task Tool

**Priority**: P1
**Estimated Time**: 40 minutes
**Dependencies**: Task 4.1

**Description**: Create MCP tool for deleting tasks.

**Files to Create**:
- `backend/app/mcp_server/tools/delete_task.py`

**Files to Modify**:
- `backend/app/mcp_server/tools/__init__.py`

**Acceptance Criteria**:
- [ ] Tool accepts task_id parameter
- [ ] Queries task by ID
- [ ] Verifies ownership (task.user_id == user_id)
- [ ] Deletes task from database
- [ ] Returns success confirmation
- [ ] Error handling: not found, access denied
- [ ] Type hints and docstring

**Implementation Notes**:
```python
# backend/app/mcp_server/tools/delete_task.py
from typing import Dict, Any
from sqlmodel import Session
from app.models import Task

def delete_task(
    task_id: int,
    user_id: str = None,
    session: Session = None
) -> Dict[str, Any]:
    """Delete a task.

    Args:
        task_id: ID of task to delete
        user_id: Authenticated user ID (injected)
        session: Database session (injected)

    Returns:
        {success: bool, message: str} or {success: false, error: str}
    """
    try:
        task = session.get(Task, task_id)

        if not task:
            return {"success": False, "error": f"Task with id {task_id} not found"}

        if task.user_id != user_id:
            return {"success": False, "error": "Access denied. This task belongs to another user"}

        session.delete(task)
        session.commit()

        return {"success": True, "message": f"Task {task_id} deleted successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 177-218

---

### Task 4.6: Implement update_task Tool

**Priority**: P1
**Estimated Time**: 50 minutes
**Dependencies**: Task 4.1

**Description**: Create MCP tool for updating task details.

**Files to Create**:
- `backend/app/mcp_server/tools/update_task.py`

**Files to Modify**:
- `backend/app/mcp_server/tools/__init__.py`

**Acceptance Criteria**:
- [ ] Tool accepts task_id, title (optional), description (optional), completed (optional)
- [ ] At least one update field must be provided
- [ ] Verifies ownership
- [ ] Updates only provided fields
- [ ] Updates updated_at timestamp
- [ ] Returns updated task
- [ ] Error handling: not found, access denied, no fields provided
- [ ] Type hints and docstring

**Implementation Notes**:
```python
# backend/app/mcp_server/tools/update_task.py
from typing import Dict, Any, Optional
from sqlmodel import Session
from app.models import Task
from datetime import datetime

def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    user_id: str = None,
    session: Session = None
) -> Dict[str, Any]:
    """Update a task's details.

    Args:
        task_id: ID of task to update
        title: New title (1-200 characters)
        description: New description
        completed: New completion status
        user_id: Authenticated user ID (injected)
        session: Database session (injected)

    Returns:
        {success: bool, task: dict} or {success: false, error: str}
    """
    try:
        if title is None and description is None and completed is None:
            return {"success": False, "error": "At least one field must be provided"}

        task = session.get(Task, task_id)

        if not task:
            return {"success": False, "error": f"Task with id {task_id} not found"}

        if task.user_id != user_id:
            return {"success": False, "error": "Access denied"}

        if title is not None:
            if len(title) < 1 or len(title) > 200:
                return {"success": False, "error": "Title must be 1-200 characters"}
            task.title = title

        if description is not None:
            task.description = description

        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat()
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 222-278

---

### Task 4.7: Create OpenAI Agent Configuration

**Priority**: P0 (Blocker)
**Estimated Time**: 60 minutes
**Dependencies**: Task 4.2, Task 4.3, Task 4.4, Task 4.5, Task 4.6

**Description**: Configure OpenAI Agents SDK with MCP tools.

**Files to Create**:
- `backend/app/mcp_server/agent.py`

**Acceptance Criteria**:
- [ ] Agent initialized with OpenAI API key from settings
- [ ] Agent uses configured model (OPENAI_MODEL setting)
- [ ] All 5 MCP tools registered with agent
- [ ] Agent instructions define conversational behavior
- [ ] Instructions explain tool usage
- [ ] Error handling for OpenAI API failures
- [ ] Type hints and docstring

**Implementation Notes**:
```python
# backend/app/mcp_server/agent.py
from openai import OpenAI
from app.config import settings
from app.mcp_server.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

AGENT_INSTRUCTIONS = """
You are a helpful todo management assistant. You can help users:
- Create new tasks
- View all tasks or filter by status (pending/completed)
- Mark tasks as complete
- Update task details
- Delete tasks

When users ask to create a task, extract the task title from their message.
Be conversational and friendly. Confirm actions clearly.
If a user's request is ambiguous, ask clarifying questions.
Never expose technical details like task IDs unless relevant.
"""

def create_agent_tools():
    """Create tool definitions for OpenAI agent."""
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new todo task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Task title (1-200 characters)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional task description"
                        }
                    },
                    "required": ["title"]
                }
            }
        },
        # ... other tools
    ]
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 385-407

---

### Task 4.8: Implement Tool Context Injection

**Priority**: P0 (Blocker)
**Estimated Time**: 45 minutes
**Dependencies**: Task 4.7

**Description**: Create mechanism to inject user_id and database session into MCP tools.

**Files to Create**:
- `backend/app/mcp_server/context.py`

**Acceptance Criteria**:
- [ ] Context manager extracts user_id from FastAPI request
- [ ] Database session injected via dependency
- [ ] Tools receive context automatically
- [ ] user_id NEVER accepted from tool parameters (security)
- [ ] Error handling for missing authentication
- [ ] Type hints and docstring

**Implementation Notes**:
```python
# backend/app/mcp_server/context.py
from typing import Dict, Any, Callable
from sqlmodel import Session
from app.middleware.auth import get_current_user
from app.database import get_session

def inject_context(
    tool_func: Callable,
    user_id: str,
    session: Session
) -> Callable:
    """Inject authentication context into MCP tool.

    Args:
        tool_func: MCP tool function
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Wrapped tool function with context injected
    """
    def wrapper(*args, **kwargs):
        kwargs['user_id'] = user_id
        kwargs['session'] = session
        return tool_func(*args, **kwargs)
    return wrapper
```

**Reference**: [contracts/mcp-tools.md](./contracts/mcp-tools.md) lines 283-306

---

### Task 4.9: Write MCP Tools Unit Tests

**Priority**: P2
**Estimated Time**: 90 minutes
**Dependencies**: Task 4.2, Task 4.3, Task 4.4, Task 4.5, Task 4.6

**Description**: Create unit tests for all MCP tools.

**Files to Create**:
- `backend/tests/test_mcp_tools.py`

**Acceptance Criteria**:
- [ ] Test add_task: success, validation errors
- [ ] Test list_tasks: all filters, statistics calculation
- [ ] Test complete_task: success, not found, access denied
- [ ] Test delete_task: success, not found, access denied
- [ ] Test update_task: all field combinations, validation
- [ ] Mock database session
- [ ] Test user isolation (prevent cross-user access)
- [ ] All tests pass

**Implementation Notes**:
```python
# backend/tests/test_mcp_tools.py
import pytest
from unittest.mock import Mock
from app.mcp_server.tools import add_task, list_tasks

def test_add_task_success():
    session = Mock()
    result = add_task(
        title="Test task",
        description="Test description",
        user_id="user123",
        session=session
    )
    assert result["success"] == True
    assert "task_id" in result

def test_add_task_validation_error():
    result = add_task(title="", user_id="user123", session=Mock())
    assert result["success"] == False
    assert "error" in result
```

---

## Phase 5: Chat API Endpoint (5 tasks)

### Task 5.1: Create Chat Route Handler

**Priority**: P0 (Blocker)
**Estimated Time**: 90 minutes
**Dependencies**: Task 2.1, Task 2.2, Task 3.2, Task 4.7

**Description**: Implement stateless chat endpoint that processes messages.

**Files to Create**:
- `backend/app/routes/chat.py`

**Files to Modify**:
- `backend/app/main.py` (register router)

**Acceptance Criteria**:
- [ ] POST /api/{user_id}/chat endpoint defined
- [ ] Accepts MessageCreate (conversation_id, message)
- [ ] Validates JWT authentication
- [ ] Creates new conversation if conversation_id not provided
- [ ] Loads conversation history from database
- [ ] Sends message + history to OpenAI agent
- [ ] Receives agent response with tool calls
- [ ] Saves user message and assistant response to database
- [ ] Returns ChatResponse
- [ ] Error handling: 401, 403, 404, 500
- [ ] Type hints and docstring
- [ ] Route registered in main.py

**Implementation Notes**:
```python
# backend/app/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict
from datetime import datetime
import uuid

from app.database import get_session
from app.models import Conversation, Message
from app.schemas.message import MessageCreate, ChatResponse
from app.middleware.auth import get_current_user
from app.mcp_server.agent import process_message

router = APIRouter()

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def send_chat_message(
    user_id: str,
    message_data: MessageCreate,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Send a chat message and get AI response.

    Args:
        user_id: User ID from path (must match JWT)
        message_data: Message with optional conversation_id
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        ChatResponse with conversation_id, response, tool_calls
    """
    # Validate user_id matches JWT
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Get or create conversation
    if message_data.conversation_id:
        conversation = session.get(Conversation, message_data.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if conversation.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.flush()

    # Load conversation history
    history = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
    ).all()

    # Save user message
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=message_data.message,
        created_at=datetime.utcnow()
    )
    session.add(user_message)

    # Process with AI agent
    agent_response = await process_message(
        message=message_data.message,
        history=history,
        user_id=user_id,
        session=session
    )

    # Save assistant message
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=agent_response["response"],
        created_at=datetime.utcnow()
    )
    session.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)

    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=agent_response["response"],
        tool_calls=agent_response.get("tool_calls", []),
        created_at=assistant_message.created_at
    )
```

**Reference**: [contracts/chat-api.md](./contracts/chat-api.md) lines 15-69

---

### Task 5.2: Implement Agent Message Processing

**Priority**: P0 (Blocker)
**Estimated Time**: 90 minutes
**Dependencies**: Task 4.7, Task 4.8

**Description**: Create function to process messages with OpenAI agent and execute tools.

**Files to Modify**:
- `backend/app/mcp_server/agent.py`

**Acceptance Criteria**:
- [ ] Function accepts message, history, user_id, session
- [ ] Formats conversation history for OpenAI API
- [ ] Calls OpenAI chat completion with tools
- [ ] Executes tool calls with injected context
- [ ] Handles tool execution errors gracefully
- [ ] Returns response text and tool_calls array
- [ ] Implements message history windowing (MAX_CONVERSATION_MESSAGES)
- [ ] Error handling for OpenAI API failures
- [ ] Retry logic for rate limits (exponential backoff)
- [ ] Type hints and docstring

**Implementation Notes**:
```python
# backend/app/mcp_server/agent.py (add this function)
from typing import List, Dict, Any
from app.models import Message
from app.config import settings

async def process_message(
    message: str,
    history: List[Message],
    user_id: str,
    session: Session
) -> Dict[str, Any]:
    """Process user message with OpenAI agent.

    Args:
        message: User's message
        history: Previous messages in conversation
        user_id: Authenticated user ID
        session: Database session

    Returns:
        {response: str, tool_calls: list}
    """
    # Format history for OpenAI (window to last N messages)
    max_messages = settings.MAX_CONVERSATION_MESSAGES
    recent_history = history[-max_messages:] if len(history) > max_messages else history

    messages = [
        {"role": "system", "content": AGENT_INSTRUCTIONS}
    ]

    for msg in recent_history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    messages.append({"role": "user", "content": message})

    # Call OpenAI with tools
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        tools=create_agent_tools()
    )

    # Execute tool calls
    tool_calls_results = []
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Get tool function and inject context
            tool_func = get_tool_function(tool_name)
            result = tool_func(**arguments, user_id=user_id, session=session)

            tool_calls_results.append({
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            })

    return {
        "response": response.choices[0].message.content,
        "tool_calls": tool_calls_results
    }
```

---

### Task 5.3: Implement Conversation Management Endpoints

**Priority**: P2
**Estimated Time**: 60 minutes
**Dependencies**: Task 5.1

**Description**: Add endpoints for listing and managing conversations.

**Files to Modify**:
- `backend/app/routes/chat.py`

**Acceptance Criteria**:
- [ ] GET /api/{user_id}/conversations - List user's conversations
- [ ] GET /api/{user_id}/conversations/{id} - Get conversation history
- [ ] DELETE /api/{user_id}/conversations/{id} - Delete conversation
- [ ] Pagination support (limit, offset)
- [ ] Authentication required
- [ ] User isolation enforced
- [ ] Error handling
- [ ] Type hints and docstrings

**Implementation Notes**:
```python
@router.get("/{user_id}/conversations")
async def list_conversations(
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List user's conversations."""
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403)

    query = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )

    conversations = session.exec(query).all()

    return {
        "conversations": conversations,
        "total": len(conversations)
    }
```

**Reference**: [contracts/chat-api.md](./contracts/chat-api.md) lines 115-162

---

### Task 5.4: Add Error Handling and Rate Limiting

**Priority**: P2
**Estimated Time**: 45 minutes
**Dependencies**: Task 5.1, Task 5.2

**Description**: Implement comprehensive error handling and rate limiting.

**Files to Modify**:
- `backend/app/routes/chat.py`
- `backend/app/mcp_server/agent.py`

**Acceptance Criteria**:
- [ ] OpenAI API errors caught and return 500/503
- [ ] Rate limit errors return 429 with retry_after
- [ ] Validation errors return 400 with clear messages
- [ ] Database errors return 500 with generic message
- [ ] Detailed errors logged server-side
- [ ] Generic errors shown to users (no sensitive info)
- [ ] Rate limiting: 30 req/min per user on chat endpoint
- [ ] Exponential backoff for OpenAI retries

**Implementation Notes**:
```python
from fastapi import HTTPException
from openai import RateLimitError, APIError

try:
    response = client.chat.completions.create(...)
except RateLimitError as e:
    raise HTTPException(
        status_code=503,
        detail="Service is busy. Please try again in a few seconds",
        headers={"Retry-After": "5"}
    )
except APIError as e:
    logger.error(f"OpenAI API error: {e}")
    raise HTTPException(
        status_code=500,
        detail="I'm temporarily unavailable. Please try again in a moment"
    )
```

**Reference**: [contracts/chat-api.md](./contracts/chat-api.md) lines 163-184

---

### Task 5.5: Write Chat Endpoint Tests

**Priority**: P2
**Estimated Time**: 90 minutes
**Dependencies**: Task 5.1, Task 5.2, Task 5.3

**Description**: Create integration tests for chat endpoints.

**Files to Create**:
- `backend/tests/test_chat_endpoints.py`

**Acceptance Criteria**:
- [ ] Test send message (new conversation)
- [ ] Test send message (existing conversation)
- [ ] Test conversation history loading
- [ ] Test user isolation (403 errors)
- [ ] Test authentication requirement (401 errors)
- [ ] Test conversation not found (404 error)
- [ ] Test list conversations
- [ ] Test delete conversation
- [ ] Mock OpenAI API calls
- [ ] All tests pass

**Implementation Notes**:
```python
# backend/tests/test_chat_endpoints.py
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_send_chat_message_new_conversation(client, auth_headers):
    with patch('app.mcp_server.agent.process_message') as mock_agent:
        mock_agent.return_value = {
            "response": "I've added the task.",
            "tool_calls": []
        }

        response = client.post(
            "/api/user123/chat",
            json={"message": "Add task to buy milk"},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["response"] == "I've added the task."
```

---

## Phase 6: Frontend ChatKit (8 tasks)

### Task 6.1: Create Chat API Client

**Priority**: P0 (Blocker)
**Estimated Time**: 45 minutes
**Dependencies**: Task 3.3 (TypeScript interfaces)

**Description**: Create TypeScript client for chat API with JWT authentication.

**Files to Create**:
- `frontend/lib/chat-api.ts`

**Acceptance Criteria**:
- [ ] sendMessage function (conversation_id, message) → ChatResponse
- [ ] getConversations function → Conversation[]
- [ ] getConversationHistory function (conversation_id) → Message[]
- [ ] deleteConversation function (conversation_id)
- [ ] JWT token included in Authorization header
- [ ] Error handling for API failures
- [ ] TypeScript types from chat.ts interfaces
- [ ] Async/await pattern

**Implementation Notes**:
```typescript
// frontend/lib/chat-api.ts
import { ChatRequest, ChatResponse, Conversation, Message } from './types/chat';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function getAuthHeaders(): Promise<HeadersInit> {
  const token = localStorage.getItem('auth_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
}

export async function sendMessage(
  userId: string,
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify(request)
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function getConversations(userId: string): Promise<Conversation[]> {
  const response = await fetch(`${API_URL}/api/${userId}/conversations`, {
    headers: await getAuthHeaders()
  });

  if (!response.ok) throw new Error('Failed to fetch conversations');

  const data = await response.json();
  return data.conversations;
}

export async function getConversationHistory(
  userId: string,
  conversationId: string
): Promise<Message[]> {
  const response = await fetch(
    `${API_URL}/api/${userId}/conversations/${conversationId}`,
    { headers: await getAuthHeaders() }
  );

  if (!response.ok) throw new Error('Failed to fetch history');

  const data = await response.json();
  return data.messages;
}

export async function deleteConversation(
  userId: string,
  conversationId: string
): Promise<void> {
  const response = await fetch(
    `${API_URL}/api/${userId}/conversations/${conversationId}`,
    { method: 'DELETE', headers: await getAuthHeaders() }
  );

  if (!response.ok) throw new Error('Failed to delete conversation');
}
```

---

### Task 6.2: Create Chat Page Route

**Priority**: P0 (Blocker)
**Estimated Time**: 30 minutes
**Dependencies**: None

**Description**: Set up Next.js App Router page for chat interface.

**Files to Create**:
- `frontend/app/chat/page.tsx`
- `frontend/app/chat/layout.tsx` (optional)

**Acceptance Criteria**:
- [ ] Page created at /app/chat/page.tsx
- [ ] Protected route (requires authentication)
- [ ] Imports ChatInterface component
- [ ] Responsive layout
- [ ] Page metadata (title, description)
- [ ] TypeScript strict mode compliant

**Implementation Notes**:
```typescript
// frontend/app/chat/page.tsx
import { Metadata } from 'next';
import ChatInterface from '@/components/chat/ChatInterface';
import { AuthGuard } from '@/components/auth/AuthGuard';

export const metadata: Metadata = {
  title: 'Chat | Todo AI Assistant',
  description: 'Manage your tasks with natural language'
};

export default function ChatPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto max-w-4xl h-screen">
        <ChatInterface />
      </div>
    </AuthGuard>
  );
}
```

---

### Task 6.3: Create ChatInterface Component

**Priority**: P0 (Blocker)
**Estimated Time**: 90 minutes
**Dependencies**: Task 6.1 (chat API client)

**Description**: Main chat interface component using OpenAI ChatKit.

**Files to Create**:
- `frontend/components/chat/ChatInterface.tsx`

**Acceptance Criteria**:
- [ ] Uses OpenAI ChatKit components
- [ ] Displays message list
- [ ] Message input at bottom
- [ ] Send button and Enter key support
- [ ] Loading state while AI responds
- [ ] Error handling and display
- [ ] Conversation state management
- [ ] Calls sendMessage API
- [ ] Updates UI optimistically
- [ ] Responsive design
- [ ] TypeScript types

**Implementation Notes**:
```typescript
// frontend/components/chat/ChatInterface.tsx
'use client';

import { useState } from 'react';
import { ChatKit } from '@openai/chatkit';
import { sendMessage } from '@/lib/chat-api';
import { Message } from '@/lib/types/chat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSendMessage = async (content: string) => {
    const userId = localStorage.getItem('user_id'); // From auth

    // Optimistic update
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);
    setError(null);

    try {
      const response = await sendMessage(userId!, {
        conversation_id: conversationId,
        message: content
      });

      setConversationId(response.conversation_id);

      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        created_at: response.created_at
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError('Failed to send message. Please try again.');
      // Remove optimistic message on error
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      <div className="p-4 border-b">
        <h1 className="text-2xl font-bold">Todo AI Assistant</h1>
      </div>

      <MessageList messages={messages} isLoading={isLoading} />

      {error && (
        <div className="px-4 py-2 bg-red-50 text-red-600">
          {error}
        </div>
      )}

      <MessageInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}
```

---

### Task 6.4: Create MessageList Component

**Priority**: P0 (Blocker)
**Estimated Time**: 60 minutes
**Dependencies**: Task 3.3 (TypeScript interfaces)

**Description**: Component to display chat message history.

**Files to Create**:
- `frontend/components/chat/MessageList.tsx`

**Acceptance Criteria**:
- [ ] Displays array of messages
- [ ] Differentiates user vs assistant messages
- [ ] Auto-scrolls to latest message
- [ ] Shows typing indicator when loading
- [ ] Empty state for no messages
- [ ] Virtualization for long conversations (optional)
- [ ] Responsive design
- [ ] TypeScript types

**Implementation Notes**:
```typescript
// frontend/components/chat/MessageList.tsx
'use client';

import { useEffect, useRef } from 'react';
import { Message } from '@/lib/types/chat';

interface Props {
  messages: Message[];
  isLoading: boolean;
}

export default function MessageList({ messages, isLoading }: Props) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        <p>Start a conversation by typing a message below</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[70%] rounded-lg px-4 py-2 ${
              message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-900'
            }`}
          >
            <p className="whitespace-pre-wrap">{message.content}</p>
            <span className="text-xs opacity-70 mt-1 block">
              {new Date(message.created_at).toLocaleTimeString()}
            </span>
          </div>
        </div>
      ))}

      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-gray-100 rounded-lg px-4 py-2">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
```

---

### Task 6.5: Create MessageInput Component

**Priority**: P0 (Blocker)
**Estimated Time**: 45 minutes
**Dependencies**: None

**Description**: Component for message input with send button.

**Files to Create**:
- `frontend/components/chat/MessageInput.tsx`

**Acceptance Criteria**:
- [ ] Textarea for message input
- [ ] Send button
- [ ] Enter key sends message (Shift+Enter for newline)
- [ ] Disabled state while loading
- [ ] Auto-resize textarea
- [ ] Character limit (5000 chars)
- [ ] Clear input after send
- [ ] Responsive design
- [ ] TypeScript types

**Implementation Notes**:
```typescript
// frontend/components/chat/MessageInput.tsx
'use client';

import { useState, KeyboardEvent } from 'react';

interface Props {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function MessageInput({ onSend, disabled = false }: Props) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t p-4">
      <div className="flex gap-2">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
          disabled={disabled}
          maxLength={5000}
          rows={3}
          className="flex-1 resize-none border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          Send
        </button>
      </div>
      <p className="text-xs text-gray-500 mt-1">
        {message.length}/5000 characters
      </p>
    </div>
  );
}
```

---

### Task 6.6: Add Navigation to Chat Page

**Priority**: P2
**Estimated Time**: 20 minutes
**Dependencies**: Task 6.2

**Description**: Add chat link to navigation menu.

**Files to Modify**:
- `frontend/components/navigation/Header.tsx` (or equivalent nav component)

**Acceptance Criteria**:
- [ ] "Chat" link in navigation
- [ ] Active state when on /chat route
- [ ] Only visible when authenticated
- [ ] Responsive navigation
- [ ] Icon for chat (optional)

**Implementation Notes**:
```typescript
<nav>
  <Link href="/dashboard">Dashboard</Link>
  <Link href="/chat">Chat</Link>
  <Link href="/logout">Logout</Link>
</nav>
```

---

### Task 6.7: Create Conversation List Component (Optional)

**Priority**: P3
**Estimated Time**: 75 minutes
**Dependencies**: Task 6.1 (API client)

**Description**: Sidebar component showing conversation history.

**Files to Create**:
- `frontend/components/chat/ConversationList.tsx`

**Acceptance Criteria**:
- [ ] Lists user's conversations
- [ ] Shows last message preview
- [ ] Click to load conversation
- [ ] Delete conversation button
- [ ] Sorted by updated_at
- [ ] Loading state
- [ ] Empty state
- [ ] Responsive (collapsible on mobile)

**Implementation Notes**:
```typescript
// frontend/components/chat/ConversationList.tsx
'use client';

import { useState, useEffect } from 'react';
import { getConversations, deleteConversation } from '@/lib/chat-api';
import { Conversation } from '@/lib/types/chat';

interface Props {
  userId: string;
  onSelectConversation: (id: string) => void;
  currentConversationId?: string;
}

export default function ConversationList({
  userId,
  onSelectConversation,
  currentConversationId
}: Props) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConversations();
  }, [userId]);

  const loadConversations = async () => {
    try {
      const data = await getConversations(userId);
      setConversations(data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm('Delete this conversation?')) {
      try {
        await deleteConversation(userId, id);
        setConversations(prev => prev.filter(c => c.id !== id));
      } catch (error) {
        alert('Failed to delete conversation');
      }
    }
  };

  if (loading) return <div className="p-4">Loading...</div>;

  if (conversations.length === 0) {
    return <div className="p-4 text-gray-500">No conversations yet</div>;
  }

  return (
    <div className="divide-y">
      {conversations.map((conv) => (
        <div
          key={conv.id}
          className={`p-4 cursor-pointer hover:bg-gray-50 ${
            conv.id === currentConversationId ? 'bg-blue-50' : ''
          }`}
          onClick={() => onSelectConversation(conv.id)}
        >
          <div className="flex justify-between items-start">
            <p className="text-sm text-gray-600">
              {new Date(conv.updated_at).toLocaleDateString()}
            </p>
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDelete(conv.id);
              }}
              className="text-red-600 hover:text-red-800"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
```

---

### Task 6.8: Add Responsive Mobile Layout

**Priority**: P2
**Estimated Time**: 45 minutes
**Dependencies**: Task 6.3, Task 6.4, Task 6.5

**Description**: Optimize chat interface for mobile devices.

**Files to Modify**:
- `frontend/components/chat/ChatInterface.tsx`
- `frontend/components/chat/MessageList.tsx`
- `frontend/components/chat/MessageInput.tsx`

**Acceptance Criteria**:
- [ ] Full-height layout on mobile (100vh)
- [ ] Touch-friendly input area
- [ ] Proper keyboard handling on mobile
- [ ] Responsive text sizes
- [ ] Tested on mobile viewport (< 640px)
- [ ] No horizontal scroll
- [ ] Message bubbles fit screen width

**Implementation Notes**:
```typescript
// Use Tailwind responsive classes
<div className="h-screen md:h-auto">
  <textarea className="text-base md:text-sm" />
  <div className="px-4 md:px-6" />
</div>
```

---

## Phase 7: Integration & Testing (3 tasks)

### Task 7.1: End-to-End Integration Testing

**Priority**: P2
**Estimated Time**: 90 minutes
**Dependencies**: All previous tasks

**Description**: Test complete flow from frontend to backend to database.

**Acceptance Criteria**:
- [ ] User can send message from ChatKit UI
- [ ] Message saved to database (messages table)
- [ ] AI processes message and calls MCP tools
- [ ] Tool executes task operation (e.g., creates task in tasks table)
- [ ] AI response displayed in UI
- [ ] Conversation persists across page refreshes
- [ ] Multiple users have isolated conversations
- [ ] Test on local environment
- [ ] No errors in browser console or backend logs

**Test Scenarios**:
1. Create task via chat → verify in tasks table
2. List tasks via chat → verify response
3. Mark complete via chat → verify task updated
4. Delete task via chat → verify task removed
5. Multi-turn conversation → verify context maintained
6. New conversation → verify new UUID created
7. Existing conversation → verify history loaded

---

### Task 7.2: Error Handling Validation

**Priority**: P2
**Estimated Time**: 60 minutes
**Dependencies**: Task 7.1

**Description**: Test all error scenarios and edge cases.

**Acceptance Criteria**:
- [ ] Test: OpenAI API down → graceful error message
- [ ] Test: Invalid JWT → 401 error
- [ ] Test: Access other user's conversation → 403 error
- [ ] Test: Conversation not found → 404 error
- [ ] Test: Empty message → validation error
- [ ] Test: Message too long (> 5000 chars) → validation error
- [ ] Test: Database connection failure → error handling
- [ ] Test: MCP tool error → AI informs user
- [ ] Test: Rate limit exceeded → 429 error with retry_after
- [ ] All errors display user-friendly messages

---

### Task 7.3: Performance Testing

**Priority**: P3
**Estimated Time**: 60 minutes
**Dependencies**: Task 7.1

**Description**: Verify performance meets success criteria.

**Acceptance Criteria**:
- [ ] Chat response < 3 seconds (SC-003)
- [ ] Conversation history loads < 1 second (SC-004)
- [ ] 20+ concurrent chat sessions supported (SC-006)
- [ ] Database queries use indexes (verify with EXPLAIN)
- [ ] No N+1 query problems
- [ ] Frontend renders smoothly (no lag on message send)
- [ ] Memory usage stable over extended use

**Test Plan**:
```bash
# Load test with multiple concurrent users
# Use tools like Apache Bench or Locust
ab -n 100 -c 20 http://localhost:8000/api/user123/chat
```

---

## Phase 8: Documentation & Deployment (2 tasks)

### Task 8.1: Update Environment Configuration

**Priority**: P1
**Estimated Time**: 30 minutes
**Dependencies**: All implementation tasks

**Description**: Document all environment variables and create examples.

**Files to Modify**:
- `backend/.env.example`
- `backend/README.md` (or docs/)

**Acceptance Criteria**:
- [ ] .env.example includes all Phase III variables
- [ ] Each variable has description comment
- [ ] Required vs optional variables marked
- [ ] Example values provided
- [ ] Setup instructions updated
- [ ] Deployment guide includes env var setup

**Implementation Notes**:
```bash
# backend/.env.example

# Phase II - Existing
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key-min-32-characters
JWT_SECRET_KEY=your-jwt-secret-key
FRONTEND_URL=http://localhost:3000

# Phase III - New (Required)
OPENAI_API_KEY=sk-your-openai-api-key-here  # Get from https://platform.openai.com/api-keys

# Phase III - Optional (with defaults)
OPENAI_MODEL=gpt-4  # Model for AI agent (default: gpt-4)
MAX_CONVERSATION_MESSAGES=50  # Max messages loaded per request (default: 50)
```

---

### Task 8.2: Create Deployment Checklist

**Priority**: P2
**Estimated Time**: 30 minutes
**Dependencies**: All implementation tasks

**Description**: Document deployment steps for Phase III.

**Files to Create**:
- `docs/DEPLOYMENT_PHASE3.md` (or update existing deployment docs)

**Acceptance Criteria**:
- [ ] Prerequisites listed (OpenAI API key, Phase II deployed)
- [ ] Database migration steps documented
- [ ] Environment variable configuration steps
- [ ] Backend deployment steps (Railway/Render)
- [ ] Frontend deployment steps (Vercel)
- [ ] Verification steps
- [ ] Rollback procedure
- [ ] Troubleshooting common issues

**Deployment Checklist Template**:
```markdown
## Phase III Deployment Checklist

### Prerequisites
- [ ] Phase II deployed and running
- [ ] OpenAI API key obtained
- [ ] Database accessible

### Backend Deployment
- [ ] Add OPENAI_API_KEY to Railway/Render environment variables
- [ ] Update requirements.txt with Phase III dependencies
- [ ] Run database migrations (conversations, messages tables)
- [ ] Deploy backend code
- [ ] Verify /docs shows new /chat endpoint
- [ ] Test chat endpoint with curl

### Frontend Deployment
- [ ] Install @openai/chatkit dependency
- [ ] Deploy to Vercel
- [ ] Verify /chat route accessible
- [ ] Test chat functionality

### Verification
- [ ] User can send chat message
- [ ] AI responds correctly
- [ ] Tasks created via chat appear in database
- [ ] Conversation persists across page refreshes
- [ ] No errors in logs

### Rollback (if needed)
- [ ] Revert backend code
- [ ] Revert frontend code
- [ ] Keep database tables (data preserved)
```

---

## Task Dependencies Graph

```
Phase 1 (Environment): 1.1, 1.2, 1.3 (parallel)
                        ↓
Phase 2 (Database):    2.1 → 2.2 → 2.3 → 2.4
                        ↓     ↓
Phase 3 (Schemas):     3.1   3.2 → 3.3
                              ↓    3.4
                              ↓
Phase 4 (MCP):         4.1 → 4.2, 4.3, 4.4, 4.5, 4.6 (parallel)
                        ↓                              ↓
                       4.7 ← ← ← ← ← ← ← ← ← ← ← ← ←
                        ↓
                       4.8 → 4.9
                        ↓
Phase 5 (Chat API):    5.1 → 5.2 → 5.3
                        ↓           ↓
                       5.4 → → → → 5.5
                        ↓
Phase 6 (Frontend):    6.1 → 6.3 → 6.4, 6.5 (parallel)
                        ↓     ↓
                       6.2 ← ←
                        ↓
                       6.6, 6.7, 6.8 (parallel)
                        ↓
Phase 7 (Testing):     7.1 → 7.2, 7.3 (parallel)
                        ↓
Phase 8 (Docs):        8.1, 8.2 (parallel)
```

---

## Priority Levels

- **P0 (Blocker)**: Must complete to have working chatbot (25 tasks)
- **P1 (High)**: Important features for good UX (8 tasks)
- **P2 (Medium)**: Quality improvements (4 tasks)
- **P3 (Low)**: Nice-to-have enhancements (1 task)

---

## Estimated Timeline

**Aggressive** (full-time, experienced developer):
- Phase 1: 0.5 hours
- Phase 2: 2 hours
- Phase 3: 2.5 hours
- Phase 4: 7 hours
- Phase 5: 6 hours
- Phase 6: 6 hours
- Phase 7: 3.5 hours
- Phase 8: 1 hour
**Total: ~28.5 hours (3-4 days)**

**Moderate** (part-time or learning):
- **Total: ~50-60 hours (1-2 weeks)**

---

## Next Steps

1. **Review this task breakdown** with your team
2. **Set up development environment** (Phase 1)
3. **Create feature branch**: `git checkout -b 002-phase3-ai-chatbot`
4. **Start with Phase 1, Task 1.1** (Configure OpenAI API Key)
5. **Follow dependency order** from graph above
6. **Test incrementally** after each phase
7. **Update README** as you complete tasks
8. **Create pull request** when Phase III complete

---

**Status**: Tasks ready for implementation
**Last Updated**: 2026-01-04
