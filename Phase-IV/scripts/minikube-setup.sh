#!/bin/bash
# Phase IV: Minikube Setup Script
# Sets up a local Kubernetes cluster with required addons

set -e

echo "=========================================="
echo "Phase IV: Minikube Cluster Setup"
echo "=========================================="

# Check if minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Error: minikube is not installed."
    echo "Install from: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed."
    echo "Install from: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Error: Docker is not running."
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo ""
echo "Step 1: Starting Minikube cluster..."
echo "----------------------------------------"

# Start minikube with recommended resources
minikube start \
    --cpus=4 \
    --memory=8192 \
    --disk-size=20gb \
    --driver=docker \
    --kubernetes-version=v1.28.0

echo ""
echo "Step 2: Enabling required addons..."
echo "----------------------------------------"

# Enable ingress controller
minikube addons enable ingress
echo "  - Ingress controller enabled"

# Enable metrics server for HPA
minikube addons enable metrics-server
echo "  - Metrics server enabled"

# Enable dashboard (optional)
minikube addons enable dashboard
echo "  - Dashboard enabled"

# Enable storage provisioner
minikube addons enable storage-provisioner
echo "  - Storage provisioner enabled"

echo ""
echo "Step 3: Waiting for addons to be ready..."
echo "----------------------------------------"

# Wait for ingress controller
kubectl wait --namespace ingress-nginx \
    --for=condition=ready pod \
    --selector=app.kubernetes.io/component=controller \
    --timeout=300s 2>/dev/null || echo "  - Ingress controller starting..."

# Wait for metrics server
kubectl wait --namespace kube-system \
    --for=condition=ready pod \
    --selector=k8s-app=metrics-server \
    --timeout=120s 2>/dev/null || echo "  - Metrics server starting..."

echo ""
echo "Step 4: Cluster Information"
echo "----------------------------------------"
echo ""
echo "Cluster Status:"
minikube status

echo ""
echo "Kubectl Context:"
kubectl config current-context

echo ""
echo "Cluster Nodes:"
kubectl get nodes

echo ""
echo "=========================================="
echo "Minikube cluster is ready!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Build Docker images: ./scripts/build-images.sh"
echo "  2. Deploy application: ./scripts/deploy-local.sh"
echo "  3. Access dashboard:   minikube dashboard"
echo ""
echo "To add todo.local to your hosts file:"
echo "  echo \"\$(minikube ip) todo.local\" | sudo tee -a /etc/hosts"
echo ""
