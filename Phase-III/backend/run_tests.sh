#!/bin/bash
# Test Runner Script
# Runs all tests with coverage reporting

echo "========================================="
echo "Running Chat Endpoint Tests"
echo "========================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install test dependencies if needed
echo "Installing test dependencies..."
pip install -q pytest pytest-asyncio pytest-cov httpx

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v

# Show coverage report
echo ""
echo "Coverage Summary:"
pytest tests/ --cov=app --cov-report=term-missing

echo ""
echo "========================================="
echo "Tests Complete!"
echo "========================================="
echo ""
echo "For detailed HTML coverage report:"
echo "  pytest tests/ --cov=app --cov-report=html"
echo "  Then open: htmlcov/index.html"
