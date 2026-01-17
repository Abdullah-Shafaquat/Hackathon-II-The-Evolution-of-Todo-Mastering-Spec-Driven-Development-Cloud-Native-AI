# Phase IV: Troubleshooting Guide

Common issues and solutions for the Phase IV Kubernetes deployment.

## Quick Diagnostics

Run these commands first to understand the current state:

```bash
# Overall cluster status
minikube status

# Pod status
kubectl get pods -n todo-app

# Service status
kubectl get svc -n todo-app

# Recent events
kubectl get events -n todo-app --sort-by='.lastTimestamp' | tail -20
```

## Common Issues

### 1. Minikube Won't Start

**Symptoms:**
- `minikube start` fails
- Error about hypervisor or Docker

**Solutions:**

```bash
# Clean start
minikube delete
minikube start --cpus=4 --memory=8192 --driver=docker

# Check Docker is running
docker info

# Try different driver
minikube start --driver=virtualbox  # Alternative driver
```

### 2. Pods Stuck in Pending

**Symptoms:**
- Pods show `Pending` status
- No containers starting

**Diagnosis:**
```bash
kubectl describe pod <pod-name> -n todo-app
```

**Common Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Insufficient resources | `minikube stop && minikube start --cpus=4 --memory=8192` |
| Node not ready | `kubectl get nodes` - wait for Ready status |
| Image pull failure | Check image name, ensure Minikube Docker env is set |

### 3. Pods in CrashLoopBackOff

**Symptoms:**
- Pod keeps restarting
- Status shows `CrashLoopBackOff`

**Diagnosis:**
```bash
kubectl logs <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app --previous  # Previous crash logs
```

**Common Causes & Solutions:**

**Backend crashes:**
```bash
# Check database connection
kubectl logs -n todo-app -l app=backend | grep -i "database\|connection"

# Verify secrets
kubectl get secret backend-secrets -n todo-app -o yaml
```

**Frontend crashes:**
```bash
# Check build errors
kubectl logs -n todo-app -l app=frontend

# Verify API URL configuration
kubectl get configmap frontend-config -n todo-app -o yaml
```

### 4. Image Pull Errors

**Symptoms:**
- `ErrImagePull` or `ImagePullBackOff` status

**Solutions:**

```bash
# Ensure Minikube Docker environment is set
eval $(minikube docker-env)

# Verify images exist
docker images | grep todo-chatbot

# Rebuild if missing
./scripts/build-images.sh
```

### 5. Service Not Accessible

**Symptoms:**
- Cannot access frontend URL
- Connection refused

**Solutions:**

```bash
# Check service exists
kubectl get svc -n todo-app

# Get access URL
minikube service todo-chatbot-frontend -n todo-app --url

# Port forward for testing
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 -n todo-app
```

### 6. Database Connection Issues

**Symptoms:**
- Backend logs show database errors
- API returns 500 errors

**Diagnosis:**
```bash
kubectl logs -n todo-app -l app=backend | grep -i "database\|postgres\|connection"
```

**Solutions:**

```bash
# Verify DATABASE_URL secret
kubectl get secret backend-secrets -n todo-app -o jsonpath='{.data.DATABASE_URL}' | base64 -d

# Test connection manually
kubectl run pg-test --rm -it --image=postgres:15-alpine -n todo-app -- \
  psql "YOUR_DATABASE_URL"

# Check Neon dashboard for connection limits
```

### 7. Ingress Not Working

**Symptoms:**
- http://todo.local not accessible
- 404 or connection errors

**Solutions:**

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress resource
kubectl describe ingress -n todo-app

# Verify hosts file (add if missing)
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Restart ingress controller
kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx
```

### 8. HPA Not Scaling

**Symptoms:**
- HPA shows `unknown` metrics
- Pods not scaling

**Solutions:**

```bash
# Check metrics server
kubectl get pods -n kube-system | grep metrics-server

# Verify HPA
kubectl describe hpa -n todo-app

# Enable metrics addon
minikube addons enable metrics-server
```

### 9. Secrets Not Applied

**Symptoms:**
- Environment variables empty
- Auth failures

**Solutions:**

```bash
# Verify secret exists
kubectl get secret backend-secrets -n todo-app

# Check secret content (decode base64)
kubectl get secret backend-secrets -n todo-app -o jsonpath='{.data}' | jq

# Recreate secret
kubectl delete secret backend-secrets -n todo-app
kubectl apply -f k8s/base/backend/secret.yaml
kubectl rollout restart deployment todo-chatbot-backend -n todo-app
```

### 10. Migration Job Fails

**Symptoms:**
- Database tables not created
- Job shows `Failed` status

**Diagnosis:**
```bash
kubectl logs job/todo-chatbot-migration -n todo-app
```

**Solutions:**

```bash
# Delete failed job and retry
kubectl delete job todo-chatbot-migration -n todo-app
helm upgrade todo-chatbot ./charts/todo-chatbot -f ./charts/todo-chatbot/values.local.yaml -n todo-app

# Run migration manually
kubectl exec -it deployment/todo-chatbot-backend -n todo-app -- python -c "from app.database import create_db_and_tables; create_db_and_tables()"
```

## Health Check Commands

```bash
# Full health check
./scripts/smoke-test.sh

# Backend health
curl http://$(minikube ip):30080/health

# Check all resources
kubectl get all -n todo-app
```

## Log Analysis

```bash
# Backend logs (follow)
kubectl logs -n todo-app -l app=backend -f

# Frontend logs (follow)
kubectl logs -n todo-app -l app=frontend -f

# All logs with timestamps
kubectl logs -n todo-app --all-containers=true --timestamps=true --since=1h

# Search for errors
kubectl logs -n todo-app -l app=backend | grep -i "error\|exception\|failed"
```

## Resource Monitoring

```bash
# Pod resource usage
kubectl top pods -n todo-app

# Node resource usage
kubectl top nodes

# Detailed pod info
kubectl describe pod <pod-name> -n todo-app | grep -A 5 "Resources:"
```

## Reset and Recovery

### Soft Reset (Keep Minikube)

```bash
# Uninstall and reinstall
helm uninstall todo-chatbot -n todo-app
./scripts/build-images.sh
./scripts/deploy-local.sh
```

### Hard Reset (Full Cleanup)

```bash
# Delete everything
minikube delete

# Fresh start
./scripts/minikube-setup.sh
./scripts/build-images.sh
./scripts/deploy-local.sh
```

## Getting Help

1. **Check documentation**: `docs/DEPLOYMENT_GUIDE.md`
2. **AI troubleshooting**: `./scripts/ai-troubleshoot.sh`
3. **View dashboard**: `minikube dashboard`
4. **Community**: Open an issue on GitHub

## AI-Assisted Debugging

If you have kubectl-ai installed:

```bash
# Comprehensive analysis
kubectl ai "analyze all issues in the todo-app namespace and provide solutions"

# Specific issue
kubectl ai "why is the backend pod crashing"

# Performance
kubectl ai "identify performance bottlenecks in todo-app"
```
