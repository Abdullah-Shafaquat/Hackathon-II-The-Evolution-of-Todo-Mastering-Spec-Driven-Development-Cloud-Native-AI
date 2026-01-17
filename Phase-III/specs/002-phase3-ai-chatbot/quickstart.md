# Quickstart Guide: Phase III AI Chatbot

**Last Updated**: 2026-01-04
**Prerequisites**: Phase II completed and running

## Overview

This guide walks you through setting up and running the Phase III AI Chatbot extension to your existing Phase II Todo application.

---

## Prerequisites

Before starting Phase III implementation:

1. **Phase II Running**: Full-stack todo app with authentication
2. **OpenAI API Key**: Obtain from https://platform.openai.com/api-keys
3. **Python 3.11+**: For backend MCP server
4. **Node.js 18+**: For frontend ChatKit
5. **PostgreSQL Access**: Existing Neon database from Phase II

---

## Environment Setup

### 1. Backend Configuration

Add OpenAI API key to backend environment:

```bash
cd backend

# Update .env file
echo "OPENAI_API_KEY=sk-your-api-key-here" >> .env
echo "OPENAI_MODEL=gpt-4" >> .env
echo "MAX_CONVERSATION_MESSAGES=50" >> .env
```

**Example .env** (complete):
```bash
# Database (existing Phase II)
DATABASE_URL=postgresql://neondb_owner:...@ep-shiny-bar-adtgsazt-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require

# Authentication (existing Phase II)
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
REFRESH_TOKEN_EXPIRE_MINUTES=43200

# CORS (existing Phase II)
FRONTEND_URL=http://localhost:3000

# Server (existing Phase II)
HOST=0.0.0.0
PORT=8000

# NEW: Phase III - OpenAI Configuration
OPENAI_API_KEY=sk-proj-...  # Your OpenAI API key
OPENAI_MODEL=gpt-4
MAX_CONVERSATION_MESSAGES=50
```

### 2. Install Backend Dependencies

```bash
cd backend

# Install new dependencies
pip install mcp openai openai-agents-sdk

# Or update requirements.txt and install all
pip install -r requirements.txt
```

**Updated requirements.txt** (Phase III additions):
```txt
# Existing Phase II dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
asyncpg==0.29.0
psycopg2-binary==2.9.9

# NEW: Phase III dependencies
mcp==0.1.0                    # Official Python MCP SDK
openai==1.6.0                 # OpenAI Python client
openai-agents-sdk==0.2.0      # OpenAI Agents SDK
```

### 3. Frontend Configuration

Install ChatKit in frontend:

```bash
cd frontend

# Install OpenAI ChatKit
npm install @openai/chatkit

# Or update package.json and install
npm install
```

**Updated package.json** (Phase III addition):
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.3.0",
    "@openai/chatkit": "^1.2.0"
  }
}
```

---

## Database Migration

### 1. Create Conversations and Messages Tables

Run migration to add new tables:

```bash
cd backend

# Option 1: Using migration script (if available)
python scripts/migrate_phase3.py

# Option 2: Manual SQL execution
# Connect to your Neon database and run:
```

**Migration SQL**:
```sql
-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for conversations
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

-- Create messages table
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

-- Create indexes for messages
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

### 2. Verify Tables Created

```bash
# Connect to database and verify
psql $DATABASE_URL

\dt conversations
\dt messages
\d conversations
\d messages
```

Expected output:
```
                 Table "public.conversations"
   Column    |            Type             | Nullable
-------------+-----------------------------+----------
 id          | uuid                        | not null
 user_id     | character varying(255)      | not null
 created_at  | timestamp without time zone | not null
 updated_at  | timestamp without time zone | not null

                    Table "public.messages"
     Column       |            Type             | Nullable
------------------+-----------------------------+----------
 id               | integer                     | not null
 user_id          | character varying(255)      | not null
 conversation_id  | uuid                        | not null
 role             | character varying(50)       | not null
 content          | text                        | not null
 created_at       | timestamp without time zone | not null
```

---

## Running the Application

### 1. Start Backend

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify backend running**:
- Navigate to: http://localhost:8000/docs
- Check for new endpoint: `POST /api/{user_id}/chat`
- Verify existing endpoints still work

### 2. Start Frontend

```bash
cd frontend

# Start Next.js development server
npm run dev
```

**Verify frontend running**:
- Navigate to: http://localhost:3000
- Check existing routes still work (/dashboard, /login, /signup)
- Navigate to new chat route: http://localhost:3000/chat

---

## Testing the Chatbot

### 1. Create Test User (if needed)

```bash
# Use existing Phase II user or create new one via signup page
# http://localhost:3000/signup
```

### 2. Test Chat Interface

1. **Login**: http://localhost:3000/login
2. **Navigate to Chat**: http://localhost:3000/chat
3. **Send test messages**:

**Test 1 - Create Task**:
```
You: Add a task to buy groceries
AI: I've added 'Buy groceries' to your tasks.
```

**Test 2 - List Tasks**:
```
You: Show me all my tasks
AI: You have 3 tasks:
1. Buy groceries (pending)
2. Call mom (pending)
3. Finish project (completed)
```

**Test 3 - Mark Complete**:
```
You: Mark task 1 as complete
AI: Done! I've marked task 1 as complete.
```

**Test 4 - Update Task**:
```
You: Change task 2 to "Call mom tonight"
AI: Updated! Task 2 is now 'Call mom tonight'.
```

**Test 5 - Delete Task**:
```
You: Delete task 3
AI: Removed 'Finish project' from your tasks.
```

### 3. Verify Database Changes

```sql
-- Check conversations created
SELECT * FROM conversations WHERE user_id = 'your-user-id';

-- Check messages stored
SELECT * FROM messages WHERE conversation_id = 'conversation-id-from-above';

-- Verify tasks were modified
SELECT * FROM tasks WHERE user_id = 'your-user-id';
```

---

## Common Issues & Troubleshooting

### Issue 1: "OpenAI API Key Invalid"

**Error**: `401 Unauthorized from OpenAI API`

**Solution**:
1. Verify API key in `.env`: `OPENAI_API_KEY=sk-...`
2. Check key validity at: https://platform.openai.com/api-keys
3. Ensure key has GPT-4 access (or change `OPENAI_MODEL=gpt-3.5-turbo`)
4. Restart backend after updating `.env`

### Issue 2: "Conversation Table Not Found"

**Error**: `relation "conversations" does not exist`

**Solution**:
1. Run database migrations (see Database Migration section)
2. Verify tables exist: `\dt conversations` in psql
3. Check DATABASE_URL points to correct database

### Issue 3: "Chat Endpoint 404"

**Error**: `POST /api/{user_id}/chat returns 404`

**Solution**:
1. Verify chat routes registered in `app/main.py`
2. Check backend logs for startup errors
3. Restart backend: `uvicorn app.main:app --reload`

### Issue 4: "ChatKit Component Not Rendering"

**Error**: Blank chat page or import errors

**Solution**:
1. Verify ChatKit installed: `npm list @openai/chatkit`
2. Check for TypeScript errors: `npm run build`
3. Clear Next.js cache: `rm -rf .next && npm run dev`

### Issue 5: "MCP Tools Not Called"

**Error**: AI responds but doesn't create/modify tasks

**Solution**:
1. Check MCP server initialization in backend logs
2. Verify tools registered with agent
3. Test tools directly (write unit tests)
4. Check OpenAI agent instructions include tool usage

### Issue 6: "Rate Limit Exceeded"

**Error**: `429 Too Many Requests from OpenAI`

**Solution**:
1. Reduce request frequency
2. Implement exponential backoff (should be automatic)
3. Upgrade OpenAI plan for higher limits
4. Cache responses for identical queries

---

## Development Workflow

### 1. Add New MCP Tool

```bash
# Create new tool file
touch backend/app/mcp_server/tools/my_tool.py

# Implement tool with type hints
# Register tool in mcp_server/__init__.py
# Add tool to agent configuration
# Write unit tests
# Test via chat interface
```

### 2. Modify Chat UI

```bash
# Edit ChatKit components
cd frontend/components/chat

# Customize styling with Tailwind
# Add new features (conversation list, message reactions)
# Test responsive design (mobile, tablet, desktop)
```

### 3. Update Database Schema

```bash
# Create migration script
touch backend/migrations/add_column_to_conversations.sql

# Test on local database
psql $DATABASE_URL < migrations/add_column_to_conversations.sql

# Update SQLModel models
# Update Pydantic schemas
# Update TypeScript interfaces
```

---

## Production Deployment

### Backend (Railway/Render)

1. **Add environment variable**:
   ```
   OPENAI_API_KEY=sk-...
   ```

2. **Run migrations**:
   ```bash
   # SSH into production or run via platform CLI
   psql $DATABASE_URL < migrations/phase3.sql
   ```

3. **Deploy updated code**:
   ```bash
   git push railway main
   # or
   git push render main
   ```

4. **Verify deployment**:
   - Check backend health: `https://your-backend.railway.app/health`
   - Test chat endpoint: `POST https://your-backend.railway.app/api/{user_id}/chat`

### Frontend (Vercel)

1. **Update environment** (if needed):
   - No changes needed (uses same NEXT_PUBLIC_API_URL)

2. **Deploy**:
   ```bash
   git push origin main
   # Vercel auto-deploys
   ```

3. **Verify deployment**:
   - Navigate to: `https://your-app.vercel.app/chat`
   - Test chat functionality

---

## Performance Optimization

### Backend

1. **Database Connection Pooling**:
   ```python
   # Already configured in Phase II
   # Verify pool size sufficient for chat load
   ```

2. **OpenAI Response Caching** (optional):
   ```python
   # Cache frequent queries to reduce API calls
   from functools import lru_cache
   ```

3. **Message History Windowing**:
   ```python
   # Limit messages loaded per request
   MAX_CONVERSATION_MESSAGES = 50  # In .env
   ```

### Frontend

1. **Message List Virtualization**:
   ```typescript
   // Use react-window for long conversations
   import { FixedSizeList } from 'react-window';
   ```

2. **Optimistic Updates**:
   ```typescript
   // Show message immediately, confirm with backend
   ```

3. **Lazy Load Conversations**:
   ```typescript
   // Paginate conversation list
   ```

---

## Monitoring & Logging

### Backend Logs

```bash
# View backend logs
tail -f backend/app.log

# Check for errors
grep "ERROR" backend/app.log

# Monitor OpenAI API calls
grep "openai" backend/app.log
```

### Database Queries

```sql
-- Monitor conversation growth
SELECT COUNT(*) FROM conversations;
SELECT COUNT(*) FROM messages;

-- Check user activity
SELECT user_id, COUNT(*) as conversation_count
FROM conversations
GROUP BY user_id
ORDER BY conversation_count DESC;

-- Find long conversations
SELECT conversation_id, COUNT(*) as message_count
FROM messages
GROUP BY conversation_id
HAVING COUNT(*) > 50
ORDER BY message_count DESC;
```

### OpenAI Usage

```bash
# Check usage on OpenAI dashboard
https://platform.openai.com/usage

# Monitor costs
# Set up billing alerts
```

---

## Next Steps

After successful Phase III setup:

1. **Refine AI Prompts**: Improve agent instructions for better responses
2. **Add Features**: Conversation management, search, export
3. **Optimize Performance**: Caching, indexing, query optimization
4. **User Testing**: Gather feedback on conversational interface
5. **Monitor Usage**: Track OpenAI API costs and user engagement

---

## Support

- **Phase II Spec**: [../001-phase2-fullstack-web-app/](../001-phase2-fullstack-web-app/)
- **OpenAI API Docs**: https://platform.openai.com/docs
- **MCP SDK Docs**: [MCP SDK repository]
- **ChatKit Docs**: [@openai/chatkit documentation]

---

**Last Updated**: 2026-01-04
**Status**: Ready for Implementation
