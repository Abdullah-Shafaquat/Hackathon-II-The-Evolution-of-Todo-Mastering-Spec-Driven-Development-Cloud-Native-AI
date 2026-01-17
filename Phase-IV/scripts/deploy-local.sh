#!/bin/bash
# Phase IV: Local Deployment Script
# Deploys the Todo Chatbot to Minikube using Helm

set -e

echo "=========================================="
echo "Phase IV: Deploying to Minikube"
echo "=========================================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CHART_DIR="$PROJECT_ROOT/charts/todo-chatbot"

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "Error: Minikube is not running."
    echo "Run: ./scripts/minikube-setup.sh"
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed."
    echo "Install from: https://helm.sh/docs/intro/install/"
    exit 1
fi

# Check if images exist
eval $(minikube docker-env)
if ! docker images | grep -q "todo-chatbot-backend"; then
    echo "Error: Backend image not found."
    echo "Run: ./scripts/build-images.sh"
    exit 1
fi

if ! docker images | grep -q "todo-chatbot-frontend"; then
    echo "Error: Frontend image not found."
    echo "Run: ./scripts/build-images.sh"
    exit 1
fi

echo ""
echo "Step 1: Validating Helm Chart..."
echo "----------------------------------------"

cd "$PROJECT_ROOT"
helm lint "$CHART_DIR"
echo "  Helm chart validation passed"

echo ""
echo "Step 2: Installing/Upgrading Application..."
echo "----------------------------------------"

# Check if values.local.yaml has been configured
if grep -q "YOUR_PASSWORD" "$CHART_DIR/values.local.yaml"; then
    echo ""
    echo "WARNING: Default secrets detected in values.local.yaml"
    echo "Please update the following values before deployment:"
    echo "  - DATABASE_URL"
    echo "  - BETTER_AUTH_SECRET"
    echo "  - JWT_SECRET_KEY"
    echo "  - GEMINI_API_KEY"
    echo ""
    read -p "Continue with default values? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled. Update values.local.yaml and try again."
        exit 1
    fi
fi

# Install or upgrade the release
helm upgrade --install todo-chatbot "$CHART_DIR" \
    -f "$CHART_DIR/values.local.yaml" \
    --namespace todo-app \
    --create-namespace \
    --wait \
    --timeout 5m

echo ""
echo "Step 3: Waiting for pods to be ready..."
echo "----------------------------------------"

kubectl wait --namespace todo-app \
    --for=condition=ready pod \
    --selector=app=backend \
    --timeout=180s

kubectl wait --namespace todo-app \
    --for=condition=ready pod \
    --selector=app=frontend \
    --timeout=180s

echo ""
echo "Step 4: Deployment Status..."
echo "----------------------------------------"

echo ""
echo "Pods:"
kubectl get pods -n todo-app

echo ""
echo "Services:"
kubectl get services -n todo-app

echo ""
echo "Ingress:"
kubectl get ingress -n todo-app

echo ""
echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo ""

# Get access URLs
MINIKUBE_IP=$(minikube ip)
NODEPORT=$(kubectl get svc -n todo-app todo-chatbot-frontend -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null || echo "30080")

echo "Access the application:"
echo ""
echo "  Via NodePort:  http://${MINIKUBE_IP}:${NODEPORT}"
echo "  Via Ingress:   http://todo.local (add to /etc/hosts)"
echo ""
echo "Add to /etc/hosts:"
echo "  echo \"${MINIKUBE_IP} todo.local\" | sudo tee -a /etc/hosts"
echo ""
echo "Useful commands:"
echo "  View logs:     kubectl logs -n todo-app -l app=backend -f"
echo "  View pods:     kubectl get pods -n todo-app"
echo "  Dashboard:     minikube dashboard"
echo ""
