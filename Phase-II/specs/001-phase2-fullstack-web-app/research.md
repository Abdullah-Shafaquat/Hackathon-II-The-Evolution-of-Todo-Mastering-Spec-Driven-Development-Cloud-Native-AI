# Research: Phase II Full-Stack Web Application

**Feature**: `001-phase2-fullstack-web-app` | **Date**: 2025-12-30 | **Phase**: 0 - Research
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Purpose

This research document resolves technical uncertainties and establishes implementation foundations for transforming the Phase I console todo application into a full-stack web application with authentication, database persistence, and RESTful API.

## Research Questions & Findings

### 1. Better Auth Integration with Next.js 16+ App Router

**Question**: How do we integrate Better Auth with Next.js 16+ App Router for JWT-based authentication?

**Findings**:
- **Better Auth v2** supports Next.js App Router with Server Components
- **Installation**: `npm install better-auth` in frontend/, `pip install python-jose[cryptography] passlib[bcrypt]` in backend/
- **Frontend Setup**:
  - Create `lib/auth.ts` with Better Auth client configuration
  - Use `'use client'` for auth context provider component
  - Server Components can read auth state, Client Components can modify it
- **JWT Token Flow**:
  1. Better Auth issues JWT tokens on signup/login
  2. Frontend stores tokens in httpOnly cookies (secure) or localStorage (less secure but simpler)
  3. Frontend attaches tokens in `Authorization: Bearer <token>` header for API calls
  4. Backend FastAPI middleware verifies JWT signature and extracts `user_id`
- **Shared Secret**: Both frontend and backend need `BETTER_AUTH_SECRET` environment variable (≥32 chars)
- **Token Expiry**: Configure 7-day access tokens, 30-day refresh tokens in Better Auth config

**Decision**: Use Better Auth with httpOnly cookies for production security, include token refresh logic in API client.

**Reference**: Better Auth docs, Next.js App Router authentication patterns

---

### 2. Neon PostgreSQL Connection from FastAPI

**Question**: How do we connect FastAPI to Neon Serverless PostgreSQL with SQLModel?

**Findings**:
- **Neon Connection String**: Format `postgresql://user:password@host/database?sslmode=require`
- **Copy from Neon Dashboard**: Project Settings → Connection String → Direct Connection (not pooled)
- **SQLModel Setup**:
  ```python
  from sqlmodel import create_engine, Session, SQLModel

  DATABASE_URL = os.getenv("DATABASE_URL")
  engine = create_engine(DATABASE_URL, echo=True)  # echo=True for dev logging

  def get_session():
      with Session(engine) as session:
          yield session
  ```
- **Connection Pooling**: SQLModel uses SQLAlchemy engine with default pool (5-20 connections)
- **SSL Requirement**: Neon requires `sslmode=require` parameter in connection string
- **Schema Creation**: Call `SQLModel.metadata.create_all(engine)` on startup to create tables
- **Migrations**: For Phase II, schema is stable enough to use `create_all()` - no Alembic needed yet

**Decision**: Use direct Neon connection with SQLModel, create_all() for schema initialization, add proper connection pool configuration.

**Reference**: Neon documentation, SQLModel docs, FastAPI database tutorial

---

### 3. JWT Verification Middleware in FastAPI

**Question**: How do we implement JWT verification middleware for protected routes?

**Findings**:
- **python-jose Library**: Industry standard for JWT in Python
  ```python
  from jose import jwt, JWTError

  def verify_token(token: str) -> dict:
      try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
          user_id = payload.get("sub")
          if user_id is None:
              raise HTTPException(401, "Invalid token")
          return {"user_id": user_id}
      except JWTError:
          raise HTTPException(401, "Invalid token")
  ```
- **Dependency Injection**:
  ```python
  from fastapi import Depends, HTTPException
  from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

  security = HTTPBearer()

  def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
      return verify_token(credentials.credentials)
  ```
- **Protected Routes**: Add `current_user: dict = Depends(get_current_user)` to route parameters
- **User Isolation**: Extract `user_id` from JWT, filter database queries: `session.query(Task).filter(Task.user_id == current_user["user_id"])`

**Decision**: Use python-jose with HTTPBearer security scheme, implement get_current_user dependency for all protected routes.

**Reference**: FastAPI security documentation, python-jose docs

---

### 4. CORS Configuration for Separate Frontend/Backend Deployment

**Question**: How do we configure CORS when frontend (Vercel) and backend (Railway/Render) are on different domains?

**Findings**:
- **FastAPI CORS Middleware**:
  ```python
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=[os.getenv("FRONTEND_URL")],  # e.g., "https://my-app.vercel.app"
      allow_credentials=True,  # Allow cookies/auth headers
      allow_methods=["*"],     # Allow all HTTP methods
      allow_headers=["*"],     # Allow all headers including Authorization
  )
  ```
- **Environment Variables**:
  - Backend: `FRONTEND_URL` = frontend domain (set in Railway/Render dashboard)
  - Frontend: `NEXT_PUBLIC_API_URL` = backend domain (set in Vercel dashboard)
- **Credentials**: `allow_credentials=True` required for JWT tokens in Authorization header
- **Preflight Requests**: CORS middleware handles OPTIONS requests automatically

**Decision**: Configure CORSMiddleware with FRONTEND_URL environment variable, allow credentials for auth headers.

**Reference**: FastAPI CORS documentation, MDN CORS guide

---

### 5. Next.js 16+ App Router Route Organization

**Question**: What's the best way to organize routes in Next.js App Router for auth and protected pages?

**Findings**:
- **Route Groups**: Use `(auth)` folder for grouping without affecting URL
  - `app/(auth)/login/page.tsx` → URL: `/login`
  - `app/(auth)/signup/page.tsx` → URL: `/signup`
  - Benefits: Shared layouts, logical grouping, no URL nesting
- **Protected Routes**: Create `app/dashboard/layout.tsx` with auth guard:
  ```tsx
  export default function DashboardLayout({ children }) {
    // Check auth state, redirect to /login if not authenticated
    return <div>{children}</div>
  }
  ```
- **Server Components vs Client Components**:
  - Use Server Components by default (better performance, no JS bundle)
  - Use `'use client'` only for interactivity (forms, buttons, state)
  - Auth context provider MUST be Client Component
- **Metadata**: Server Components can export `metadata` object for SEO

**Decision**: Use route groups `(auth)` for public pages, dashboard layout with auth guard for protected routes, minimize Client Components.

**Reference**: Next.js App Router documentation, route groups guide

---

### 6. Tailwind CSS Configuration for Responsive Design

**Question**: How do we configure Tailwind for mobile-first responsive design?

**Findings**:
- **Default Breakpoints**: Tailwind uses mobile-first breakpoints
  - `sm:` 640px (tablet)
  - `md:` 768px (tablet landscape)
  - `lg:` 1024px (desktop)
  - `xl:` 1280px (large desktop)
- **Mobile-First Approach**: Write base styles for mobile, add `sm:`, `md:`, `lg:` prefixes for larger screens
  ```jsx
  <div className="w-full sm:w-96 lg:w-1/2">  // Full width mobile, fixed width tablet, half desktop
  ```
- **Touch Targets**: Minimum 44px (11 rem) for buttons on mobile
  ```jsx
  <button className="h-11 px-4 sm:h-10">  // Larger touch target on mobile
  ```
- **Custom Configuration**: Can extend `tailwind.config.js` with custom colors, spacing, breakpoints
- **Dark Mode**: Use `dark:` prefix with `class` strategy in config

**Decision**: Use Tailwind default breakpoints with mobile-first approach, ensure ≥44px touch targets, skip dark mode for Phase II MVP.

**Reference**: Tailwind CSS documentation, responsive design guide

---

### 7. Environment Variables Management Across Services

**Question**: How do we manage environment variables for frontend, backend, and database consistently?

**Findings**:
- **Frontend (.env.local)**:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000  # Dev: localhost, Prod: backend domain
  BETTER_AUTH_SECRET=your-secret-key-min-32-chars
  ```
  - `NEXT_PUBLIC_*` prefix exposes to browser (use for API URL only)
  - Non-prefixed vars are server-side only (use for auth secret)
- **Backend (.env)**:
  ```
  DATABASE_URL=postgresql://user:password@host/database?sslmode=require
  BETTER_AUTH_SECRET=your-secret-key-min-32-chars  # MUST match frontend
  FRONTEND_URL=http://localhost:3000  # Dev: localhost, Prod: Vercel domain
  ```
- **Neon Database**: No .env needed - connection string copied from dashboard
- **Deployment**:
  - Vercel: Set environment variables in Project Settings → Environment Variables
  - Railway/Render: Set environment variables in service dashboard
  - Neon: Connection string remains same for prod, use Neon branches for dev/staging
- **Security**:
  - Never commit .env files (add to .gitignore)
  - Create .env.example templates with placeholder values
  - Use strong random values for BETTER_AUTH_SECRET (generate with `openssl rand -base64 32`)

**Decision**: Create .env.example templates, use NEXT_PUBLIC_ prefix for browser-exposed vars, sync BETTER_AUTH_SECRET between frontend and backend.

**Reference**: Next.js environment variables docs, FastAPI settings management, Vercel docs

---

### 8. Database Schema Design for User Isolation

**Question**: How do we design database schema to ensure user isolation and efficient queries?

**Findings**:
- **Users Table** (managed by Better Auth):
  ```sql
  CREATE TABLE users (
      id TEXT PRIMARY KEY,  -- Better Auth generates UUID as text
      email TEXT UNIQUE NOT NULL,
      name TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- **Tasks Table** (our main entity):
  ```sql
  CREATE TABLE tasks (
      id SERIAL PRIMARY KEY,
      user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(200) NOT NULL,
      description TEXT,
      completed BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- **Critical Indexes**:
  ```sql
  CREATE INDEX idx_tasks_user_id ON tasks(user_id);  -- CRITICAL for user queries
  CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);  -- For filtering
  CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);  -- For sorting
  ```
- **Cascade Delete**: When user deleted, all their tasks deleted automatically
- **User Isolation Pattern**: Always filter queries by `user_id` from JWT:
  ```python
  tasks = session.query(Task).filter(Task.user_id == current_user["user_id"]).all()
  ```

**Decision**: Use TEXT for user_id (Better Auth UUIDs), SERIAL for task_id, create indexes on user_id and user_id+completed, enforce cascade delete.

**Reference**: PostgreSQL documentation, SQLModel relationship patterns, database indexing best practices

---

### 9. Error Handling Strategy Across Stack

**Question**: How do we handle errors consistently across frontend, backend, and database layers?

**Findings**:
- **Frontend Error Handling**:
  ```tsx
  try {
    const response = await api.post('/tasks', taskData)
    toast.success('Task created!')
  } catch (error) {
    if (error.response?.status === 401) {
      router.push('/login')  // Redirect on auth failure
    } else {
      toast.error(error.response?.data?.detail || 'Something went wrong')
    }
  }
  ```
- **Backend Error Responses**:
  ```python
  from fastapi import HTTPException

  # Validation error
  raise HTTPException(status_code=400, detail="Title is required")

  # Auth error
  raise HTTPException(status_code=401, detail="Invalid or expired token")

  # Not found
  raise HTTPException(status_code=404, detail="Task not found")

  # Server error (catch database errors, log details, return generic message)
  try:
      session.execute(query)
  except Exception as e:
      logger.error(f"Database error: {e}")
      raise HTTPException(status_code=500, detail="Internal server error")
  ```
- **Database Errors**: Catch SQLAlchemy exceptions, log full details server-side, return generic 500 to client
- **Pydantic Validation**: FastAPI auto-converts Pydantic validation errors to 422 with field-specific messages

**Decision**: Use HTTPException with appropriate status codes, log detailed errors server-side, return user-friendly messages to client, implement global error boundary in React.

**Reference**: FastAPI error handling docs, React error boundaries, HTTP status codes

---

### 10. Deployment Strategy for Monorepo

**Question**: How do we deploy a monorepo with separate frontend and backend to different platforms?

**Findings**:
- **Frontend Deployment (Vercel)**:
  - Connect GitHub repo to Vercel
  - Set Root Directory to `frontend/` in project settings
  - Configure build command: `npm run build` (Next.js default)
  - Set environment variables in Vercel dashboard
  - Automatic deployments on git push
- **Backend Deployment (Railway)**:
  - Create new Railway project, connect same GitHub repo
  - Set Root Directory to `backend/` in service settings
  - Configure start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Set environment variables in Railway dashboard
  - Automatic deployments on git push
- **Alternative Backend Hosts**: Render, Fly.io, Heroku (all support monorepo root directory)
- **Neon Database**: No deployment needed - always accessible via connection string
- **Monorepo Git Strategy**:
  - Keep both frontend/ and backend/ in same repo
  - Vercel watches changes in frontend/, Railway watches changes in backend/
  - Shared specs/ directory visible to both deployments

**Decision**: Deploy frontend to Vercel with root=frontend/, deploy backend to Railway with root=backend/, use Neon connection string in both.

**Reference**: Vercel monorepo docs, Railway documentation, deployment best practices

---

## Resolved Uncertainties

All research questions resolved with zero `NEEDS CLARIFICATION` markers remaining. Key technical decisions documented for:

1. ✅ Better Auth integration with Next.js App Router
2. ✅ Neon PostgreSQL connection with SQLModel
3. ✅ JWT verification middleware in FastAPI
4. ✅ CORS configuration for cross-origin requests
5. ✅ Next.js route organization with route groups
6. ✅ Tailwind responsive design configuration
7. ✅ Environment variables management
8. ✅ Database schema with user isolation
9. ✅ Error handling across full stack
10. ✅ Monorepo deployment strategy

## Dependencies Verified

- ✅ **Better Auth**: Compatible with Next.js 16+ App Router
- ✅ **Neon PostgreSQL**: Free tier sufficient for hackathon (500MB storage, 0.5 compute units)
- ✅ **FastAPI**: Latest version (0.100+) supports async with SQLModel
- ✅ **SQLModel**: Compatible with PostgreSQL 16 (Neon version)
- ✅ **Vercel**: Supports Next.js 16+ with automatic deployments
- ✅ **Railway**: Supports Python 3.11+ with FastAPI

## Next Steps

1. ✅ Research complete - proceed to Phase 1 (Design)
2. → Create `data-model.md` with SQLModel class definitions
3. → Create API contracts in `contracts/` directory
4. → Create `quickstart.md` with setup instructions
5. → Run `/sp.tasks` to generate implementation tasks from plan

---

**Research Status**: ✅ COMPLETE - All technical uncertainties resolved
**Last Updated**: 2025-12-30
