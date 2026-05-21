#!/bin/bash
# Setup script for local development with Azurite

set -e

echo "Setting up local development environment..."

# Check if podman is running
if ! podman info > /dev/null 2>&1; then
    echo "Error: Podman is not running. Please start Podman and try again."
    exit 1
fi

# Start Azurite and API services
echo "Starting Azurite and API services..."
podman-compose -f recorder-backend/docker-compose.yml up -d --build

# Wait for Azurite to be ready
echo "Waiting for Azurite to start..."
sleep 5

# Initialize blob storage with test data
echo "Initializing blob storage..."
if [ ! -x "recorder-tooling/.venv/bin/python" ]; then
    echo "Setting up recorder-tooling virtual environment..."
    if ! command -v uv &> /dev/null; then
        echo "Error: uv is required to bootstrap recorder-tooling/.venv"
        echo "Install uv with: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    (cd recorder-tooling && uv sync)
fi
source recorder-tooling/.venv/bin/activate
recorder-tooling storage init

# Wait for the API to be ready before reporting success
echo "Waiting for FastAPI backend to start..."
max_attempts=30
attempt=1
until curl -fsS http://localhost:8000/openapi.json > /dev/null 2>&1; do
    if [ "$attempt" -ge "$max_attempts" ]; then
        echo "Error: Backend did not become ready at http://localhost:8000"
        echo "Check logs with: podman-compose logs -f api"
        exit 1
    fi
    sleep 1
    attempt=$((attempt + 1))
done

echo ""
echo "✓ Local development environment is ready!"
echo ""
echo "Services running:"
echo "  - Azurite Blob Storage: http://localhost:10000"
echo "  - FastAPI Backend: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "To stop services: cd recorder-backend && podman-compose down"
echo "To view logs: cd recorder-backend && podman-compose logs -f"
