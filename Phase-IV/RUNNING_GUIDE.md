# Running & Testing Guide - Phase III AI Chatbot

Complete guide for running and testing the full-stack AI-powered todo application.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Running the Backend](#running-the-backend)
5. [Running the Frontend](#running-the-frontend)
6. [Testing the Application](#testing-the-application)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- **PostgreSQL database** (Neon or local)
- **OpenAI API key** (for AI chat functionality)

---

## 🔧 Environment Setup

### 1. Backend Environment (.env)

Create `backend/.env` file:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://username:password@host/database?sslmode=require

# JWT Authentication
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI API (Required for Phase III)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Optional: Chat Configuration
MAX_CONVERSATION_MESSAGES=50
```

**Important Environment Variables:**
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `OPENAI_API_KEY`: Get from https://platform.openai.com/api-keys
- `OPENAI_MODEL`: Default is `gpt-4o-mini` (recommended for cost)

### 2. Frontend Environment (.env.local)

Create `frontend/.env.local` file:

```bash
cd frontend
cp .env.example .env.local  # if example exists
```

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🗄️ Database Setup

### Option 1: Neon (Recommended)

1. **Create Neon Account**: https://neon.tech
2. **Create New Project**: Click "Create Project"
3. **Get Connection String**:
   - Go to Dashboard → Connection Details
   - Copy the connection string
   - Add to `backend/.env` as `DATABASE_URL`

### Option 2: Local PostgreSQL

```bash
# Install PostgreSQL (if not installed)
# Windows: Download from https://www.postgresql.org/download/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Create database
createdb todo_db

# Update DATABASE_URL in backend/.env
DATABASE_URL=postgresql://localhost/todo_db
```

### Run Migrations

```bash
cd backend

# Run database migrations
psql $DATABASE_URL -f migrations/001_create_users_tasks.sql
psql $DATABASE_URL -f migrations/002_add_email_verified.sql
psql $DATABASE_URL -f migrations/003_add_conversations_messages.sql

# Verify tables created
psql $DATABASE_URL -c "\dt"
```

Expected tables:
- `users`
- `tasks`
- `conversations`
- `messages`

---

## 🚀 Running the Backend

### 1. Install Dependencies

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Backend Server

```bash
# Make sure you're in the backend directory
cd backend

# Start with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Backend API Endpoints:**
- Swagger Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Run Backend Tests (Optional)

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Quick test script
./run_tests.bat  # Windows
./run_tests.sh   # Mac/Linux
```

---

## 🎨 Running the Frontend

### 1. Install Dependencies

```bash
cd frontend

# Install npm packages
npm install
```

### 2. Start Frontend Development Server

```bash
# Make sure you're in the frontend directory
cd frontend

# Start Next.js dev server
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 15.5.9
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.x:3000

 ✓ Starting...
 ✓ Ready in 2.3s
```

**Frontend Pages:**
- Home: http://localhost:3000
- Login: http://localhost:3000/login
- Signup: http://localhost:3000/signup
- Dashboard: http://localhost:3000/dashboard
- Chat: http://localhost:3000/chat

### 3. Build Frontend for Production (Optional)

```bash
cd frontend

# Build production bundle
npm run build

# Start production server
npm start
```

---

## 🧪 Testing the Application

### End-to-End Testing Flow

#### 1. **User Registration**

1. Navigate to http://localhost:3000/signup
2. Fill in:
   - Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Sign Up"
4. Should redirect to dashboard

#### 2. **Login**

1. Navigate to http://localhost:3000/login
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Login"
4. Should redirect to dashboard

#### 3. **Task Management (Dashboard)**

1. **Create Task**:
   - In the "Create New Task" form
   - Title: `Buy groceries`
   - Description: `Milk, eggs, bread`
   - Click "Create Task"

2. **View Tasks**:
   - See task appear in "Your Tasks" list
   - Check statistics update

3. **Complete Task**:
   - Click checkbox on task
   - Should move to completed

4. **Delete Task**:
   - Click trash icon
   - Confirm deletion

#### 4. **AI Chat Assistant** ⭐ NEW

1. **Navigate to Chat**:
   - Click "Chat" button in dashboard header
   - Or go to http://localhost:3000/chat

2. **Send First Message**:
   ```
   Add a task to call mom tomorrow
   ```
   - Should see message appear immediately
   - AI responds with confirmation
   - New conversation created

3. **View Tool Execution**:
   - Open browser console (F12)
   - Look for: `AI executed tools: [...]`
   - Should show `add_task` tool call

4. **Continue Conversation**:
   ```
   What tasks do I have?
   ```
   - AI should list your tasks
   - Uses `list_tasks` tool

5. **Test Conversation Sidebar**:
   - Click hamburger menu (mobile) or see sidebar (desktop)
   - View conversation history
   - Click "New Conversation"
   - Start fresh chat

6. **Test Task Operations via Chat**:
   ```
   # Add multiple tasks
   "Add task to finish the report"
   "Add task to schedule meeting"

   # List tasks
   "Show me all my tasks"
   "What pending tasks do I have?"

   # Complete tasks
   "Mark task 1 as complete"
   "Complete the task about calling mom"

   # Delete tasks
   "Delete task 2"
   ```

#### 5. **Error Handling**

1. **Rate Limiting** (30 requests/min):
   - Send 31 messages rapidly
   - Should see 429 error on 31st

2. **Invalid Input**:
   - Try empty message
   - Try message > 5000 characters
   - Should see validation errors

3. **Network Error**:
   - Stop backend server
   - Try sending message
   - Should see error banner

---

## 🐛 Troubleshooting

### Backend Issues

#### **Port 8000 Already in Use**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

#### **Database Connection Failed**
```bash
# Check DATABASE_URL in .env
# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check if migrations ran
psql $DATABASE_URL -c "\dt"
```

#### **OpenAI API Errors**
```bash
# Verify API key
echo $OPENAI_API_KEY

# Test API key (Python)
python -c "import openai; openai.api_key='YOUR_KEY'; print(openai.models.list())"

# Check rate limits at: https://platform.openai.com/account/rate-limits
```

#### **Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.9+
```

### Frontend Issues

#### **Port 3000 Already in Use**
```bash
# Kill process on port 3000
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
```

#### **API Connection Failed**
```bash
# Check NEXT_PUBLIC_API_URL in .env.local
# Should be: http://localhost:8000

# Verify backend is running
curl http://localhost:8000/health

# Check browser console for CORS errors
```

#### **Build Errors**
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall node_modules
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

### Common Issues

#### **"User not authenticated" Error**
- Clear browser localStorage
- Login again
- Check JWT token expiration in backend logs

#### **Chat Messages Not Sending**
1. Check OpenAI API key in backend `.env`
2. Verify backend logs for errors
3. Check browser console for API errors
4. Ensure rate limit not exceeded

#### **Conversations Not Loading**
1. Check database has `conversations` and `messages` tables
2. Verify migrations ran successfully
3. Check backend API logs

---

## 📊 Quick Reference Commands

### Backend
```bash
# Start server
cd backend && uvicorn app.main:app --reload

# Run tests
cd backend && pytest tests/ -v

# Check health
curl http://localhost:8000/health
```

### Frontend
```bash
# Start dev server
cd frontend && npm run dev

# Build production
cd frontend && npm run build

# Start production
cd frontend && npm start
```

### Database
```bash
# Run migrations
psql $DATABASE_URL -f migrations/001_create_users_tasks.sql
psql $DATABASE_URL -f migrations/002_add_email_verified.sql
psql $DATABASE_URL -f migrations/003_add_conversations_messages.sql

# View tables
psql $DATABASE_URL -c "\dt"

# View data
psql $DATABASE_URL -c "SELECT * FROM users"
psql $DATABASE_URL -c "SELECT * FROM conversations LIMIT 5"
```

---

## 🎯 Feature Testing Checklist

Use this checklist to verify all features:

### Phase I: Authentication
- [ ] User signup
- [ ] Email validation
- [ ] User login
- [ ] JWT token generation
- [ ] Protected routes
- [ ] Logout

### Phase II: Task Management
- [ ] Create task
- [ ] List tasks
- [ ] Update task
- [ ] Complete/uncomplete task
- [ ] Delete task
- [ ] Task filtering (all/pending/completed)
- [ ] User isolation

### Phase III: AI Chat Assistant ⭐
- [ ] Send chat message
- [ ] Receive AI response
- [ ] Create new conversation
- [ ] Load conversation history
- [ ] Switch between conversations
- [ ] Delete conversation
- [ ] Tool execution (add_task, list_tasks, etc.)
- [ ] Error handling
- [ ] Rate limiting
- [ ] Responsive sidebar

---

## 📝 Next Steps

After successful testing:

1. **Deploy Backend**: Heroku, Railway, or Render
2. **Deploy Frontend**: Vercel or Netlify
3. **Setup Production DB**: Neon production tier
4. **Add Environment Variables**: In deployment platform
5. **Test Production**: Verify all features work

---

## 🆘 Getting Help

If you encounter issues:

1. Check logs:
   - Backend: Terminal running uvicorn
   - Frontend: Browser console (F12)
   - Database: `psql` connection

2. Verify environment variables are set
3. Ensure all migrations ran successfully
4. Check API endpoint documentation: http://localhost:8000/docs

---

## ✅ Success Indicators

You know everything is working when:

✓ Backend returns `{"status": "healthy"}` at `/health`
✓ Frontend loads without errors at `http://localhost:3000`
✓ Can signup/login successfully
✓ Can create/view/edit/delete tasks
✓ Can send chat messages and get AI responses
✓ Can see tool executions in console
✓ Conversations persist and load correctly
✓ No errors in backend or frontend logs

---

**Happy Testing! 🚀**
