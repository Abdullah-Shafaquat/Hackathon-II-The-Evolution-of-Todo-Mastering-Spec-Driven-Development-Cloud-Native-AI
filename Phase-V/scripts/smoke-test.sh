#!/bin/bash
# Phase IV: Smoke Test Script
# Tests the deployed application

set -e

echo "=========================================="
echo "Phase IV: Running Smoke Tests"
echo "=========================================="

# Get Minikube IP and NodePort
MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "localhost")
NODEPORT=$(kubectl get svc -n todo-app todo-chatbot-frontend -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null || echo "30080")
BACKEND_URL="http://${MINIKUBE_IP}:${NODEPORT}"

# For backend testing, use port-forward
echo ""
echo "Setting up port-forward for backend testing..."
kubectl port-forward -n todo-app svc/todo-chatbot-backend 8000:8000 &
PF_PID=$!
sleep 3

BACKEND_DIRECT="http://localhost:8000"

echo ""
echo "Test Configuration:"
echo "  Frontend URL: ${BACKEND_URL}"
echo "  Backend URL:  ${BACKEND_DIRECT}"
echo ""

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local url="$2"
    local expected="$3"

    echo -n "  Testing ${name}... "

    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)

    if [ "$response" == "$expected" ]; then
        echo "PASSED (HTTP $response)"
        ((PASSED++))
    else
        echo "FAILED (Expected $expected, got $response)"
        ((FAILED++))
    fi
}

echo ""
echo "Running Tests..."
echo "----------------------------------------"

# Backend health check
run_test "Backend Health" "${BACKEND_DIRECT}/health" "200"

# Backend root endpoint
run_test "Backend Root" "${BACKEND_DIRECT}/" "200"

# Frontend homepage
run_test "Frontend Homepage" "${BACKEND_URL}/" "200"

# Check pods are running
echo ""
echo "Checking Pod Status..."
echo "----------------------------------------"

BACKEND_PODS=$(kubectl get pods -n todo-app -l app=backend --no-headers 2>/dev/null | grep -c "Running" || echo "0")
FRONTEND_PODS=$(kubectl get pods -n todo-app -l app=frontend --no-headers 2>/dev/null | grep -c "Running" || echo "0")

echo "  Backend pods running: ${BACKEND_PODS}"
echo "  Frontend pods running: ${FRONTEND_PODS}"

if [ "$BACKEND_PODS" -ge 1 ]; then
    echo "  Backend pods: PASSED"
    ((PASSED++))
else
    echo "  Backend pods: FAILED"
    ((FAILED++))
fi

if [ "$FRONTEND_PODS" -ge 1 ]; then
    echo "  Frontend pods: PASSED"
    ((PASSED++))
else
    echo "  Frontend pods: FAILED"
    ((FAILED++))
fi

# Cleanup port-forward
kill $PF_PID 2>/dev/null || true

echo ""
echo "=========================================="
echo "Smoke Test Results"
echo "=========================================="
echo ""
echo "  Passed: ${PASSED}"
echo "  Failed: ${FAILED}"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "All smoke tests PASSED!"
    exit 0
else
    echo "Some tests FAILED. Check the deployment."
    exit 1
fi
