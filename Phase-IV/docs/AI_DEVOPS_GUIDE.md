# Phase IV: AI DevOps Tools Guide

This guide covers using AI-powered tools for Kubernetes operations and container management.

## Overview

Phase IV integrates three AI-assisted DevOps tools:

1. **kubectl-ai** - AI-powered Kubernetes command generation
2. **kagent** - Kubernetes AI agent for cluster analysis
3. **Docker AI (Gordon)** - Docker Desktop's built-in AI assistant

## kubectl-ai

### Installation

#### macOS (Homebrew)
```bash
brew install sozercan/kubectl-ai/kubectl-ai
```

#### Linux/Windows (krew)
```bash
kubectl krew install ai
```

#### Manual Download
Download from: https://github.com/sozercan/kubectl-ai/releases

### Configuration

Set your API key:

```bash
# For Gemini (recommended - free tier)
export GEMINI_API_KEY=your-gemini-api-key

# For OpenAI
export OPENAI_API_KEY=your-openai-api-key
```

### Usage Examples

#### Generate Manifests

```bash
# Create a deployment
kubectl ai "create a deployment for nginx with 3 replicas and a service"

# Create a ConfigMap
kubectl ai "create a configmap named app-config with DATABASE_URL set to postgresql://localhost/db"

# Create an Ingress
kubectl ai "create an ingress for my-app service on port 8080 with host my-app.local"
```

#### Troubleshooting

```bash
# Analyze pod issues
kubectl ai "why is my pod crashing in namespace todo-app"

# Check resource usage
kubectl ai "show me which pods are using the most memory"

# Debug networking
kubectl ai "why can't my frontend pod connect to the backend service"
```

#### Operations

```bash
# Scale deployment
kubectl ai "scale the backend deployment to 5 replicas in namespace todo-app"

# Rollback
kubectl ai "rollback the frontend deployment to the previous version"

# Port forwarding
kubectl ai "forward port 8080 from the backend pod to local port 8000"
```

#### Information Queries

```bash
# List resources
kubectl ai "list all pods with high memory usage"

# Get status
kubectl ai "show me the health status of all deployments"

# Find logs
kubectl ai "show me the last 50 error logs from the backend"
```

## Docker AI (Gordon)

### Enabling Docker AI

1. Open Docker Desktop
2. Go to **Settings** > **Features in development**
3. Enable **Docker AI (Gordon)**
4. Restart Docker Desktop

### Usage Examples

#### Dockerfile Optimization

```bash
docker ai "analyze my Dockerfile and suggest optimizations"
docker ai "how can I reduce the size of my Docker image"
docker ai "what security issues does my Dockerfile have"
```

#### Container Debugging

```bash
docker ai "why is my container exiting immediately"
docker ai "debug network connectivity issues in my container"
docker ai "why is my container using too much memory"
```

#### Best Practices

```bash
docker ai "review my docker-compose.yml for best practices"
docker ai "how should I structure my multi-stage Dockerfile"
docker ai "what's the best base image for a Python 3.13 application"
```

## kagent (Kubernetes AI Agent)

### Installation

```bash
# Install via Helm
helm repo add kagent https://kagent-ai.github.io/charts
helm install kagent kagent/kagent --namespace kagent-system --create-namespace
```

### Configuration

Create a ConfigMap with your API key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kagent-config
  namespace: kagent-system
type: Opaque
stringData:
  GEMINI_API_KEY: your-api-key
```

### Usage

kagent runs as a Kubernetes operator and provides:

- Automated cluster health monitoring
- AI-powered recommendations
- Anomaly detection
- Resource optimization suggestions

Check kagent status:
```bash
kubectl get pods -n kagent-system
kubectl logs -n kagent-system -l app=kagent
```

## AI-Assisted Deployment Workflow

### 1. Pre-deployment Analysis

```bash
# Check cluster readiness
kubectl ai "is my cluster ready for a new deployment? Check resources and health"

# Validate manifests
kubectl ai "validate my deployment yaml for best practices"
```

### 2. Deployment

Use the AI-assisted deployment script:

```bash
./scripts/ai-deploy.sh
```

This script:
1. Analyzes cluster state
2. Deploys using Helm
3. Verifies deployment with AI
4. Provides optimization recommendations

### 3. Post-deployment Verification

```bash
# AI health check
kubectl ai "verify that the todo-app deployment is healthy"

# Performance analysis
kubectl ai "analyze the performance of pods in todo-app namespace"
```

### 4. Troubleshooting

Use the AI troubleshooting script:

```bash
./scripts/ai-troubleshoot.sh
```

## Common AI Commands for Phase IV

### Deployment Operations

```bash
# Deploy full stack
kubectl ai "deploy a todo app with frontend and backend services"

# Update configuration
kubectl ai "update the backend configmap to change the API port to 9000"

# Rolling update
kubectl ai "perform a rolling update on the frontend deployment"
```

### Monitoring

```bash
# Resource monitoring
kubectl ai "show me CPU and memory usage for all pods in todo-app"

# Log analysis
kubectl ai "find errors in the backend logs from the last hour"

# Event monitoring
kubectl ai "show me warning events in the todo-app namespace"
```

### Scaling

```bash
# HPA status
kubectl ai "check the HPA configuration and current scaling status"

# Manual scaling
kubectl ai "scale frontend to handle more traffic"

# Resource adjustment
kubectl ai "increase memory limits for the backend pods"
```

## Tips and Best Practices

### 1. Be Specific

```bash
# Too vague
kubectl ai "fix my pod"

# Better
kubectl ai "why is my backend pod in namespace todo-app showing CrashLoopBackOff"
```

### 2. Provide Context

```bash
# Include namespace and labels
kubectl ai "list pods with label app=backend in namespace todo-app"
```

### 3. Request Explanations

```bash
# Ask for explanations
kubectl ai "explain why my HPA isn't scaling up"

# Ask for recommendations
kubectl ai "what's the best resource limit for a FastAPI application"
```

### 4. Combine with kubectl

```bash
# Pipe output to AI
kubectl get pods -n todo-app -o yaml | kubectl ai "analyze these pod specs"

# Use AI-generated commands
kubectl ai "show me the command to delete stuck pods"
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Commands**: Review AI-generated commands before executing
3. **Permissions**: Ensure AI tools have appropriate RBAC permissions
4. **Sensitive Data**: Be careful about exposing secrets in AI queries

## Fallback Procedures

If AI tools are unavailable:

```bash
# Standard deployment
./scripts/deploy-local.sh

# Manual troubleshooting
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
kubectl get events -n todo-app
```
