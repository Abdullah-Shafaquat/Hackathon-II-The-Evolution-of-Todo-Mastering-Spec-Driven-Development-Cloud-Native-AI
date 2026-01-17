# Phase IV: Local Kubernetes Deployment Specification

## OVERVIEW

Transition the Phase III Todo AI Chatbot from local development to a production-grade local Kubernetes cluster using Minikube. The chatbot must be fully containerized and deployed with Helm charts, using AI-assisted DevOps tools (kubectl-ai, kagent, Docker AI Gordon).

## USER JOURNEYS

### Journey 1: Developer Deploying Locally

**As a** developer
**I want to** deploy the Todo Chatbot to local Kubernetes
**So that** I can test production-like deployment locally

**Steps:**
1. Run `minikube start`
2. Build Docker images
3. Deploy using Helm charts
4. Access application via ingress
5. Verify all services are running
6. Test chatbot functionality

### Journey 2: AI-Assisted Operations

**As a** DevOps engineer
**I want to** use AI tools for Kubernetes operations
**So that** I can manage infrastructure with natural language

**Steps:**
1. Use `kubectl-ai` to create deployments
2. Use `kagent` to analyze cluster health
3. Use Docker AI (Gordon) for container optimization
4. Fix issues with AI assistance

## REQUIREMENTS

### R1: Containerization

**ID:** R1-CONTAINER
**Priority:** High
**Description:** Containerize all Phase III components

**Components:**
1. Frontend (Next.js)
2. Backend (FastAPI + Gemini AI + MCP Server)
3. Database (Neon PostgreSQL - external)

**Acceptance Criteria:**
- [x] Dockerfiles for frontend and backend
- [x] Multi-stage builds for optimization
- [x] `.dockerignore` files
- [x] Images under 500MB each
- [x] Non-root user execution

### R2: Minikube Cluster Setup

**ID:** R2-MINIKUBE
**Priority:** High
**Description:** Set up local Kubernetes cluster

**Requirements:**
1. Minikube with adequate resources
2. Ingress controller enabled
3. Metrics server for HPA
4. Local storage class

**Acceptance Criteria:**
- [x] `minikube start --cpus=4 --memory=8192`
- [x] Ingress addon enabled
- [x] Metrics server running
- [x] Storage provisioner configured

### R3: Kubernetes Manifests

**ID:** R3-MANIFESTS
**Priority:** High
**Description:** Create Kubernetes deployment manifests

**Resources Needed:**
1. Deployments for frontend and backend
2. Services for internal and external access
3. ConfigMaps for environment variables
4. Secrets for sensitive data
5. Ingress for routing

**Acceptance Criteria:**
- [x] Deployment with 2 replicas minimum
- [x] Services with proper selectors
- [x] Ingress routing to both services
- [x] Liveness and readiness probes
- [x] Resource limits defined

### R4: Helm Charts

**ID:** R4-HELM
**Priority:** High
**Description:** Package deployment as Helm charts

**Components:**
1. Chart for frontend
2. Chart for backend
3. Values files for different environments
4. Template for ConfigMaps and Secrets

**Acceptance Criteria:**
- [x] `helm create` structure
- [x] Templates for all resources
- [x] Values.yaml with defaults
- [x] Local values file for Minikube
- [x] Chart.yaml with metadata

### R5: AI DevOps Integration

**ID:** R5-AIDEVOPS
**Priority:** High
**Description:** Integrate AI tools for Kubernetes management

**Tools:**
1. kubectl-ai for command generation
2. kagent for cluster analysis
3. Docker AI (Gordon) for container help

**Acceptance Criteria:**
- [x] Installation scripts created
- [x] AI-assisted deployment script
- [x] AI troubleshooting script
- [x] Documentation provided

### R6: Database Integration

**ID:** R6-DATABASE
**Priority:** High
**Description:** Connect to external Neon PostgreSQL

**Requirements:**
1. Database connection via environment variables
2. SSL/TLS encryption
3. Migration job for schema

**Acceptance Criteria:**
- [x] Database URL from environment
- [x] SSL connection configured
- [x] Migration job Kubernetes Job

### R7: Monitoring & Health

**ID:** R7-MONITORING
**Priority:** Medium
**Description:** Implement basic monitoring

**Components:**
1. Health endpoints
2. Log aggregation
3. Resource usage monitoring

**Acceptance Criteria:**
- [x] `/health` endpoints
- [x] Structured logging
- [x] Resource requests/limits

## TECHNICAL CONSTRAINTS

1. Use Python 3.13+ for backend
2. Use Node.js 20+ for frontend
3. PostgreSQL 15+ for database
4. Kubernetes 1.28+
5. Helm 3.12+

## DEPENDENCIES

- Phase III codebase (GitHub repository)
- Docker Desktop with Gordon AI enabled
- Minikube installed
- kubectl, helm CLI tools
- Neon PostgreSQL database URL
- Gemini API Key
