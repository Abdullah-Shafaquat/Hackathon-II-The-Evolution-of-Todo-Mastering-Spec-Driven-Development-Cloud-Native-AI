# Phase IV: Local Kubernetes Deployment Guide

This guide covers deploying the Todo AI Chatbot to a local Kubernetes cluster using Minikube.

## Prerequisites

Before starting, ensure you have the following installed:

1. **Docker Desktop** (with 4+ GB RAM allocated)
   - Download: https://www.docker.com/products/docker-desktop

2. **Minikube** (v1.28+)
   - Download: https://minikube.sigs.k8s.io/docs/start/

3. **kubectl** (v1.28+)
   - Download: https://kubernetes.io/docs/tasks/tools/

4. **Helm** (v3.12+)
   - Download: https://helm.sh/docs/intro/install/

5. **Neon PostgreSQL Database**
   - Create free database: https://neon.tech

6. **Gemini API Key**
   - Get free key: https://aistudio.google.com/app/apikey

## Quick Start

### Windows

```powershell
# 1. Start Minikube
.\scripts\minikube-setup.bat

# 2. Update secrets in values.local.yaml
notepad .\charts\todo-chatbot\values.local.yaml

# 3. Deploy
.\scripts\deploy-local.bat
```

### Linux/macOS

```bash
# 1. Make scripts executable
chmod +x scripts/*.sh

# 2. Start Minikube
./scripts/minikube-setup.sh

# 3. Update secrets
nano ./charts/todo-chatbot/values.local.yaml

# 4. Build images
./scripts/build-images.sh

# 5. Deploy
./scripts/deploy-local.sh
```

## Configuration

### Required Secrets

Edit `charts/todo-chatbot/values.local.yaml` with your actual values:

```yaml
backend:
  secrets:
    DATABASE_URL: "postgresql://user:pass@host/dbname?sslmode=require"
    BETTER_AUTH_SECRET: "your-32-char-secret"
    JWT_SECRET_KEY: "your-jwt-secret"
    GEMINI_API_KEY: "your-gemini-api-key"
```

### Environment-Specific Values

| Environment | Values File | Description |
|-------------|-------------|-------------|
| Local | `values.local.yaml` | Minikube with minimal resources |
| Development | `values.yaml` | Default values for dev |
| Production | `values.prod.yaml` | Full resources (create as needed) |

## Deployment Steps

### Step 1: Start Minikube

```bash
minikube start --cpus=4 --memory=8192 --disk-size=20gb
minikube addons enable ingress
minikube addons enable metrics-server
```

### Step 2: Configure Docker Environment

```bash
# Linux/macOS
eval $(minikube docker-env)

# Windows PowerShell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

### Step 3: Build Docker Images

```bash
# Backend
cd backend
docker build -t todo-chatbot-backend:latest .
cd ..

# Frontend
cd frontend
docker build -t todo-chatbot-frontend:latest \
  --build-arg NEXT_PUBLIC_API_URL=http://backend-service:8000 .
cd ..
```

### Step 4: Deploy with Helm

```bash
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
  -f ./charts/todo-chatbot/values.local.yaml \
  --namespace todo-app \
  --create-namespace \
  --wait
```

### Step 5: Access the Application

```bash
# Get the URL
minikube service todo-chatbot-frontend -n todo-app --url

# Or use NodePort
echo "http://$(minikube ip):30080"

# Or configure Ingress
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
# Then access http://todo.local
```

## Verification

### Check Pod Status

```bash
kubectl get pods -n todo-app
```

Expected output:
```
NAME                                    READY   STATUS    RESTARTS   AGE
todo-chatbot-backend-xxx                1/1     Running   0          2m
todo-chatbot-frontend-xxx               1/1     Running   0          2m
```

### Run Smoke Tests

```bash
./scripts/smoke-test.sh
```

### View Logs

```bash
# Backend logs
kubectl logs -n todo-app -l app=backend -f

# Frontend logs
kubectl logs -n todo-app -l app=frontend -f
```

## Troubleshooting

### Common Issues

#### 1. Pods stuck in Pending

```bash
# Check events
kubectl describe pod <pod-name> -n todo-app

# Common fix: Increase Minikube resources
minikube stop
minikube start --cpus=4 --memory=8192
```

#### 2. Database Connection Failed

```bash
# Verify secret is set
kubectl get secret backend-secrets -n todo-app -o yaml

# Test database connectivity
kubectl run pg-test --rm -it --image=postgres:15 -- \
  psql "postgresql://user:pass@host/db?sslmode=require"
```

#### 3. Image Pull Errors

```bash
# Ensure you're using Minikube's Docker
eval $(minikube docker-env)
docker images | grep todo-chatbot
```

#### 4. Ingress Not Working

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Verify ingress resource
kubectl get ingress -n todo-app
```

### AI-Assisted Troubleshooting

If you have kubectl-ai installed:

```bash
./scripts/ai-troubleshoot.sh
```

## Scaling

### Manual Scaling

```bash
kubectl scale deployment todo-chatbot-backend -n todo-app --replicas=3
```

### Horizontal Pod Autoscaler

HPA is configured by default. Check status:

```bash
kubectl get hpa -n todo-app
```

## Cleanup

### Remove Deployment (Keep Minikube)

```bash
./scripts/teardown-local.sh
```

### Full Cleanup

```bash
minikube delete
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         MINIKUBE CLUSTER                        │
│                                                                 │
│  ┌──────────────────┐     ┌───────────────────────────────┐   │
│  │  Ingress (nginx) │────▶│  todo.local                   │   │
│  └────────┬─────────┘     │  /api/* → backend:8000        │   │
│           │               │  /*     → frontend:3000       │   │
│           │               └───────────────────────────────┘   │
│     ┌─────┴─────┐                                              │
│     │           │                                              │
│     ▼           ▼                                              │
│ ┌────────┐ ┌────────┐        ┌─────────────────────────┐      │
│ │Frontend│ │Backend │───────▶│  Neon PostgreSQL        │      │
│ │ (2x)   │ │ (2x)   │        │  (External Database)    │      │
│ └────────┘ └────────┘        └─────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Next Steps

- Set up CI/CD pipeline for automated deployments
- Configure monitoring with Prometheus/Grafana
- Add TLS/SSL certificates for production
- Consider cloud deployment (Phase V)
