#!/bin/bash
# Phase IV: AI DevOps Tools Installation Script
# Installs kubectl-ai and other AI-assisted Kubernetes tools

set -e

echo "=========================================="
echo "Phase IV: AI DevOps Tools Installation"
echo "=========================================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed."
    echo "Install kubectl first."
    exit 1
fi

echo ""
echo "Step 1: Installing kubectl-ai..."
echo "----------------------------------------"

# Check if kubectl-ai is already installed
if command -v kubectl-ai &> /dev/null; then
    echo "  kubectl-ai is already installed"
    kubectl-ai --version 2>/dev/null || true
else
    # Try to install via krew (kubectl plugin manager)
    if command -v kubectl-krew &> /dev/null || kubectl krew version &> /dev/null 2>&1; then
        echo "  Installing via krew..."
        kubectl krew install ai || echo "  kubectl-ai not available in krew, try manual install"
    else
        echo ""
        echo "  kubectl-ai installation options:"
        echo ""
        echo "  Option 1: Install via Homebrew (macOS/Linux):"
        echo "    brew install sozercan/kubectl-ai/kubectl-ai"
        echo ""
        echo "  Option 2: Install via krew:"
        echo "    kubectl krew install ai"
        echo ""
        echo "  Option 3: Download binary from GitHub:"
        echo "    https://github.com/sozercan/kubectl-ai/releases"
        echo ""
    fi
fi

echo ""
echo "Step 2: Configuring kubectl-ai..."
echo "----------------------------------------"

# Create kubectl-ai config directory
mkdir -p ~/.config/kubectl-ai

# Check for API key
if [ -z "$GEMINI_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "  Note: kubectl-ai requires an API key."
    echo ""
    echo "  For Gemini (recommended - free tier available):"
    echo "    export GEMINI_API_KEY=your-api-key"
    echo ""
    echo "  For OpenAI:"
    echo "    export OPENAI_API_KEY=your-api-key"
    echo ""
else
    echo "  API key found in environment"
fi

echo ""
echo "Step 3: kubectl-ai Usage Examples"
echo "----------------------------------------"
echo ""
echo "  # Generate deployment manifest"
echo "  kubectl ai \"create a deployment for nginx with 3 replicas\""
echo ""
echo "  # Troubleshoot pods"
echo "  kubectl ai \"why is my pod crashing in namespace todo-app\""
echo ""
echo "  # Scale deployment"
echo "  kubectl ai \"scale the backend deployment to 5 replicas\""
echo ""
echo "  # Create service"
echo "  kubectl ai \"expose the backend deployment on port 8000\""
echo ""

echo ""
echo "Step 4: Docker AI (Gordon) Setup"
echo "----------------------------------------"
echo ""
echo "  Docker AI (Gordon) is built into Docker Desktop."
echo ""
echo "  To enable:"
echo "    1. Open Docker Desktop"
echo "    2. Go to Settings > Features in Development"
echo "    3. Enable 'Docker AI'"
echo ""
echo "  Usage:"
echo "    docker ai \"optimize my Dockerfile\""
echo "    docker ai \"why is my container failing\""
echo ""

echo ""
echo "=========================================="
echo "AI DevOps Tools Setup Complete"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Set your API key: export GEMINI_API_KEY=your-key"
echo "  2. Test kubectl-ai: kubectl ai \"list all pods\""
echo "  3. Enable Docker AI in Docker Desktop settings"
echo ""
