#!/bin/bash
# Phase IV: AI-Assisted Deployment Script
# Uses kubectl-ai for intelligent deployment assistance

set -e

echo "=========================================="
echo "Phase IV: AI-Assisted Deployment"
echo "=========================================="

# Check if kubectl-ai is available
if ! command -v kubectl-ai &> /dev/null && ! kubectl ai --version &> /dev/null 2>&1; then
    echo "Warning: kubectl-ai is not installed."
    echo "Falling back to standard deployment."
    echo ""
    exec ./scripts/deploy-local.sh
fi

# Check for API key
if [ -z "$GEMINI_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: No API key found for kubectl-ai."
    echo "Set GEMINI_API_KEY or OPENAI_API_KEY environment variable."
    echo ""
    echo "Falling back to standard deployment."
    exec ./scripts/deploy-local.sh
fi

echo ""
echo "Using kubectl-ai for intelligent deployment..."
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Step 1: Analyzing current cluster state..."
echo "----------------------------------------"
echo ""

# Use AI to check cluster health
kubectl ai "Check if the todo-app namespace exists and show its status"

echo ""
echo "Step 2: Checking for existing deployments..."
echo "----------------------------------------"
echo ""

kubectl ai "List all deployments in the todo-app namespace and their status"

echo ""
echo "Step 3: Deploying application with Helm..."
echo "----------------------------------------"
echo ""

# Standard Helm deployment
cd "$PROJECT_ROOT"
helm upgrade --install todo-chatbot ./charts/todo-chatbot \
    -f ./charts/todo-chatbot/values.local.yaml \
    --namespace todo-app \
    --create-namespace \
    --wait \
    --timeout 5m

echo ""
echo "Step 4: AI-Assisted Deployment Verification..."
echo "----------------------------------------"
echo ""

# Use AI to verify deployment
kubectl ai "Check the health of all pods in the todo-app namespace and report any issues"

echo ""
echo "Step 5: AI Recommendations..."
echo "----------------------------------------"
echo ""

kubectl ai "Analyze the todo-app namespace deployment and provide optimization recommendations"

echo ""
echo "=========================================="
echo "AI-Assisted Deployment Complete!"
echo "=========================================="
