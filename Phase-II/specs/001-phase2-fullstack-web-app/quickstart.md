# Quickstart Guide: Phase II Full-Stack Web Application

**Feature**: `001-phase2-fullstack-web-app` | **Date**: 2025-12-30
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md) | [data-model.md](./data-model.md)

## Overview

This guide provides step-by-step instructions to set up the Phase II full-stack todo web application from scratch, including frontend (Next.js 16+), backend (FastAPI), and database (Neon PostgreSQL) setup.

**Estimated Time**: 30-45 minutes

---

## Prerequisites

Ensure you have the following installed:

- **Node.js 18+**: Download from [nodejs.org](https://nodejs.org)
- **Python 3.11+**: Download from [python.org](https://python.org)
- **Git**: Download from [git-scm.com](https://git-scm.com)
- **Code Editor**: VS Code recommended
- **Neon Account**: Free account at [neon.tech](https://neon.tech)

**Verify Installations**:
```bash
node --version  # Should show v18.x or higher
python --version  # Should show 3.11.x or higher
git --version  # Any recent version
```

---

## Step 1: Clone Repository and Setup Monorepo

```bash
# Navigate to your projects directory
cd ~/projects  # or your preferred location

# Clone the repository (replace with your repo URL)
git clone <repository-url>
cd Phase-II

# Verify monorepo structure
ls -la
# Should see: frontend/, backend/, specs/, .specify/, etc.
```

---

## Step 2: Database Setup (Neon PostgreSQL)

### 2.1 Create Neon Project

1. **Sign up** at [neon.tech](https://neon.tech) (free tier)
2. **Create new project**:
   - Project Name: `phase2-todo-app`
   - PostgreSQL Version: 16 (latest)
   - Region: Choose closest to you
3. **Create database**:
   - Database Name: `todoapp`
   - Leave other settings as default

### 2.2 Get Connection String

1. In Neon dashboard, navigate to **Connection Details**
2. Copy the **Connection String** (Direct Connection, not pooled)
3. Format: `postgresql://user:password@host/database?sslmode=require`

**Example**:
```
postgresql://alex:AbCd1234@ep-cool-sound-123456.us-east-2.aws.neon.tech/todoapp?sslmode=require
```

**Save this connection string** - you'll need it for backend configuration.

### 2.3 Database Schema Creation

**Note**: Schema will be created automatically by SQLModel when backend starts. No manual SQL execution needed.

---

## Step 3: Backend Setup (FastAPI)

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation (should show (venv) in prompt)
```

### 3.3 Install Dependencies

Create `requirements.txt`:

```bash
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
pydantic[email]==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
asyncpg==0.29.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
EOF

# Install all dependencies
pip install -r requirements.txt
```

### 3.4 Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
# ↑ Replace with your Neon connection string from Step 2.2

# Authentication Configuration
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long-replace-this
# ↑ Generate with: openssl rand -base64 32

# CORS Configuration
FRONTEND_URL=http://localhost:3000
# ↑ For development; change to Vercel URL in production

# Application Configuration
PORT=8000
EOF
```

**Generate BETTER_AUTH_SECRET**:
```bash
# Generate strong random secret
openssl rand -base64 32
# Copy output and replace placeholder in .env
```

### 3.5 Create .env.example Template

```bash
cp .env .env.example

# Edit .env.example to remove sensitive values
sed -i 's/=postgresql.*/=postgresql:\/\/user:password@host\/database?sslmode=require/' .env.example
sed -i 's/=your-secret.*/=your-secret-key-min-32-characters-long/' .env.example
```

### 3.6 Verify Backend Setup

```bash
# Check Python packages installed
pip list | grep fastapi
pip list | grep sqlmodel

# Should see:
# fastapi      0.104.1
# sqlmodel     0.0.14
```

---

## Step 4: Frontend Setup (Next.js 16+)

### 4.1 Navigate to Frontend Directory

```bash
cd ../frontend  # From backend/, go to frontend/
```

### 4.2 Install Node Dependencies

```bash
# Install Next.js and dependencies
npm install next@latest react@latest react-dom@latest
npm install --save-dev typescript @types/react @types/node

# Install additional dependencies
npm install tailwindcss postcss autoprefixer
npm install better-auth
npm install react-hook-form zod @hookform/resolvers

# Initialize Tailwind CSS
npx tailwindcss init -p
```

### 4.3 Configure TypeScript

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### 4.4 Configure Tailwind CSS

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 4.5 Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
cat > .env.local << EOF
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
# ↑ For development; change to backend URL in production

# Better Auth Secret (MUST match backend)
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long-replace-this
# ↑ Use the SAME secret from backend/.env
EOF
```

**CRITICAL**: `BETTER_AUTH_SECRET` must be identical in both frontend and backend `.env` files.

### 4.6 Create .env.example Template

```bash
cp .env.local .env.example

# Edit to remove sensitive values
sed -i 's/=your-secret.*/=your-secret-key-min-32-characters-long/' .env.example
```

### 4.7 Create package.json Scripts

Update `frontend/package.json` to include:

```json
{
  "name": "phase2-todo-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "better-auth": "^1.0.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

### 4.8 Verify Frontend Setup

```bash
# Check Node modules installed
ls node_modules | grep next
ls node_modules | grep tailwindcss

# Should see directories: next, tailwindcss, etc.
```

---

## Step 5: Running the Application Locally

### 5.1 Start Backend Server

```bash
# In backend/ directory with venv activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Verify Backend**:
- Open browser: `http://localhost:8000/docs`
- You should see FastAPI Swagger UI with API documentation
- Test health endpoint: `http://localhost:8000/health` should return `{"status": "ok"}`

### 5.2 Start Frontend Development Server

```bash
# In NEW terminal window, navigate to frontend/
cd frontend

# Start Next.js development server
npm run dev

# You should see:
# ▲ Next.js 14.0.0
# - Local:        http://localhost:3000
# - Ready in 2.3s
```

**Verify Frontend**:
- Open browser: `http://localhost:3000`
- You should see the landing page (or default Next.js page if not implemented yet)

---

## Step 6: Verify Full Stack Integration

### 6.1 Test Authentication Flow

1. **Navigate to** `http://localhost:3000/signup`
2. **Create test account**:
   - Email: `test@example.com`
   - Password: `TestPassword123!`
   - Name: `Test User`
3. **Submit form** → should redirect to dashboard
4. **Check backend logs** → should see database queries and JWT token generation

### 6.2 Test Task CRUD Operations

1. **Create task**: Click "Add Task" button
   - Title: `Test Task`
   - Description: `Testing Phase II implementation`
2. **View tasks**: Task should appear in list
3. **Complete task**: Click checkbox → task should show as completed
4. **Edit task**: Click edit button → update title or description
5. **Delete task**: Click delete button → confirm → task removed

### 6.3 Verify Database Persistence

1. **Create several tasks** in the UI
2. **Stop frontend server** (Ctrl+C)
3. **Restart frontend** (`npm run dev`)
4. **Navigate to dashboard** → tasks should still be there (persisted in database)

### 6.4 Test User Isolation

1. **Logout** from first account
2. **Create second account**: `test2@example.com`
3. **Check dashboard** → should see NO tasks (tasks from first account not visible)
4. **Create tasks** for second account
5. **Switch back to first account** → should only see first account's tasks

---

## Step 7: Development Workflow

### 7.1 Typical Development Session

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Git operations, file edits, etc.
```

### 7.2 Making Code Changes

**Backend Changes**:
- Edit files in `backend/app/`
- Server auto-reloads (thanks to `--reload` flag)
- Check terminal for errors

**Frontend Changes**:
- Edit files in `frontend/app/` or `frontend/components/`
- Next.js auto-reloads in browser (Fast Refresh)
- Check browser console for errors

**Database Schema Changes**:
- Edit SQLModel models in `backend/app/models/`
- Delete database tables (Neon dashboard) or drop database
- Restart backend → tables recreated with new schema

### 7.3 Common Development Commands

```bash
# Backend
pip install <package>  # Install new Python package
pip freeze > requirements.txt  # Update requirements
python -m pytest  # Run backend tests (if implemented)

# Frontend
npm install <package>  # Install new Node package
npm run build  # Test production build
npm run lint  # Run ESLint

# Database
# View data: Neon dashboard → SQL Editor → SELECT * FROM tasks;
# Reset data: Neon dashboard → SQL Editor → DELETE FROM tasks;
```

---

## Step 8: Deployment (Production)

### 8.1 Deploy Frontend to Vercel

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Phase II implementation"
   git push origin master
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - **Root Directory**: `frontend/`
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Environment Variables**:
     - `NEXT_PUBLIC_API_URL`: Your backend URL (see Step 8.2)
     - `BETTER_AUTH_SECRET`: Same secret from `.env`

3. **Deploy**: Click "Deploy" button

4. **Get Frontend URL**: Copy Vercel deployment URL (e.g., `https://my-app.vercel.app`)

### 8.2 Deploy Backend to Railway

1. **Create Railway account** at [railway.app](https://railway.app)

2. **Create new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - **Root Directory**: `backend/`

3. **Configure build**:
   - Railway auto-detects Python
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables** (Railway dashboard → Variables):
   ```
   DATABASE_URL=<your-neon-connection-string>
   BETTER_AUTH_SECRET=<same-secret-as-frontend>
   FRONTEND_URL=<your-vercel-url-from-step-8.1>
   PORT=8000
   ```

5. **Deploy**: Railway automatically deploys

6. **Get Backend URL**: Copy Railway deployment URL (e.g., `https://my-backend.railway.app`)

7. **Update Vercel**: Go back to Vercel → Environment Variables → Update `NEXT_PUBLIC_API_URL` to Railway URL → Redeploy

### 8.3 Verify Production Deployment

1. **Visit frontend URL** (Vercel)
2. **Create account** in production
3. **Create tasks** and verify persistence
4. **Check backend health**: `<railway-url>/health`
5. **Check API docs**: `<railway-url>/docs`

---

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'app'"**
- **Solution**: Ensure you're in `backend/` directory and venv is activated
- **Fix**: `cd backend && source venv/bin/activate`

**Error: "could not connect to server: Connection refused"**
- **Solution**: Check `DATABASE_URL` in `.env` is correct
- **Fix**: Copy connection string from Neon dashboard again

**Error: "JWT decode error"**
- **Solution**: `BETTER_AUTH_SECRET` mismatch between frontend and backend
- **Fix**: Ensure both `.env` files have identical secret

### Frontend Issues

**Error: "Module not found: Can't resolve '@/lib/types'"**
- **Solution**: Create missing file or check `tsconfig.json` paths
- **Fix**: Ensure `"@/*": ["./*"]` in paths

**Error: "Failed to fetch" when calling API**
- **Solution**: Backend not running or wrong `NEXT_PUBLIC_API_URL`
- **Fix**: Start backend and verify URL in `.env.local`

**Error: "CORS policy: No 'Access-Control-Allow-Origin' header"**
- **Solution**: Backend CORS not configured for frontend URL
- **Fix**: Update `FRONTEND_URL` in backend `.env`

### Database Issues

**Error: "relation 'tasks' does not exist"**
- **Solution**: Tables not created yet
- **Fix**: Restart backend → SQLModel creates tables automatically

**Error: "no pg_hba.conf entry for host"**
- **Solution**: Connection string missing `?sslmode=require`
- **Fix**: Add `?sslmode=require` to end of `DATABASE_URL`

---

## Next Steps

After completing this quickstart, you should have:

- ✅ Neon PostgreSQL database configured
- ✅ FastAPI backend running locally (port 8000)
- ✅ Next.js frontend running locally (port 3000)
- ✅ Full authentication flow working
- ✅ Task CRUD operations working
- ✅ User isolation verified
- ✅ (Optional) Production deployment on Vercel + Railway

**Ready for Implementation**:
1. Run `/sp.tasks` to generate implementation tasks
2. Follow task-driven development workflow
3. Implement features incrementally (P1 → P2 → P3)

---

## Useful Resources

- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **SQLModel Docs**: [sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com)
- **Neon Docs**: [neon.tech/docs](https://neon.tech/docs)
- **Better Auth Docs**: [better-auth.com/docs](https://better-auth.com/docs)
- **Tailwind CSS Docs**: [tailwindcss.com/docs](https://tailwindcss.com/docs)

---

**Quickstart Status**: ✅ COMPLETE
**Last Updated**: 2025-12-30
