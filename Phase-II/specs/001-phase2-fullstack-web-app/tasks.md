# Implementation Tasks: Phase II Full-Stack Web Application

**Feature**: `001-phase2-fullstack-web-app` | **Date**: 2025-12-30
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md) | [data-model.md](./data-model.md)

## Overview

This document contains dependency-ordered implementation tasks for transforming the Phase I console todo application into a full-stack web application. Tasks are organized by user story to enable independent, incremental delivery.

**Total Tasks**: 62 tasks
**Estimated Timeline**: 2-3 weeks (hackathon schedule)
**Testing**: Optional for Phase II (not included in task count)

---

## Implementation Strategy

### MVP First (User Story 1 - P1)
Complete User Story 1 to deliver minimum viable product: user registration + first task creation with database persistence.

### Incremental Delivery (User Stories 2-4)
Build remaining features story-by-story, each delivering independent value and being fully testable.

### Parallel Execution Opportunities
Tasks marked with `[P]` can be executed in parallel when working with multiple developers or sessions.

---

## Phase 1: Environment Setup (5 tasks)

**Goal**: Initialize monorepo structure, install dependencies, configure development environment

**Prerequisites**: None (starting from scratch)

### Tasks

- [ ] T001 Create monorepo directory structure per plan.md (frontend/, backend/, specs/, .specify/, history/)
- [ ] T002 [P] Initialize frontend with Next.js 16+ in frontend/ directory: `npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir`
- [ ] T003 [P] Initialize backend Python environment in backend/ directory: create virtual environment, install FastAPI/SQLModel/dependencies per quickstart.md
- [ ] T004 Create environment variable templates: frontend/.env.example and backend/.env.example with all required variables (NEXT_PUBLIC_API_URL, DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL)
- [ ] T005 [P] Configure .gitignore for both frontend/ (node_modules/, .env.local, .next/) and backend/ (venv/, .env, __pycache__/, *.pyc)

**Completion Criteria**:
- ✅ Directory structure matches plan.md project structure
- ✅ Next.js 16+ with App Router initialized (verify `app/` directory exists)
- ✅ Python virtual environment created with all dependencies installed (verify `pip list`)
- ✅ Environment variable templates documented
- ✅ Git configured to ignore sensitive files

---

## Phase 2: Database & Backend Foundation (9 tasks)

**Goal**: Set up Neon PostgreSQL database, SQLModel models, database connection, and core configuration

**Prerequisites**: Phase 1 complete

### Tasks

- [ ] T006 Create Neon PostgreSQL database per quickstart.md Step 2 and obtain connection string
- [ ] T007 Create backend/app/config.py with Pydantic BaseSettings for DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL, PORT environment variables
- [ ] T008 Create backend/app/database.py with SQLModel engine creation, session management, and get_session() dependency per data-model.md
- [ ] T009 [P] Create backend/app/models/__init__.py to export User and Task models
- [ ] T010 [P] Create backend/app/models/user.py with User SQLModel class per data-model.md (id: str, email: str, name: Optional[str], password_hash: str, created_at, updated_at)
- [ ] T011 [P] Create backend/app/models/task.py with Task SQLModel class per data-model.md (id: Optional[int], user_id: str FK, title: str, description: Optional[str], completed: bool, created_at, updated_at)
- [ ] T012 [P] Create backend/app/schemas/__init__.py to export all Pydantic schemas
- [ ] T013 [P] Create backend/app/schemas/auth.py with SignupRequest, LoginRequest, AuthResponse, UserResponse per data-model.md
- [ ] T014 [P] Create backend/app/schemas/task.py with TaskCreate, TaskUpdate, TaskResponse, TaskListResponse per data-model.md

**Completion Criteria**:
- ✅ Neon database created and connection string obtained
- ✅ Configuration management with Pydantic BaseSettings
- ✅ Database connection established (test with SQLModel.metadata.create_all())
- ✅ User and Task models defined with proper relationships and constraints
- ✅ All Pydantic schemas match API contracts in contracts/auth-api.md and contracts/tasks-api.md

---

## Phase 3: Backend Authentication & Middleware (8 tasks)

**Goal**: Implement JWT authentication, CORS configuration, and protective middleware

**Prerequisites**: Phase 2 complete

### Tasks

- [ ] T015 Create backend/app/middleware/__init__.py to export auth and CORS middleware
- [ ] T016 Create backend/app/middleware/cors.py with CORSMiddleware configuration allowing FRONTEND_URL with credentials per research.md Finding #4
- [ ] T017 Create backend/app/middleware/auth.py with JWT verification functions: verify_token(token: str) -> dict using python-jose per research.md Finding #3
- [ ] T018 Create backend/app/middleware/auth.py get_current_user(credentials: HTTPAuthorizationCredentials) dependency using HTTPBearer security scheme
- [ ] T019 [P] Create backend/app/routes/__init__.py to export all route modules
- [ ] T020 Create backend/app/main.py FastAPI application with CORS middleware, startup event to create database tables (SQLModel.metadata.create_all()), and /health endpoint returning {"status": "ok"}
- [ ] T021 Test backend startup: `uvicorn app.main:app --reload --port 8000` and verify /health endpoint returns 200 OK
- [ ] T022 Test database table creation: verify Neon dashboard shows users and tasks tables with correct schema and indexes

**Completion Criteria**:
- ✅ CORS configured to allow frontend domain with credentials
- ✅ JWT verification middleware implemented with python-jose
- ✅ get_current_user dependency extracts user_id from JWT
- ✅ FastAPI application starts without errors
- ✅ /health endpoint accessible
- ✅ Database tables created automatically on startup

---

## Phase 4: User Story 1 - New User Registration and First Task (P1 - MVP) (13 tasks)

**Goal**: Enable new user to register account, log in automatically, and create their first task

**Why P1**: Foundation of entire application - delivers minimum viable product

**Independent Test**: Complete signup flow with valid email/password and create one task. Verify persistence by logging out and back in.

**Prerequisites**: Phases 1-3 complete

### Backend Tasks (User Story 1)

- [ ] T023 [US1] Create backend/app/routes/auth.py with POST /api/auth/signup endpoint: validate SignupRequest, hash password with passlib bcrypt, create User in database, generate JWT tokens, return AuthResponse per contracts/auth-api.md
- [ ] T024 [US1] Create backend/app/routes/auth.py POST /api/auth/login endpoint: validate LoginRequest, verify password hash, generate JWT tokens with 7-day access + 30-day refresh per research.md Finding #1, return AuthResponse
- [ ] T025 [US1] Add authentication routes to backend/app/main.py FastAPI router with prefix="/api/auth"
- [ ] T026 [US1] Create backend/app/routes/tasks.py with POST /api/tasks endpoint (protected): validate TaskCreate, extract user_id from get_current_user dependency, create Task in database with user isolation, return TaskResponse per contracts/tasks-api.md
- [ ] T027 [US1] Create backend/app/routes/tasks.py GET /api/tasks endpoint (protected): extract user_id, query tasks filtered by user_id, sort by created_at DESC, return TaskListResponse with statistics (total, completed, pending)
- [ ] T028 [US1] Create backend/app/routes/tasks.py GET /api/tasks/{id} endpoint (protected): verify task belongs to authenticated user (403 if not), return TaskResponse or 404
- [ ] T029 [US1] Add task routes to backend/app/main.py FastAPI router with prefix="/api/tasks"

**Completion Criteria (Backend)**:
- ✅ User can register with valid email/password (201 Created with JWT tokens)
- ✅ User can login with credentials (200 OK with JWT tokens)
- ✅ Authenticated user can create task (201 Created)
- ✅ Authenticated user can list their tasks (200 OK)
- ✅ User isolation enforced (403 when accessing other user's tasks)

### Frontend Tasks (User Story 1)

- [ ] T030 [P] [US1] Create frontend/lib/types.ts with all TypeScript interfaces per data-model.md (User, SignupRequest, LoginRequest, AuthResponse, Task, TaskCreate, TaskListResponse, APIError)
- [ ] T031 [P] [US1] Create frontend/lib/api.ts with API client class: baseURL from NEXT_PUBLIC_API_URL, methods for signup(), login(), createTask(), listTasks() with automatic JWT token attachment from localStorage per contracts/
- [ ] T032 [US1] Create frontend/app/(auth)/signup/page.tsx Server Component with SignupForm: email input (EmailStr validation), password input (min 8 chars), optional name input, submit calls API signup(), stores tokens in localStorage, redirects to /dashboard
- [ ] T033 [US1] Create frontend/app/(auth)/login/page.tsx Server Component with LoginForm: email/password inputs, remember_me checkbox, submit calls API login(), stores tokens, redirects to /dashboard
- [ ] T034 [US1] Create frontend/app/dashboard/page.tsx with authentication check: if no token redirect to /login, else fetch tasks from API and display TaskList component, include "Add Task" button
- [ ] T035 [US1] Create frontend/components/task/TaskForm.tsx Client Component for task creation: title input (1-200 chars validation), description textarea (optional), submit calls API createTask(), shows success toast, refreshes task list
- [ ] T036 [US1] Create frontend/components/task/TaskList.tsx Client Component: map tasks to TaskItem components, show empty state "No tasks yet. Create your first task!" when tasks.length === 0, display statistics (e.g., "2 of 5 tasks completed (40%)")

**Completion Criteria (Frontend)**:
- ✅ User can navigate to /signup and create account
- ✅ After signup, user automatically logged in and redirected to /dashboard
- ✅ Dashboard shows empty state for new user
- ✅ User can create first task via TaskForm
- ✅ Task appears in TaskList immediately after creation
- ✅ User can logout and login again - task still visible (persistence test)

**US1 Acceptance Test**:
1. Visit /signup → enter user@example.com, SecurePass123!, John Doe → account created, auto-login, see dashboard
2. Click "Add Task" → enter "Buy groceries", "Milk, eggs, bread" → task appears in list
3. Logout → login with same credentials → task still visible

---

## Phase 5: User Story 4 - Secure Session Management (P2) (6 tasks)

**Goal**: Implement logout, session expiration handling, protected route guards, "remember me" functionality

**Why P2**: Security critical before public deployment, builds on US1 authentication foundation

**Independent Test**: Test login with remember me, logout, session expiry, unauthenticated access attempts

**Prerequisites**: Phase 4 (US1) complete

### Tasks

- [ ] T037 [US4] Create backend/app/routes/auth.py POST /api/auth/logout endpoint (protected): clear session (stateless JWT, client-side deletion), return success message per contracts/auth-api.md
- [ ] T038 [US4] Create backend/app/routes/auth.py GET /api/auth/me endpoint (protected): extract user from get_current_user, return UserResponse with profile data
- [ ] T039 [US4] Update frontend/lib/api.ts with logout() method calling POST /api/auth/logout, deleting tokens from localStorage, and getCurrentUser() method calling GET /api/auth/me
- [ ] T040 [US4] Create frontend/components/auth/AuthGuard.tsx Client Component: check for JWT token in localStorage, if missing redirect to /login with message "Please log in to continue", if present verify with /api/auth/me
- [ ] T041 [US4] Wrap frontend/app/dashboard/page.tsx with AuthGuard component to protect dashboard route
- [ ] T042 [US4] Add Logout button to frontend/app/dashboard/page.tsx: onClick calls API logout(), clears localStorage, redirects to /login with message "Successfully logged out"

**Completion Criteria**:
- ✅ User can logout from dashboard (tokens cleared, redirect to login)
- ✅ Unauthenticated user accessing /dashboard redirected to /login
- ✅ AuthGuard protects dashboard route
- ✅ "Remember me" functionality stores tokens persistently
- ✅ Session expiration handled gracefully (401 → redirect to login)

**US4 Acceptance Test**:
1. Login with "Remember me" → close browser → return within 7 days → still logged in
2. Click Logout → session terminates, redirect to login
3. Direct access to /dashboard without login → redirect to /login with message
4. Token expires → any action shows "Session expired" and redirects to login

---

## Phase 6: User Story 2 - Existing User Task Management (P2) (10 tasks)

**Goal**: Enable full task lifecycle management: view all tasks, mark complete/incomplete, edit task details, delete tasks, filter by status

**Why P2**: Extends MVP to complete task management, enables users to track progress

**Independent Test**: Create user with 3-5 tasks, test all CRUD operations and filtering

**Prerequisites**: Phase 4 (US1) complete (note: can be parallel with Phase 5/US4 if working with multiple developers)

### Backend Tasks (User Story 2)

- [ ] T043 [P] [US2] Create backend/app/routes/tasks.py PUT /api/tasks/{id} endpoint (protected): validate TaskUpdate, verify user owns task (403 if not), update fields, set updated_at to current timestamp, return TaskResponse per contracts/tasks-api.md
- [ ] T044 [P] [US2] Create backend/app/routes/tasks.py PATCH /api/tasks/{id}/complete endpoint (protected): verify ownership, toggle completed status (false→true or true→false), update updated_at, return TaskResponse
- [ ] T045 [P] [US2] Create backend/app/routes/tasks.py DELETE /api/tasks/{id} endpoint (protected): verify ownership (403 if not), delete task from database, return 204 No Content per contracts/tasks-api.md
- [ ] T046 [US2] Update GET /api/tasks endpoint to support query parameters: filter (all/pending/completed), sort (created_at/updated_at/title), order (asc/desc) per contracts/tasks-api.md

**Completion Criteria (Backend)**:
- ✅ User can update task title and description (PUT /api/tasks/{id})
- ✅ User can toggle task completion status (PATCH /api/tasks/{id}/complete)
- ✅ User can delete task (DELETE /api/tasks/{id}, 204 response)
- ✅ User can filter tasks by completion status (query param ?filter=completed)
- ✅ User isolation enforced for all operations (403 for other user's tasks)

### Frontend Tasks (User Story 2)

- [ ] T047 [US2] Update frontend/lib/api.ts with updateTask(id, data), toggleComplete(id), deleteTask(id), listTasks(filter) methods per contracts/tasks-api.md
- [ ] T048 [US2] Create frontend/components/task/TaskItem.tsx Client Component: display task with title (strikethrough if completed), description, timestamps, checkbox for completion toggle, Edit button, Delete button
- [ ] T049 [US2] Implement TaskItem checkbox onClick: call API toggleComplete(task.id), optimistically update UI (no page refresh), show success toast
- [ ] T050 [US2] Implement TaskItem Edit button: show Modal with TaskForm pre-filled with current values, submit calls API updateTask(), updates list immediately
- [ ] T051 [US2] Implement TaskItem Delete button: show confirmation dialog "Delete task? This cannot be undone", on confirm call API deleteTask(), remove from list immediately
- [ ] T052 [US2] Create frontend/components/task/TaskFilters.tsx Client Component: buttons/tabs for "All", "Pending", "Completed", onClick updates URL query param and filters task list

**Completion Criteria (Frontend)**:
- ✅ User can mark task complete via checkbox (visual change: strikethrough, color)
- ✅ Statistics update automatically when task toggled (e.g., "3 of 5 completed (60%)")
- ✅ User can edit task via Edit button (modal opens, submit updates task)
- ✅ User can delete task via Delete button (confirmation dialog, then remove from list)
- ✅ User can filter tasks by status (All/Pending/Completed filters work)

**US2 Acceptance Test**:
1. Login as user with 3 tasks (2 pending, 1 completed)
2. View dashboard → all 3 tasks displayed sorted by newest first
3. Click checkbox on pending task → task shows as completed, statistics update
4. Click Edit on task → change description → submit → task updates immediately
5. Click Delete on completed task → confirm → task removed from list
6. Click "Completed" filter → only 2 completed tasks shown

---

## Phase 7: User Story 3 - Multi-Device Access and Responsive Experience (P3) (6 tasks)

**Goal**: Implement responsive layouts for mobile/tablet/desktop with touch-friendly UI and adaptive navigation

**Why P3**: Enhances UX for cross-device access, not critical for initial launch but important for modern web app

**Independent Test**: Access application from different device types/screen sizes and verify layout adapts correctly

**Prerequisites**: Phases 4-6 complete (US1, US2, US4 implemented)

### Tasks

- [ ] T053 [P] [US3] Create frontend/components/ui/Button.tsx reusable component with Tailwind: base styles + responsive touch targets (h-11 on mobile <640px, h-10 on desktop) per research.md Finding #6
- [ ] T054 [P] [US3] Create frontend/components/ui/Input.tsx reusable form input component with Tailwind: full width on mobile, max-width on desktop, proper focus states, WCAG AA color contrast
- [ ] T055 [US3] Update frontend/app/dashboard/page.tsx with responsive layout: single column on mobile (<640px), centered with max-width 1200px on desktop (>1024px), comfortable spacing
- [ ] T056 [US3] Update frontend/components/task/TaskList.tsx with responsive grid: single column mobile, optional 2-column tablet, single centered column desktop
- [ ] T057 [US3] Add mobile navigation: create hamburger menu component for <640px, full navigation bar for >=1024px, smooth transitions
- [ ] T058 [US3] Test responsive breakpoints: verify layout adapts correctly at 640px (sm), 768px (md), 1024px (lg) Tailwind breakpoints, ensure all touch targets >=44px on mobile

**Completion Criteria**:
- ✅ Mobile (<640px): Single column layout, touch-friendly buttons (≥44px), hamburger menu
- ✅ Tablet (640px-1024px): Optimized spacing, larger touch targets, adapted navigation
- ✅ Desktop (>1024px): Centered max-width 1200px, comfortable spacing, full navigation, hover states
- ✅ Resize responsiveness: Layout adapts smoothly through breakpoints without page refresh
- ✅ Accessibility: WCAG 2.1 AA color contrast, keyboard navigation works

**US3 Acceptance Test**:
1. Access /dashboard on mobile phone (<640px) → single column, touch-friendly buttons
2. Access /dashboard on tablet (768px) → optimized spacing, adapted navigation
3. Access /dashboard on desktop (>1024px) → centered layout, full nav, hover states
4. Resize browser from wide to narrow → layout adapts through breakpoints smoothly

---

## Phase 8: Polish & Cross-Cutting Concerns (5 tasks)

**Goal**: Add loading states, error handling, empty states, success notifications, and production optimizations

**Prerequisites**: Phases 4-7 complete (all user stories implemented)

### Tasks

- [ ] T059 [P] Create frontend/components/ui/Toast.tsx notification component: success/error variants, auto-dismiss after 3 seconds, accessible with ARIA labels
- [ ] T060 [P] Create frontend/components/ui/Modal.tsx dialog component: backdrop, close button, focus trap, ESC key to close, accessible with ARIA
- [ ] T061 Update all frontend API calls with loading states: show spinner during fetch, disable buttons to prevent double-submit, handle network errors with user-friendly messages
- [ ] T062 Add global error boundary in frontend/app/layout.tsx: catch runtime errors, display "Something went wrong" page with refresh button, log errors to console for debugging
- [ ] T063 Configure frontend/next.config.js for production: enable strict mode, configure image optimization, set environment variables, verify build succeeds with `npm run build`

**Completion Criteria**:
- ✅ Loading indicators shown during async operations (API calls, data fetching)
- ✅ Success toasts appear after task created/updated/deleted
- ✅ Error messages display when operations fail (network errors, validation errors)
- ✅ Empty states shown when appropriate (no tasks, loading, error states)
- ✅ Global error boundary catches and displays runtime errors
- ✅ Production build succeeds without errors

---

## Deployment Tasks (Optional - not included in main count)

**Note**: Deployment is optional for development phase. Complete when ready for production.

### Frontend Deployment (Vercel)

- [ ] D001 Push code to GitHub repository
- [ ] D002 Connect GitHub repo to Vercel, set Root Directory to "frontend/", configure Next.js preset
- [ ] D003 Configure Vercel environment variables: NEXT_PUBLIC_API_URL (backend URL), BETTER_AUTH_SECRET
- [ ] D004 Deploy to Vercel, verify build succeeds, test production URL

### Backend Deployment (Railway)

- [ ] D005 Create Railway project, connect GitHub repo, set Root Directory to "backend/"
- [ ] D006 Configure Railway environment variables: DATABASE_URL (Neon connection string), BETTER_AUTH_SECRET, FRONTEND_URL (Vercel URL), PORT=8000
- [ ] D007 Deploy backend, verify uvicorn starts, test /health endpoint
- [ ] D008 Update Vercel NEXT_PUBLIC_API_URL to Railway production URL, redeploy frontend

---

## Dependency Graph

**User Story Completion Order**:

```
Phase 1 (Setup) → Phase 2 (Database/Backend Foundation) → Phase 3 (Auth/Middleware)
    ↓
Phase 4 (US1 - P1 MVP) ← REQUIRED FOR ALL OTHER STORIES
    ↓
    ├→ Phase 5 (US4 - P2 Session Management)
    ├→ Phase 6 (US2 - P2 Task Management)  ← Can be parallel with US4
    ↓
Phase 7 (US3 - P3 Responsive UX) ← Requires US1, US2, US4 for complete testing
    ↓
Phase 8 (Polish) ← Final phase after all user stories
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4 (US1) → Phase 6 (US2) → Phase 8
**Estimated Timeline**: 10-15 days with sequential execution, 7-10 days with parallel execution

---

## Parallel Execution Examples

### Setup Phase (Phase 1)
- T002 (Frontend init) + T003 (Backend init) + T005 (Gitignore) can run simultaneously

### Backend Foundation (Phase 2)
- T009-T014 (all model/schema creation) can run in parallel after T008 (database setup)

### User Story 1 Implementation (Phase 4)
- T030 (TypeScript types) + T023-T024 (Backend auth routes) can run in parallel
- T031 (API client) requires T030 complete
- T032-T036 (Frontend components) can run in parallel after T031 complete

### User Story 2 Implementation (Phase 6)
- T043-T045 (Backend CRUD endpoints) can run in parallel
- T047-T052 (Frontend components) can run in parallel after T047 (API client update)

### Polish Phase (Phase 8)
- T059 (Toast) + T060 (Modal) + T062 (Error boundary) can run in parallel

---

## MVP Scope Recommendation

**Minimum Viable Product**: Complete through **Phase 4 (User Story 1 only)**

This delivers:
- ✅ User registration and authentication
- ✅ Task creation and viewing
- ✅ Database persistence
- ✅ Basic security (JWT tokens, user isolation)

**Demo-able**: User can sign up, create account, add first task, logout, login again, and see task persisted.

**Next Increment**: Add Phase 5 (US4 - Session Management) for complete authentication security
**Full Feature Set**: Complete all phases through Phase 7 for production-ready application

---

## Task Validation Checklist

All tasks follow required format:
- ✅ Checkbox format: `- [ ]`
- ✅ Task ID: T001-T063 sequential
- ✅ [P] marker: Added to parallelizable tasks (20 total)
- ✅ [Story] label: Added to user story phases (US1, US2, US3, US4)
- ✅ File paths: Included in every task description
- ✅ Acceptance criteria: Defined for each phase

**Total Tasks**: 63 implementation tasks + 8 deployment tasks (optional)
**Parallelizable Tasks**: 20 tasks (32% of implementation tasks)
**User Story Distribution**:
- US1 (P1 MVP): 14 tasks
- US2 (P2 Task CRUD): 10 tasks
- US3 (P3 Responsive): 6 tasks
- US4 (P2 Security): 6 tasks
- Setup/Foundation: 22 tasks
- Polish: 5 tasks

---

**Tasks Status**: ✅ READY FOR IMPLEMENTATION
**Last Updated**: 2025-12-30
**Version**: 1.0.0
