#!/bin/bash
# Phase IV: Build Docker Images Script
# Builds frontend and backend images for Minikube

set -e

echo "=========================================="
echo "Phase IV: Building Docker Images"
echo "=========================================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "Error: Minikube is not running."
    echo "Run: ./scripts/minikube-setup.sh"
    exit 1
fi

echo ""
echo "Step 1: Configuring Docker to use Minikube's daemon..."
echo "----------------------------------------"

# Set Docker environment to use Minikube's Docker daemon
eval $(minikube docker-env)
echo "  Docker daemon: Minikube"

echo ""
echo "Step 2: Building Backend Image..."
echo "----------------------------------------"

cd "$PROJECT_ROOT/backend"
docker build \
    -t todo-chatbot-backend:latest \
    -f Dockerfile \
    .

echo "  Backend image built successfully"

echo ""
echo "Step 3: Building Frontend Image..."
echo "----------------------------------------"

cd "$PROJECT_ROOT/frontend"

# Build with API URL pointing to the Kubernetes service
docker build \
    -t todo-chatbot-frontend:latest \
    --build-arg NEXT_PUBLIC_API_URL=http://backend-service:8000 \
    -f Dockerfile \
    .

echo "  Frontend image built successfully"

echo ""
echo "Step 4: Verifying Images..."
echo "----------------------------------------"

echo ""
echo "Docker Images:"
docker images | grep todo-chatbot

echo ""
echo "=========================================="
echo "Docker images built successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Deploy application: ./scripts/deploy-local.sh"
echo ""
