# Phase III: AI-Powered Todo Management System

A full-stack web application with AI chatbot for natural language task management, built using Next.js, FastAPI, PostgreSQL, OpenAI Agents SDK, and MCP Server.

## Overview

This project implements a three-phase todo management system:

- **Phase I** ✅: Python console application for basic todo operations
- **Phase II** ✅: Full-stack web app with authentication and database persistence
- **Phase III** 🚧: AI chatbot for conversational task management (current phase)

## Phase III Features

### Natural Language Interface

Manage tasks through conversational commands:

```
You: Add a task to buy groceries
AI: I've added 'Buy groceries' to your tasks.

You: Show me all my tasks
AI: You have 3 tasks:
1. Buy groceries (pending)
2. Call mom (pending)
3. Finish project (completed)

You: Mark task 1 as complete
AI: Done! I've marked task 1 as complete.
```

### Architecture

```
┌─────────────────┐
│  OpenAI ChatKit │  (Next.js Frontend)
│  Chat Interface │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  FastAPI Chat Endpoint  │
│  Stateless, DB-backed   │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  OpenAI Agents SDK       │
│  Natural Language → Tool │
└────────┬─────────────────┘
         │
         ▼
┌───────────────────────────┐
│  MCP Server (5 Tools)     │
│  - add_task               │
│  - list_tasks             │
│  - complete_task          │
│  - delete_task            │
│  - update_task            │
└────────┬──────────────────┘
         │
         ▼
┌────────────────────────────┐
│  PostgreSQL (Neon)         │
│  - users, tasks (Phase II) │
│  - conversations, messages │
└────────────────────────────┘
```

### Technology Stack

**Frontend**:
- Next.js 14+ (App Router)
- TypeScript (strict mode)
- Tailwind CSS
- OpenAI ChatKit

**Backend**:
- Python 3.11+ with FastAPI
- SQLModel ORM
- Official Python MCP SDK
- OpenAI Agents SDK

**Database**:
- Neon Serverless PostgreSQL
- SQLModel migrations

**AI**:
- OpenAI GPT-4 (via Agents SDK)

**Authentication**:
- Better Auth (from Phase II)
- JWT tokens

## Project Structure

```
Phase-III/
├── frontend/                 # Next.js application
│   ├── app/
│   │   ├── chat/            # NEW: Chat interface
│   │   ├── dashboard/       # Phase II: Task CRUD UI
│   │   └── (auth)/          # Phase II: Login/Signup
│   ├── components/
│   │   ├── chat/            # NEW: Chat components
│   │   └── task/            # Phase II: Task components
│   └── lib/
│       ├── chat-api.ts      # NEW: Chat API client
│       └── api.ts           # Phase II: Task API client
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/
│   │   │   ├── conversation.py    # NEW
│   │   │   ├── message.py         # NEW
│   │   │   ├── task.py            # Phase II
│   │   │   └── user.py            # Phase II
│   │   ├── routes/
│   │   │   ├── chat.py            # NEW
│   │   │   ├── tasks.py           # Phase II
│   │   │   └── auth.py            # Phase II
│   │   └── mcp_server/            # NEW
│   │       ├── server.py
│   │       ├── agent.py
│   │       └── tools/
│   │           ├── add_task.py
│   │           ├── list_tasks.py
│   │           ├── complete_task.py
│   │           ├── delete_task.py
│   │           └── update_task.py
│   └── requirements.txt
│
└── specs/                    # Spec-driven development
    ├── 001-phase2-fullstack-web-app/
    │   ├── spec.md
    │   ├── plan.md
    │   └── tasks.md
    └── 002-phase3-ai-chatbot/    # NEW
        ├── spec.md
        ├── plan.md
        ├── data-model.md
        ├── quickstart.md
        ├── contracts/
        │   ├── chat-api.md
        │   └── mcp-tools.md
        └── tasks.md (to be generated)
```

## Quick Start

### Prerequisites

- Phase II completed and running
- OpenAI API key (https://platform.openai.com/api-keys)
- Python 3.11+
- Node.js 18+

### Installation

**1. Clone and navigate**:
```bash
cd Phase-III
```

**2. Backend setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add:
# OPENAI_API_KEY=sk-your-key-here
```

**3. Database migration**:
```bash
# Run Phase III migration (creates conversations and messages tables)
python scripts/migrate_phase3.py
```

**4. Frontend setup**:
```bash
cd ../frontend
npm install
```

**5. Run the application**:
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**6. Access the app**:
- Frontend: http://localhost:3000
- Chat Interface: http://localhost:3000/chat
- API Docs: http://localhost:8000/docs

### Testing the Chatbot

1. Login at http://localhost:3000/login
2. Navigate to Chat: http://localhost:3000/chat
3. Try these commands:
   - "Add a task to buy groceries"
   - "Show me all my tasks"
   - "Mark task 1 as complete"
   - "Delete the meeting task"

## Specifications

All features follow spec-driven development methodology:

- **Phase III Spec**: [specs/002-phase3-ai-chatbot/spec.md](specs/002-phase3-ai-chatbot/spec.md)
- **Architecture Plan**: [specs/002-phase3-ai-chatbot/plan.md](specs/002-phase3-ai-chatbot/plan.md)
- **Data Model**: [specs/002-phase3-ai-chatbot/data-model.md](specs/002-phase3-ai-chatbot/data-model.md)
- **Chat API Contract**: [specs/002-phase3-ai-chatbot/contracts/chat-api.md](specs/002-phase3-ai-chatbot/contracts/chat-api.md)
- **MCP Tools Spec**: [specs/002-phase3-ai-chatbot/contracts/mcp-tools.md](specs/002-phase3-ai-chatbot/contracts/mcp-tools.md)
- **Quickstart Guide**: [specs/002-phase3-ai-chatbot/quickstart.md](specs/002-phase3-ai-chatbot/quickstart.md)

## Database Schema

### Phase II Tables (Existing)

- **users**: Authenticated users (Better Auth)
- **tasks**: Todo items belonging to users

### Phase III Tables (New)

- **conversations**: Chat sessions (UUID PK, user_id FK)
- **messages**: Chat messages (conversation_id FK, role: user/assistant)

All tables support cascade delete and have appropriate indexes for performance.

## Environment Variables

### Backend (.env)

```bash
# Phase II - Existing
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
JWT_SECRET_KEY=...
FRONTEND_URL=http://localhost:3000

# Phase III - New
OPENAI_API_KEY=sk-...          # Required: OpenAI API key
OPENAI_MODEL=gpt-4             # Optional: Default gpt-4
MAX_CONVERSATION_MESSAGES=50   # Optional: Message history limit
```

## Development Workflow

This project follows **Spec-Driven Development (SDD)**:

1. **Specification**: Define requirements in `specs/[feature]/spec.md`
2. **Planning**: Architecture plan in `specs/[feature]/plan.md`
3. **Design**: Data models and contracts in `specs/[feature]/`
4. **Tasks**: Generate implementation tasks with `/sp.tasks`
5. **Implementation**: Build features following tasks.md
6. **Testing**: Verify against acceptance criteria

## Next Steps

The Phase III specifications are complete. To begin implementation:

1. Review all specification files in `specs/002-phase3-ai-chatbot/`
2. Run `/sp.tasks` to generate implementation task list
3. Follow task breakdown for implementation
4. Test against acceptance criteria

See the [quickstart guide](specs/002-phase3-ai-chatbot/quickstart.md) for detailed setup instructions.

---

**Status**: Phase III specifications complete, ready for implementation
**Last Updated**: 2026-01-04
