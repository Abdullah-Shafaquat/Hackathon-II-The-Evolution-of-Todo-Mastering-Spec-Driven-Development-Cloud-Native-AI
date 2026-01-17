#!/bin/bash
# Phase IV: AI-Assisted Troubleshooting Script
# Uses kubectl-ai and Docker AI for intelligent debugging

set -e

echo "=========================================="
echo "Phase IV: AI-Assisted Troubleshooting"
echo "=========================================="

# Check if kubectl-ai is available
HAS_KUBECTL_AI=false
if command -v kubectl-ai &> /dev/null || kubectl ai --version &> /dev/null 2>&1; then
    HAS_KUBECTL_AI=true
fi

if [ "$HAS_KUBECTL_AI" = false ]; then
    echo "Warning: kubectl-ai is not installed."
    echo "Install it for AI-assisted troubleshooting."
    echo ""
fi

NAMESPACE="${1:-todo-app}"

echo ""
echo "Troubleshooting namespace: $NAMESPACE"
echo ""

echo "Step 1: Pod Status Analysis"
echo "----------------------------------------"
echo ""

# Get pod status
kubectl get pods -n "$NAMESPACE" -o wide

echo ""
echo "Step 2: Checking for Failed Pods..."
echo "----------------------------------------"
echo ""

FAILED_PODS=$(kubectl get pods -n "$NAMESPACE" --field-selector=status.phase!=Running,status.phase!=Succeeded -o jsonpath='{.items[*].metadata.name}' 2>/dev/null)

if [ -n "$FAILED_PODS" ]; then
    echo "Found problematic pods: $FAILED_PODS"
    echo ""

    for pod in $FAILED_PODS; do
        echo "--- Logs for $pod ---"
        kubectl logs -n "$NAMESPACE" "$pod" --tail=50 2>/dev/null || echo "  Could not get logs"
        echo ""

        echo "--- Events for $pod ---"
        kubectl describe pod -n "$NAMESPACE" "$pod" | grep -A 20 "Events:" || true
        echo ""
    done

    if [ "$HAS_KUBECTL_AI" = true ]; then
        echo ""
        echo "Step 3: AI Analysis of Issues..."
        echo "----------------------------------------"
        echo ""
        kubectl ai "Analyze why pods $FAILED_PODS in namespace $NAMESPACE are failing and suggest fixes"
    fi
else
    echo "All pods are running successfully!"
fi

echo ""
echo "Step 4: Service Connectivity Check..."
echo "----------------------------------------"
echo ""

kubectl get svc -n "$NAMESPACE"

echo ""
echo "Step 5: Resource Usage..."
echo "----------------------------------------"
echo ""

kubectl top pods -n "$NAMESPACE" 2>/dev/null || echo "  Metrics not available (metrics-server may not be ready)"

echo ""
echo "Step 6: Recent Events..."
echo "----------------------------------------"
echo ""

kubectl get events -n "$NAMESPACE" --sort-by='.lastTimestamp' | tail -20

if [ "$HAS_KUBECTL_AI" = true ]; then
    echo ""
    echo "Step 7: AI Summary and Recommendations..."
    echo "----------------------------------------"
    echo ""
    kubectl ai "Provide a summary of the health status of the $NAMESPACE namespace and any recommendations for improvement"
fi

echo ""
echo "=========================================="
echo "Troubleshooting Complete"
echo "=========================================="
echo ""
echo "Common fixes:"
echo "  - Restart pod: kubectl rollout restart deployment/<name> -n $NAMESPACE"
echo "  - View logs: kubectl logs -n $NAMESPACE -l app=backend -f"
echo "  - Shell into pod: kubectl exec -it <pod-name> -n $NAMESPACE -- /bin/sh"
echo ""
