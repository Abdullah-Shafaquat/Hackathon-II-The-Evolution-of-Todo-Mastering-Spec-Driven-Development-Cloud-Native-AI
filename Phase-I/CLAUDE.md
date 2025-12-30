# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

---

## Phase II Technology Stack Context

**Last Updated**: 2025-12-30
**Phase**: Phase II - Full-Stack Web Application

### Mandatory Technologies

**Frontend**:
- Next.js 16+ (App Router required) - File-system routing, Server Components, React 19+
- TypeScript (strict mode) - Type safety, interfaces in `src/types/`
- Tailwind CSS - Utility-first styling, responsive breakpoints (mobile <640px, tablet 640-1024px, desktop >1024px)
- Better Auth (client) - JWT authentication state management, auto token refresh

**Backend**:
- Python 3.13+ with FastAPI - Async/await patterns, automatic OpenAPI docs
- SQLModel - ORM combining Pydantic + SQLAlchemy, type-safe queries
- Pydantic - Request/response validation, settings management
- Better Auth (server) - JWT generation, token verification, refresh tokens
- Alembic - Database migrations with version control

**Database**:
- Neon Serverless PostgreSQL - Connection pooling (10-20 connections), asyncpg driver
- PostgreSQL indexes: users.email, tasks.user_id, tasks.created_at (DESC)

**Deployment**:
- Frontend: Vercel (automatic HTTPS, preview deployments)
- Backend: Railway/Render (Python runtime, environment variables)
- Database: Neon (managed PostgreSQL with auto-scaling)

### Key Patterns & Conventions

**Next.js App Router**:
- Server Components (default): Static layouts, pages without interactivity
- Client Components ('use client' directive): Forms, hooks (useState, useEffect, useAuth)
- Middleware (src/middleware.ts): Authentication route protection
- File structure: `src/app/[route]/page.tsx` → `/[route]` URL

**Authentication Flow**:
- Login → Backend issues access_token (JSON, 15min expiry) + refresh_token (HTTP-only cookie, 7 days)
- Frontend stores access_token in memory (React state, NOT localStorage)
- API requests include `Authorization: Bearer {access_token}`
- On 401 error → Call /api/auth/refresh with cookie → New access_token
- On refresh failure → Logout, redirect to /login

**User Isolation (CRITICAL)**:
- ALL task queries MUST include: `WHERE user_id = authenticated_user_id`
- Security test: User A cannot access User B's tasks (404 Not Found, not 403)
- Enforced at SQLModel query level, never skip user_id filter

**API Contracts**:
- RESTful design: POST (create), GET (read), PUT (update), PATCH (toggle), DELETE (delete)
- Authentication endpoints: /api/auth/register, /api/auth/login, /api/auth/logout, /api/auth/refresh
- Task endpoints: /api/tasks (CRUD + toggle), all protected with JWT Bearer token
- Rate limiting: 5 req/min (register), 10 req/min (login), 100 req/min (tasks)
- Error format: `{"detail": "Human-readable message"}` or validation errors with field locations

**Database Models**:
- Users table: id (SERIAL PK), email (UNIQUE), password_hash, created_at, updated_at
- Tasks table: id (SERIAL PK), user_id (FK → users.id ON DELETE CASCADE), title (1-100 chars), description (max 500), completed (BOOLEAN), created_at, updated_at
- Auto-update updated_at with PostgreSQL triggers

**Security Requirements**:
- Password hashing: bcrypt (cost ≥12) or Argon2, NEVER store plaintext
- JWT secrets: 32+ random characters in environment variables
- CORS: Whitelist frontend origin only, allow_credentials=True for cookies
- Input sanitization: Strip HTML tags (bleach library), escape special characters
- HTTPS enforced in production (automatic on Vercel/Railway)

**Testing Strategy**:
- Frontend: React Testing Library (components), Playwright (E2E), Jest (unit tests)
- Backend: pytest (unit + integration), httpx TestClient for API tests
- Target coverage: 80% for unit tests
- E2E tests: Full user journeys (register → login → create tasks → logout)

**Environment Variables**:
- Frontend (.env.local): NEXT_PUBLIC_API_URL (backend API base URL)
- Backend (.env): DATABASE_URL, JWT_SECRET, CORS_ORIGINS, RATE_LIMIT_PER_MINUTE
- NEVER commit .env files to git, use .env.example templates

**Code References**:
- API contracts: specs/001-todo-web-app-phase-ii/contracts/auth-api.md, task-api.md
- Data model: specs/001-todo-web-app-phase-ii/data-model.md
- Research decisions: specs/001-todo-web-app-phase-ii/research.md
- Quickstart guide: specs/001-todo-web-app-phase-ii/quickstart.md

### Common Pitfalls to Avoid

1. **User Isolation Bypass**: Always filter by user_id in task queries, never trust client-provided user_id
2. **CORS Misconfiguration**: Ensure CORS_ORIGINS matches exact frontend URL (protocol + domain + port)
3. **Token Storage**: Access tokens in memory only (React state), refresh tokens in HTTP-only cookies
4. **Server vs Client Components**: Use 'use client' for hooks (useState, useEffect), interactive forms, event handlers
5. **Database Connections**: Use connection pooling (SQLModel async engine), don't create new connection per request
6. **Migration Safety**: Always review auto-generated Alembic migrations, test rollback before deploying
7. **Rate Limiting**: Apply to auth endpoints (prevent brute force), health check endpoint unlimited

### Performance Targets

- Frontend: Lighthouse score ≥90, FCP <2s, LCP <3s
- Backend: API response <200ms (p95), <500ms (p99)
- Database: Query execution <100ms (p95)
- Concurrent users: 50-100 without degradation
- Task capacity: 100 tasks per user without performance impact

### Architectural Decisions Documented

See architecture decision records (ADRs) for rationale on:
- Monorepo structure (frontend/ + backend/ + .specify/)
- Better Auth over NextAuth.js or manual JWT implementation
- Neon PostgreSQL over self-hosted or other managed databases
- Vercel (frontend) + Railway/Render (backend) deployment strategy
- SQLModel ORM over raw SQL or synchronous SQLAlchemy

For implementation guidance, always refer to:
1. Constitution (.specify/memory/constitution.md) for mandatory requirements
2. Feature spec (specs/001-todo-web-app-phase-ii/spec.md) for business requirements
3. API contracts (specs/001-todo-web-app-phase-ii/contracts/) for endpoint specifications
4. Data model (specs/001-todo-web-app-phase-ii/data-model.md) for entity definitions
