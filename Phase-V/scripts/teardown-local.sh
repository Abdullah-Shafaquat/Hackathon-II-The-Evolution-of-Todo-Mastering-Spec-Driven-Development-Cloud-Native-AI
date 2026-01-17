#!/bin/bash
# Phase IV: Teardown Script
# Removes the Todo Chatbot deployment from Minikube

set -e

echo "=========================================="
echo "Phase IV: Teardown Deployment"
echo "=========================================="

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "Error: helm is not installed."
    exit 1
fi

echo ""
echo "This will remove the following:"
echo "  - Helm release: todo-chatbot"
echo "  - Namespace: todo-app"
echo ""

read -p "Continue? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Teardown cancelled."
    exit 0
fi

echo ""
echo "Step 1: Uninstalling Helm release..."
echo "----------------------------------------"

helm uninstall todo-chatbot -n todo-app 2>/dev/null || echo "  Release not found or already removed"

echo ""
echo "Step 2: Deleting namespace..."
echo "----------------------------------------"

kubectl delete namespace todo-app --ignore-not-found=true

echo ""
echo "=========================================="
echo "Teardown completed!"
echo "=========================================="
echo ""
echo "The application has been removed from Minikube."
echo "Minikube cluster is still running."
echo ""
echo "To stop Minikube: minikube stop"
echo "To delete Minikube: minikube delete"
echo ""
