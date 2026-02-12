#!/bin/bash
# Test runner script for the Recorder Backend API
# Activates virtual environment and runs pytest with coverage

set -e

echo "🧪 Running Recorder Backend API Tests..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run pytest with coverage
pytest tests/ \
    --verbose \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-config=.coveragerc

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report generated in htmlcov/index.html"
