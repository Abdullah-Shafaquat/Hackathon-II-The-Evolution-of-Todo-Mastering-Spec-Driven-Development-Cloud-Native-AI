<!--
Sync Impact Report - Constitution Version Update
================================================
Version Change: 1.0.0 → 2.0.0

Modified Principles:
- NEW: Spec-Driven Development (replaces generic development methodology)
- NEW: Mandatory Technology Stack (Phase II specific constraints)
- NEW: Multi-User Architecture (authentication and data isolation)
- NEW: Database-First Persistence (replaces in-memory storage)
- NEW: Security-First Design (JWT, CORS, input validation)
- NEW: Responsive Web Design (mobile-first approach)
- NEW: RESTful API Design (standardized endpoints)

Added Sections:
- Phase II Technical Constraints (comprehensive tech stack requirements)
- Architectural Principles (monorepo, authentication flow, JWT)
- Core Features (mandatory Phase II capabilities)
- Database Schema Requirements (Neon PostgreSQL design)
- Security Requirements (authentication, API, data security)
- Code Quality Standards (frontend, backend, database)
- Development Workflow Constraints (spec-driven rules)
- Deployment Requirements (Vercel, backend, Neon)
- Performance Requirements (frontend, backend, database)
- User Experience Requirements (auth flow, task UI, responsive, a11y)
- Error Handling Standards (frontend, backend, security)
- Integration Requirements (Better Auth, Neon, Vercel)
- Success Criteria (functional, technical, quality)
- Phase Transition Requirements (Phase I→II, II→III prep)

Removed Sections:
- Generic library-first principles (not applicable to web app)
- CLI interface requirements (replaced with web UI)

Templates Requiring Updates:
✅ plan-template.md - Updated to reference Phase II technology stack
✅ spec-template.md - Updated to include authentication and multi-user scenarios
✅ tasks-template.md - Updated to include security and deployment tasks

Follow-up TODOs:
- RATIFICATION_DATE needs to be set (marking as 2025-12-30 for Phase II start)
- Create frontend-specific CLAUDE.md with Next.js 16+ guidelines
- Create backend-specific CLAUDE.md with FastAPI guidelines
- Setup Neon database branching strategy documentation

Bump Rationale:
MAJOR version bump (1.0.0 → 2.0.0) - Backward incompatible changes representing
transformation from Phase I (console app, in-memory) to Phase II (web app, database,
authentication). Complete redefinition of project architecture and requirements.
-->

# Todo Web Application - Phase II Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All development MUST follow the spec-driven methodology:

- **Write specifications first** - before any code is generated
- **Generate code with Claude Code** - no manual coding allowed
- **Iterate on specifications** - not on code directly
- **Task references** - all code must reference task IDs from tasks.md
- **Acceptance criteria** - every feature must meet defined criteria in spec.md

**Rationale**: Ensures predictable, traceable development aligned with hackathon constraints
and enables proper version control of requirements before implementation.

### II. Mandatory Technology Stack (NON-NEGOTIABLE)

The following technology choices are fixed and MUST NOT be changed:

- **Frontend**: Next.js 16+ with App Router, TypeScript, and Tailwind CSS
- **Backend**: Python FastAPI with SQLModel for ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Architecture**: Monorepo structure (frontend + backend in same repository)
- **Deployment**: Frontend on Vercel, Backend publicly accessible via URL

**Rationale**: These are hackathon requirements that ensure compatibility with evaluation
criteria and demonstrate modern full-stack development capabilities.

### III. Multi-User Architecture (NON-NEGOTIABLE)

All features MUST support multiple independent users:

- **User Isolation**: Each user sees only their own data
- **JWT Authentication**: All API requests must include valid JWT tokens
- **Backend Verification**: FastAPI middleware verifies JWT on every protected endpoint
- **Database Filtering**: All queries filter by authenticated user_id
- **No Shared State**: No in-memory storage shared across users

**Rationale**: Core Phase II requirement transforming single-user console app into
multi-tenant web application with proper security boundaries.

### IV. Database-First Persistence (NON-NEGOTIABLE)

All data MUST persist in Neon PostgreSQL database:

- **No In-Memory Storage**: All task data stored in database tables
- **Session Persistence**: Tasks survive application restarts
- **Schema Migrations**: Use SQLModel for schema management
- **Connection Pooling**: Proper database connection lifecycle management
- **Transaction Safety**: Use transactions for multi-operation consistency

**Rationale**: Enables multi-user support and data durability required for production
web applications.

### V. Security-First Design

Security MUST be integrated at every layer:

- **JWT Secret Management**: Environment variables for sensitive credentials
- **Password Hashing**: Better Auth handles secure password storage
- **HTTPS Only**: All production API calls over HTTPS
- **CORS Configuration**: Whitelist only frontend domain
- **Input Validation**: Validate all user inputs with Pydantic models
- **SQL Injection Prevention**: Use SQLModel parameterized queries only
- **Rate Limiting**: Basic rate limiting on API endpoints
- **Error Message Safety**: Never expose sensitive information in error responses

**Rationale**: Prevents common vulnerabilities (OWASP Top 10) and ensures user data
protection in production environment.

### VI. Responsive Web Design

UI MUST work across all device sizes:

- **Mobile-First**: Start with mobile layout, enhance for larger screens
- **Tailwind Breakpoints**: Use Tailwind's responsive utilities consistently
- **Touch-Friendly**: Buttons and interactive elements sized for touch
- **Accessibility**: WCAG 2.1 AA compliance with semantic HTML and ARIA labels
- **Keyboard Navigation**: All functionality accessible via keyboard

**Rationale**: Modern web applications must serve diverse devices and users with
varying abilities.

### VII. RESTful API Design

Backend API MUST follow REST principles:

- **Standard HTTP Methods**: GET (read), POST (create), PUT/PATCH (update), DELETE
- **Resource-Based URLs**: `/api/tasks`, `/api/tasks/{id}`
- **HTTP Status Codes**: 200 (success), 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error)
- **JSON Request/Response**: Consistent JSON format with Pydantic validation
- **OpenAPI Documentation**: Auto-generated API docs via FastAPI

**Rationale**: Standard API design enables predictable integration and future extensibility
(e.g., Phase III AI agent integration).

### VIII. Test-Driven Development (OPTIONAL)

Testing is encouraged but not mandatory for Phase II:

- **Frontend Tests**: React Testing Library for component tests
- **Backend Tests**: Pytest for API endpoint tests
- **Integration Tests**: Full authentication flow tests
- **E2E Tests**: Critical user journey validation

**Rationale**: While testing improves code quality, time constraints in hackathon environment
make comprehensive test coverage optional rather than mandatory.

## Phase II Technical Constraints

### Mandatory Technology Stack (Cannot Change)

**Frontend**:
- Next.js 16+ with App Router (NOT Pages Router)
- TypeScript with strict type checking
- Tailwind CSS for styling
- Better Auth client for authentication
- React Server Components by default

**Backend**:
- Python 3.11+ with FastAPI
- SQLModel for database ORM
- Pydantic models for validation
- JWT verification middleware
- CORS middleware for frontend domain

**Database**:
- Neon Serverless PostgreSQL
- Connection pooling
- Schema migrations via SQLModel
- Indexed queries for performance

**Deployment**:
- Frontend: Vercel with automatic deployments
- Backend: Publicly accessible URL with health endpoint
- Database: Neon free tier with automatic backups

### Phase-Specific Requirements

- **Multi-User Support**: Each user must see only their own tasks
- **Database Persistence**: Tasks must persist across sessions
- **RESTful API**: Clean, documented API endpoints
- **Authentication**: Secure signup/login with JWT tokens
- **Responsive Design**: Mobile and desktop friendly UI
- **Error Handling**: User-friendly error messages throughout

### Prohibited in Phase II

- ❌ No console-only interface (must be web-based)
- ❌ No in-memory storage (must use database)
- ❌ No single-user assumption (must support multiple users)
- ❌ No manual authentication (must use Better Auth)
- ❌ No Pages Router (must use Next.js App Router)
- ❌ No untyped code (TypeScript strict mode required)

## Architectural Principles

### Monorepo Structure

```
Phase-II/
├── .specify/                    # Spec-Kit configuration
│   ├── memory/
│   │   └── constitution.md     # This file
│   ├── templates/              # Spec, plan, task templates
│   └── scripts/                # Automation scripts
├── specs/                       # Feature specifications
│   └── [feature-name]/
│       ├── spec.md             # Requirements
│       ├── plan.md             # Architecture
│       └── tasks.md            # Implementation tasks
├── frontend/                    # Next.js 16+ application
│   ├── app/                    # App Router pages
│   │   ├── (auth)/            # Auth routes
│   │   ├── dashboard/         # Main app
│   │   └── api/               # API routes (if needed)
│   ├── components/             # React components
│   │   ├── ui/                # Reusable UI components
│   │   └── task/              # Task-specific components
│   ├── lib/                    # Utilities and API client
│   │   ├── api.ts             # API client with auth
│   │   └── auth.ts            # Better Auth configuration
│   └── CLAUDE.md              # Frontend-specific guidelines
├── backend/                     # FastAPI application
│   ├── main.py                 # FastAPI app entry
│   ├── models.py               # SQLModel database models
│   ├── schemas.py              # Pydantic request/response models
│   ├── routes/                 # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   └── tasks.py           # Task CRUD endpoints
│   ├── middleware/             # Middleware components
│   │   └── auth.py            # JWT verification
│   ├── database.py             # Database connection
│   └── CLAUDE.md              # Backend-specific guidelines
├── history/                     # Development history
│   ├── prompts/                # Prompt History Records
│   └── adr/                    # Architecture Decision Records
├── docker-compose.yml          # Local development environment
├── .env.example                # Environment variable template
├── CLAUDE.md                   # Root-level guidelines
└── README.md                   # Project documentation
```

### Authentication Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Next.js    │────▶│  Better Auth│────▶│  FastAPI    │────▶│  Neon DB    │
│  Frontend   │     │  (JWT)      │     │  Backend    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                    │                    │
      └──Bearer Token────▶└────Verify Token───▶└──User Filtering──▶
```

**JWT Flow**:
1. Frontend: Better Auth handles signup/login, issues JWT token
2. Frontend: Attaches JWT to all API requests in Authorization header
3. Backend: FastAPI middleware verifies JWT signature and extracts user_id
4. Backend: All database queries filter by authenticated user_id
5. Response: JSON data returned only for authenticated user's resources

### RESTful API Endpoints

**Required Endpoints**:
```
POST   /api/auth/signup         - User registration
POST   /api/auth/login          - User login
POST   /api/auth/logout         - User logout
GET    /api/tasks               - List all tasks for authenticated user
POST   /api/tasks               - Create new task
GET    /api/tasks/{id}          - Get specific task
PUT    /api/tasks/{id}          - Update task
DELETE /api/tasks/{id}          - Delete task
PATCH  /api/tasks/{id}/complete - Toggle task completion status
GET    /health                  - Health check endpoint
```

## Core Features (MANDATORY FOR PHASE II)

### 1. Authentication System

**User Registration**:
- Email/password signup form with validation
- Password strength requirements
- Email uniqueness validation
- Better Auth integration for secure storage

**User Login**:
- Email/password login form
- Session management with JWT tokens
- "Remember me" functionality
- Automatic token refresh

**JWT Integration**:
- Token issuance on successful login
- Token verification on protected routes
- Token storage in secure httpOnly cookies
- Token expiration and refresh handling

**Protected Routes**:
- Frontend route guards for authenticated pages
- Backend middleware for API endpoints
- Redirect to login on unauthorized access

### 2. Task Management (All Basic Features - Web Version)

- ✅ **Add Task** - Web form with title and description, validation for required fields
- ✅ **View Tasks** - Responsive task list with filtering (all/completed/active)
- ✅ **Update Task** - Inline edit or modal dialog for task details
- ✅ **Delete Task** - Confirmation dialog before deletion
- ✅ **Mark Complete** - Toggle completion status with visual feedback

### 3. User Interface Requirements

**Responsive Design**:
- Mobile: Single column layout, touch-friendly buttons (≥44px tap targets)
- Tablet: Optimized layout with more screen space
- Desktop: Multi-column or centered single column with max-width
- Breakpoints: Tailwind's sm/md/lg/xl utilities

**Modern UI**:
- Clean, professional appearance with consistent spacing
- Loading states with spinners or skeleton screens
- Success/error toast notifications
- Empty states with helpful messages

**Accessibility**:
- Semantic HTML5 elements (header, nav, main, article)
- ARIA labels for interactive elements
- Keyboard navigation support (Tab, Enter, Escape)
- Color contrast WCAG 2.1 AA compliance
- Focus management for modals and forms

## Database Schema Requirements

### Tables Structure

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id TEXT PRIMARY KEY,              -- Better Auth user ID (UUID)
    email TEXT UNIQUE NOT NULL,       -- User email for login
    name TEXT,                        -- Optional display name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,                              -- Auto-increment task ID
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,                        -- Task title (required)
    description TEXT,                                   -- Optional task description
    completed BOOLEAN DEFAULT FALSE,                    -- Completion status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Creation timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP      -- Last update timestamp
);
```

### Index Requirements

```sql
-- Index for user-based queries (critical for performance)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for filtering by completion status
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Index for sorting by creation date
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Composite index for user + completion filtering
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

## Security Requirements

### Authentication Security

- **JWT Secret**: Environment variable `BETTER_AUTH_SECRET` (≥32 characters, same for frontend/backend)
- **Token Expiry**: 7 days for access tokens, 30 days for refresh tokens
- **Password Hashing**: Better Auth uses bcrypt (handled automatically)
- **HTTPS**: All API calls over HTTPS in production (enforced by Vercel)
- **Secure Cookies**: httpOnly, secure, sameSite flags for cookie storage

### API Security

- **CORS**: Configured to allow only frontend domain (`FRONTEND_URL` environment variable)
- **Rate Limiting**: 100 requests per minute per IP for authentication endpoints
- **Input Validation**: All API inputs validated with Pydantic models
- **SQL Injection Prevention**: SQLModel parameterized queries (never string concatenation)
- **XSS Prevention**: React auto-escapes output, CSP headers configured

### Data Security

- **User Isolation**: Database queries MUST filter by user_id from JWT
- **Data Validation**: Validate all user inputs (length, format, type)
- **Error Messages**: Generic errors to users, detailed logs to server
- **Authorization**: Verify user owns resource before allowing access/modification

## Code Quality Standards

### Frontend (Next.js 16+)

**TypeScript**:
- Strict type checking enabled in tsconfig.json
- No `any` types (use `unknown` with type guards)
- Explicit return types for all functions
- Interface definitions for all component props

**App Router**:
- Use Next.js App Router (NOT Pages Router)
- Server Components by default for static content
- Client Components ('use client') only for interactivity
- Route groups for organization (e.g., `(auth)`, `(dashboard)`)

**Component Organization**:
- Functional components with TypeScript
- Single Responsibility Principle (one component, one job)
- Props destructuring with TypeScript interfaces
- Consistent file naming (PascalCase for components)

**Tailwind CSS**:
- Utility-first styling (no custom CSS files)
- Responsive utilities (sm:, md:, lg:, xl:)
- Design system consistency (colors, spacing, typography)
- Dark mode support via Tailwind's dark: prefix (optional)

**API Client**:
- Centralized API client in `lib/api.ts`
- Automatic JWT token attachment
- Consistent error handling with try-catch
- Type-safe request/response with TypeScript interfaces

### Backend (FastAPI)

**Type Hints**:
- All functions MUST have type hints for parameters and return values
- Use `typing` module for complex types (List, Dict, Optional, Union)
- Pydantic models for request/response validation
- SQLModel for database model type safety

**Pydantic Models**:
- Request validation models (e.g., `TaskCreate`, `TaskUpdate`)
- Response models (e.g., `TaskResponse`, `UserResponse`)
- Field validation with constraints (min/max length, regex patterns)
- Automatic JSON schema generation for API docs

**Error Handling**:
- HTTPException with appropriate status codes
- Consistent error response format: `{"detail": "error message"}`
- Never expose stack traces or database errors to clients
- Log detailed errors server-side for debugging

**Middleware**:
- JWT verification middleware for protected routes
- CORS middleware with allowed origins
- Request logging middleware (optional)
- Error handling middleware for global exception catching

**Documentation**:
- Auto-generated OpenAPI docs at `/docs`
- Docstrings for all public functions
- API endpoint descriptions and examples

### Database (SQLModel + Neon)

**Migrations**:
- SQLModel for schema definition and creation
- Version-controlled migration scripts (optional for Phase II)
- Test migrations on development branch first

**Connection Pooling**:
- Configure connection pool size based on expected load
- Handle connection timeouts gracefully
- Close connections properly in finally blocks

**Query Optimization**:
- Use indexes for frequently queried fields
- Avoid N+1 queries (use eager loading with joins)
- Limit query results with pagination
- Profile slow queries and optimize

## Development Workflow Constraints

### Spec-Driven Development Rules

1. **NO MANUAL CODING**: All code must be generated by Claude Code based on specifications
2. **SPECIFICATION FIRST**: Update spec.md before requesting code changes
3. **TASK REFERENCES**: All code must reference task IDs from tasks.md
4. **ACCEPTANCE CRITERIA**: Every feature must meet criteria defined in spec.md

### File Organization Rules

1. **Monorepo Structure**: Frontend and backend in same repository
2. **Specification Files**: All specs in `/specs/` organized by feature name
3. **CLAUDE.md Files**: Root, frontend, and backend specific instructions
4. **Environment Variables**: `.env.example` for template, `.env` for secrets (gitignored)

### Testing Requirements (Optional)

- **Frontend Tests**: Component tests with React Testing Library and Jest
- **Backend Tests**: API endpoint tests with pytest and pytest-asyncio
- **Integration Tests**: Full authentication flow with real database
- **Database Tests**: CRUD operation tests with test database
- **E2E Tests**: Playwright for critical user journeys

## Deployment Requirements

### Frontend Deployment (Vercel)

- **Automatic Deployments**: Connect GitHub repository to Vercel project
- **Environment Variables**: Configure in Vercel dashboard
  - `NEXT_PUBLIC_API_URL`: Backend API URL
  - `BETTER_AUTH_SECRET`: JWT secret (same as backend)
  - `DATABASE_URL`: Neon connection string (if using server actions)
- **Domain**: Custom domain or Vercel subdomain (`.vercel.app`)
- **HTTPS**: Automatic SSL certificate via Let's Encrypt

### Backend Deployment

- **Accessible URL**: Backend must be publicly accessible (e.g., Railway, Render, Fly.io)
- **CORS Configuration**: Allow only frontend domain in production
- **Environment Variables**:
  - `DATABASE_URL`: Neon PostgreSQL connection string
  - `BETTER_AUTH_SECRET`: JWT secret (same as frontend)
  - `FRONTEND_URL`: Frontend domain for CORS
- **Health Check**: `/health` endpoint returns 200 OK for monitoring

### Database (Neon)

- **Free Tier**: Use Neon's free tier (sufficient for hackathon)
- **Connection String**: Copy from Neon dashboard to `DATABASE_URL`
- **Branching**: Use Neon branches for development/production isolation
- **Backups**: Automatic backups enabled (Neon feature)

## Performance Requirements

### Frontend Performance

- **First Load**: < 3 seconds on average 4G connection
- **Time to Interactive**: < 5 seconds
- **Bundle Size**: Optimize JavaScript bundles (code splitting, tree shaking)
- **Image Optimization**: Use Next.js Image component with automatic WebP

### Backend Performance

- **API Response Time**: < 200ms for typical CRUD operations
- **Database Queries**: < 100ms for simple queries (use indexes)
- **Concurrent Users**: Support at least 10 concurrent users without degradation
- **Memory Usage**: Efficient resource utilization (monitor with logs)

### Database Performance

- **Connection Pool**: Configure pool size (default 10-20 connections)
- **Query Optimization**: Use EXPLAIN to analyze slow queries
- **Read/Write Balance**: Optimize for read-heavy workload (task viewing)

## User Experience Requirements

### Authentication Flow

1. **Registration**: Simple form (email, password, optional name), clear validation errors
2. **Login**: Email/password form with "Remember me" checkbox
3. **Session Management**: Automatic token refresh before expiration
4. **Logout**: Clear logout button, clears session and redirects to login

### Task Management Interface

1. **Task List**: Clean, scannable list with completion checkboxes
2. **Task Actions**: Edit (pencil icon), Delete (trash icon), Complete (checkbox)
3. **Empty States**: "No tasks yet. Create your first task!" with call-to-action
4. **Loading States**: Spinners during API calls, optimistic UI updates

### Responsive Design

- **Mobile**: Single column, full-width components, 16px minimum font size
- **Tablet**: Optimized spacing, 2-column layout for task list (optional)
- **Desktop**: Centered layout with max-width (1200px), comfortable spacing
- **Breakpoints**: Tailwind utilities (sm:640px, md:768px, lg:1024px, xl:1280px)

### Accessibility

- **Keyboard Navigation**: Tab through all interactive elements, Enter to submit forms
- **Screen Readers**: ARIA labels for icons, semantic HTML for structure
- **Color Contrast**: 4.5:1 for normal text, 3:1 for large text (WCAG AA)
- **Focus Management**: Visible focus indicators, focus trap in modals

## Error Handling Standards

### Frontend Errors

- **Network Errors**: "Unable to connect. Please check your internet connection."
- **Validation Errors**: Inline errors below form fields (e.g., "Email is required")
- **Authentication Errors**: Redirect to login with "Session expired. Please log in again."
- **Runtime Errors**: Error boundaries catch crashes, show "Something went wrong" page

### Backend Errors

- **HTTP Status Codes**: 200 (success), 400 (validation), 401 (unauthorized), 404 (not found), 500 (server error)
- **Error Responses**: `{"detail": "User-friendly message"}` JSON format
- **Validation Errors**: `{"detail": [{"field": "email", "message": "Invalid email format"}]}`
- **Database Errors**: Logged server-side, return generic 500 to client

### Security Error Handling

- **Invalid Tokens**: 401 Unauthorized with `{"detail": "Invalid or expired token"}`
- **Permission Errors**: 403 Forbidden with `{"detail": "Access denied"}`
- **Rate Limiting**: 429 Too Many Requests with `{"detail": "Too many requests. Try again later."}`
- **Input Validation**: 400 Bad Request with field-specific errors

## Integration Requirements

### Better Auth Integration

- **Frontend Setup**: Install `better-auth` client, configure in `lib/auth.ts`
- **Backend Integration**: JWT verification middleware in `middleware/auth.py`
- **User Sync**: Create user in database on first successful login
- **Session Management**: Token refresh logic, handle expiration gracefully

### Neon Database Integration

- **Connection Setup**: SQLModel with Neon connection string from environment
- **Migrations**: Create tables on first run, alter schema as needed
- **Connection Pooling**: Configure pool size and timeout settings
- **Error Recovery**: Retry logic for transient connection failures

### Vercel Deployment Integration

- **Frontend Build**: Next.js build optimization, static generation where possible
- **Environment Variables**: Properly configure in Vercel project settings
- **API Proxy**: Optional - use Next.js API routes to proxy backend if needed
- **Domain Configuration**: Custom domain setup with DNS records

## Success Criteria for Phase II

### Functional Success Criteria

- [ ] User can register with email/password successfully
- [ ] User can login and receive valid JWT token
- [ ] User can create new tasks via web form
- [ ] User can view list of their own tasks (no other users' tasks)
- [ ] User can update task title/description
- [ ] User can delete tasks with confirmation
- [ ] User can toggle task completion status
- [ ] Tasks persist across browser sessions (database storage)
- [ ] All 5 basic features work in web interface

### Technical Success Criteria

- [ ] Monorepo structure properly implemented (frontend + backend folders)
- [ ] JWT authentication working end-to-end (signup → login → API calls)
- [ ] Database schema properly designed and implemented in Neon
- [ ] All RESTful API endpoints functional and documented
- [ ] Frontend deployed on Vercel with public URL
- [ ] Backend accessible via public URL with health endpoint
- [ ] Environment variables properly configured for all services

### Quality Success Criteria

- [ ] Code follows all quality standards (TypeScript strict, FastAPI type hints)
- [ ] Responsive design works on mobile, tablet, and desktop
- [ ] Comprehensive error handling implemented (user-friendly messages)
- [ ] Adequate test coverage achieved (optional but recommended)
- [ ] Documentation complete and clear (README, API docs)

## Phase Transition Requirements

### From Phase I to Phase II

- **Console to Web**: Transform command-line interface to web browser interface
- **Memory to Database**: Replace Python dictionaries with PostgreSQL tables
- **Single to Multi-User**: Add authentication system and user isolation
- **Local to Deployed**: Deploy frontend to Vercel, backend to public URL

### For Phase III Preparation

- **API Foundation**: Ensure clean, documented API for AI agent integration
- **Database Structure**: Prepare schema for conversation storage (future)
- **Authentication**: JWT system ready for AI agent authentication
- **Error Handling**: Robust enough for AI interactions with clear error messages

## Constitution Hierarchy

This constitution is the highest authority for Phase II development. In case of conflict:

1. **This Constitution** (`.specify/memory/constitution.md`)
2. **Phase Specifications** (`specs/phases/phase2.md` if exists)
3. **Feature Specifications** (`specs/[feature-name]/spec.md`)
4. **Technical Plan** (`specs/[feature-name]/plan.md`)
5. **Task List** (`specs/[feature-name]/tasks.md`)
6. **Generated Code** (frontend/, backend/)

**Amendment Process**:
- Constitution changes require explicit user approval
- Update version number according to semantic versioning
- Document changes in Sync Impact Report
- Update dependent templates (spec, plan, tasks) for consistency

**Compliance Review**:
- All pull requests must verify compliance with constitution
- Complexity that violates principles must be justified in plan.md
- Use CLAUDE.md files for runtime development guidance specific to frontend/backend

## Governance

**Constitutional Authority**: This constitution supersedes all other practices and documentation.
Any code, specification, or decision that conflicts with this constitution is invalid and must
be corrected.

**Amendment Procedure**:
1. Identify constitutional principle that needs change
2. Document rationale and impact analysis
3. Obtain user approval for amendment
4. Update constitution with new version number
5. Propagate changes to dependent templates
6. Create Architecture Decision Record if architecturally significant

**Versioning Policy**:
- **MAJOR**: Backward incompatible changes (e.g., Phase I → Phase II transformation)
- **MINOR**: New principles or sections added without breaking existing ones
- **PATCH**: Clarifications, wording improvements, typo fixes

**Compliance Validation**:
- All specifications (spec.md) must align with constitutional requirements
- All plans (plan.md) must verify constitutional compliance in "Constitution Check" section
- All tasks (tasks.md) must reference constitutional principles they implement
- All code generation must adhere to code quality standards defined herein

**Deferred Decisions**: If any requirements are unclear or need user input, mark as
`NEEDS CLARIFICATION` in specifications and use the AskUserQuestion tool before proceeding.

---

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30

**Revision History**:
- **Version 2.0.0** (2025-12-30): Phase II Constitution for Full-Stack Web Application
  - Complete rewrite for web app with authentication and database
  - Supersedes Phase I Constitution where applicable
  - Based on: Hackathon II Phase II requirements
  - Effective: For Phase II development only
