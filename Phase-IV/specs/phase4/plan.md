# Phase IV: Technical Implementation Plan

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────┐
│                             MINIKUBE CLUSTER                            │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        INGRESS CONTROLLER                       │   │
│  │                     (nginx-ingress)                             │   │
│  └───────────────────────────────┬─────────────────────────────────┘   │
│                                  │                                      │
│                    ┌─────────────┴─────────────┐                       │
│            ┌───────▼───────┐         ┌─────────▼─────────┐             │
│            │   FRONTEND    │         │     BACKEND       │             │
│            │   Service     │         │     Service       │             │
│            │  (NodePort)   │         │  (ClusterIP)      │             │
│            └───────┬───────┘         └─────────┬─────────┘             │
│                    │                           │                       │
│            ┌───────▼───────┐         ┌─────────▼─────────┐             │
│            │   Frontend    │         │     Backend       │             │
│            │   Deployment  │         │    Deployment     │             │
│            │  (Next.js)    │         │   (FastAPI)       │             │
│            │   2 replicas  │         │    2 replicas     │             │
│            └───────────────┘         └───────────────────┘             │
│                                                                         │
│                          External Connection                           │
│                    ┌─────────────────────────────┐                     │
│                    │      NEON POSTGRESQL        │                     │
│                    │    (Serverless Database)    │                     │
│                    └─────────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────────────┘
```

## COMPONENT BREAKDOWN

### C1: Docker Images

**Frontend Image:**
- Base: node:20-alpine
- Multi-stage build
- Standalone Next.js output
- Non-root user (nextjs:1001)

**Backend Image:**
- Base: python:3.13-slim
- Multi-stage build for smaller size
- Uvicorn ASGI server
- Non-root user (appuser:1000)

### C2: Kubernetes Resources

**Namespace:** `todo-app`

**Resources per component:**

1. **Frontend:**
   - Deployment: 2 replicas, rolling update strategy
   - Service: NodePort on 30080
   - ConfigMap: Frontend environment variables
   - Ingress: Route `/` to frontend

2. **Backend:**
   - Deployment: 2 replicas, rolling update strategy
   - Service: ClusterIP on port 8000
   - ConfigMap: Backend configuration
   - Secret: Database credentials, API keys
   - Ingress: Route `/api/*` to backend

3. **Database Migration:**
   - Job: One-time migration job
   - Runs via Helm hook on install/upgrade

### C3: Helm Chart Structure

```
charts/todo-chatbot/
├── Chart.yaml
├── values.yaml
├── values.local.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── namespace.yaml
│   ├── backend-configmap.yaml
│   ├── backend-secret.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── backend-hpa.yaml
│   ├── frontend-configmap.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── frontend-hpa.yaml
│   ├── ingress.yaml
│   └── migration-job.yaml
```

### C4: Environment Configuration

**Frontend Environment Variables:**
- `NEXT_PUBLIC_API_URL`: Backend service URL

**Backend Environment Variables:**
- `DATABASE_URL`: Neon PostgreSQL connection string
- `GEMINI_API_KEY`: Gemini API key
- `JWT_SECRET`: JWT signing secret

### C5: AI DevOps Integration

1. **kubectl-ai Setup:**
   - Installation script
   - Gemini API configuration
   - Helper scripts for common operations

2. **Docker AI (Gordon):**
   - Enable in Docker Desktop
   - Dockerfile optimization
   - Image security scanning

## IMPLEMENTATION SEQUENCE

### Phase 1: Foundation
1. ✅ Create Dockerfiles for frontend/backend
2. ✅ Create .dockerignore files
3. ✅ Update next.config.js for standalone output

### Phase 2: Kubernetes Deployment
1. ✅ Create basic Kubernetes manifests
2. ✅ Create namespace with quotas
3. ✅ Configure ingress

### Phase 3: Helm Packaging
1. ✅ Create Helm chart structure
2. ✅ Template all resources
3. ✅ Create values files for environments

### Phase 4: AI DevOps
1. ✅ Create kubectl-ai installation script
2. ✅ Create AI-assisted deployment scripts
3. ✅ Create AI troubleshooting scripts
4. ✅ Document AI tool usage

### Phase 5: Deployment Scripts
1. ✅ Minikube setup scripts (bash & Windows)
2. ✅ Image build scripts
3. ✅ Deploy/teardown scripts
4. ✅ Smoke test scripts

### Phase 6: Documentation
1. ✅ Deployment guide
2. ✅ AI DevOps guide
3. ✅ Troubleshooting guide

## DATA FLOW

1. User interacts with Next.js frontend
2. Frontend sends message to backend `/api/chat`
3. Backend processes with Gemini AI
4. Agents call MCP tools for task operations
5. MCP tools interact with Neon database
6. Response returned to frontend
7. Frontend updates UI

## SCALABILITY CONSIDERATIONS

1. **Horizontal Scaling:** Both deployments support multiple replicas
2. **Database:** Neon serverless automatically scales
3. **Stateless Design:** All services are stateless
4. **HPA:** Configured for CPU-based autoscaling

## FAILOVER & RECOVERY

1. **Pod Failure:** Kubernetes automatically restarts pods
2. **Node Failure:** Pods rescheduled on other nodes
3. **Database Failure:** Neon provides high availability
4. **Rollback:** Helm rollback to previous revision
