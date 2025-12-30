---
id: 002
title: Phase II Implementation Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: todo-web-app-phase-ii
branch: 001-todo-web-app-phase-ii
user: Dell
command: /sp.plan
labels: ["plan", "phase-ii", "full-stack", "architecture", "design"]
links:
  spec: specs/001-todo-web-app-phase-ii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-web-app-phase-ii/plan.md
  - specs/001-todo-web-app-phase-ii/research.md
  - specs/001-todo-web-app-phase-ii/data-model.md
  - specs/001-todo-web-app-phase-ii/contracts/auth-api.md
  - specs/001-todo-web-app-phase-ii/contracts/task-api.md
  - specs/001-todo-web-app-phase-ii/quickstart.md
  - CLAUDE.md
tests:
  - N/A (planning phase)
---

## Prompt

User executed `/sp.plan` command to generate the implementation plan for Phase II of the Todo Web App.

**Context from previous session**:
- Phase I specification created (specs/001-todo-web-app-phase-ii/spec.md) with 10 prioritized user stories, 52 functional requirements, 30 success criteria
- Constitution updated to v2.0.0 for Phase II (full-stack web application)
- Feature branch created: 001-todo-web-app-phase-ii

**System encountered issue**: PowerShell script `.specify/scripts/powershell/setup-plan.ps1` failed with "pwsh: No such file or directory"

**Approach**: Manually executed plan generation workflow following the sp.plan skill guidelines:
1. Read plan template to understand structure
2. Create comprehensive plan.md based on spec.md and constitution requirements
3. Generate Phase 0 research.md (technical decisions for Better Auth, Neon PostgreSQL, Next.js App Router, CORS/deployment, security)
4. Generate Phase 1 design artifacts:
   - data-model.md (User, Task, JWT Token entities with validation rules)
   - contracts/auth-api.md (5 authentication endpoints)
   - contracts/task-api.md (6 task management endpoints)
   - quickstart.md (developer onboarding guide)
5. Update agent context (CLAUDE.md) with Phase II technology stack

## Response snapshot

Successfully generated comprehensive implementation plan and all Phase 1 design artifacts:

**1. Implementation Plan (plan.md)**:
- Technical Context: Next.js 16+, FastAPI, Neon PostgreSQL, Better Auth, TypeScript, Python 3.13+
- Constitution Check: All mandatory requirements validated (✅ PASS)
- Project Structure: Monorepo (frontend/, backend/, .specify/, specs/)
- Phase 0: 5 research areas documented
- Phase 1: 4 design artifacts generated
- Implementation Strategy: 6-phase incremental delivery (2A-2F)
- Testing Strategy: Unit (80% coverage), integration (all API contracts), E2E (10 user stories)
- Risk Mitigation: 5 identified risks with mitigations
- Quality Assurance: Pre-commit checks, CI/CD pipeline, Definition of Done
- Deployment Checklist: Vercel (frontend), Railway/Render (backend), Neon (database)
- Success Metrics Mapping: 30 success criteria with measurement methods
- Technology Rationale: Why Next.js, FastAPI, SQLModel, Better Auth, Neon, Tailwind

**2. Technical Research (research.md)**:
- Area 1: Better Auth integration (JWT flow, token refresh, dual SDK setup)
- Area 2: Neon PostgreSQL connection (SQLModel + asyncpg, connection pooling, Alembic migrations)
- Area 3: Next.js App Router patterns (Server vs Client Components, middleware auth, data fetching)
- Area 4: CORS & deployment (Vercel + Railway/Render + Neon, environment variables, smoke tests)
- Area 5: Rate limiting & security (slowapi, JWT hardening, XSS prevention, OWASP top 10 checklist)
- All decisions documented with alternatives considered and rationale

**3. Data Model (data-model.md)**:
- User entity: id, email (UNIQUE), password_hash, created_at, updated_at
- Task entity: id, user_id (FK), title (1-100), description (max 500), completed, created_at, updated_at
- JWT Token (transient): Access (15min) + Refresh (7 days)
- Validation rules for all fields
- State transitions (User: Unregistered → Active → Authenticated; Task: Pending ↔ Completed)
- Database schema (PostgreSQL) with indexes and triggers
- SQLModel definitions, Pydantic schemas, TypeScript interfaces
- User isolation enforcement rules (CRITICAL: WHERE user_id filter on all queries)
- Alembic migration script

**4. API Contracts (contracts/)**:

**auth-api.md** (5 endpoints):
- POST /api/auth/register: Create account (rate: 5/min)
- POST /api/auth/login: Authenticate user, issue tokens (rate: 10/min)
- POST /api/auth/logout: Terminate session (rate: 10/min)
- POST /api/auth/refresh: Obtain new access token (rate: 20/min)
- GET /api/auth/me: Get current user profile (rate: 100/min)
- Complete request/response schemas, error handling, cURL examples
- Security considerations, frontend integration examples, testing checklist

**task-api.md** (6 endpoints):
- POST /api/tasks: Create task (rate: 100/min)
- GET /api/tasks: Get all tasks with optional status filter (rate: 100/min)
- GET /api/tasks/:id: Get single task (rate: 100/min)
- PUT /api/tasks/:id: Update task title/description (rate: 100/min)
- PATCH /api/tasks/:id/toggle: Toggle completion status (rate: 100/min)
- DELETE /api/tasks/:id: Delete task (rate: 100/min)
- All endpoints require JWT authentication
- User isolation security implementation
- HTTP status codes reference
- Frontend TypeScript API client examples
- Comprehensive testing checklist (30+ tests)

**5. Quickstart Guide (quickstart.md)**:
- Prerequisites (Node 20+, Python 3.13+, Neon account)
- Quick Setup (5 minutes): Clone, database setup, backend setup, frontend setup, verify
- Detailed setup guides for backend and frontend
- Environment variable templates
- Database migration commands
- Development server commands
- Testing commands
- Common development tasks (migrations, new endpoints, new pages, API testing, database reset)
- Troubleshooting section (backend, frontend, database issues)
- Development workflow (branching, commit conventions)
- Deployment guides (Vercel, Railway, Neon)
- Useful commands reference
- Resources and support links

**6. Agent Context Update (CLAUDE.md)**:
- Phase II Technology Stack Context section added
- Mandatory technologies (Next.js 16+, FastAPI, SQLModel, Better Auth, Neon, Tailwind)
- Key patterns & conventions (App Router, auth flow, user isolation, API contracts, database models, security)
- Testing strategy (React Testing Library, Playwright, pytest)
- Environment variables
- Code references to all planning artifacts
- Common pitfalls to avoid (7 critical issues)
- Performance targets (Lighthouse ≥90, API <200ms p95, DB <100ms p95)
- Architectural decisions summary

**Key Design Decisions**:
- Monorepo structure with frontend/ and backend/ separation
- Better Auth for JWT authentication (access 15min + refresh 7 days in HTTP-only cookies)
- SQLModel with asyncpg for async database operations
- Next.js App Router with Server Components (static) + Client Components (interactive)
- User isolation enforced at query level (WHERE user_id = authenticated_user_id)
- Rate limiting with slowapi (5-100 req/min depending on endpoint)
- CORS whitelist for frontend origin
- Vercel (frontend) + Railway/Render (backend) + Neon (database) deployment

**Implementation Phases** (6-week plan):
- Week 1-2 (Phase 2A): Foundation & Authentication
- Week 3 (Phase 2B): Core Task Management
- Week 4 (Phase 2C): Task Operations & UI Polish
- Week 5 (Phase 2D): Responsive Design & Accessibility
- Week 5 (Phase 2E): Integration Testing & Performance
- Week 6 (Phase 2F): Deployment & Documentation

## Outcome

- ✅ Impact: Complete implementation plan and design artifacts generated, ready for task breakdown
- 🧪 Tests: N/A (planning phase - no code written yet)
- 📁 Files: 7 files created (plan.md, research.md, data-model.md, 2 API contracts, quickstart.md, CLAUDE.md updated)
- 🔁 Next prompts: Run `/sp.tasks` to generate actionable task breakdown from plan; Consider `/sp.adr` for architectural decisions
- 🧠 Reflection: Successfully executed manual plan workflow when PowerShell script unavailable. All Phase 0 research complete (no NEEDS CLARIFICATION markers). All Phase 1 design artifacts generated with comprehensive documentation. Constitution check passed (all mandatory requirements met). Plan includes detailed implementation strategy, risk mitigation, testing approach, deployment checklist, and success metrics mapping. Ready for task generation phase.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script unavailability (pwsh not found) - mitigated by manual workflow execution
- Graders run and results (PASS/FAIL): PASS - All planning artifacts complete, constitution requirements validated, no NEEDS CLARIFICATION markers
- Prompt variant (if applicable): Manual plan workflow (fallback from automated PowerShell script)
- Next experiment (smallest change to try): Execute `/sp.tasks` to generate task breakdown from plan.md; Suggest ADRs for significant decisions (Better Auth selection, Neon PostgreSQL, monorepo structure, deployment strategy)
