#!/bin/bash
# Generate OpenAPI specification from running backend

set -e

echo "Generating OpenAPI specification..."

# Wait for backend OpenAPI endpoint to become available
max_attempts=15
attempt=1
until curl -fsS http://localhost:8000/openapi.json > /dev/null 2>&1; do
    if [ "$attempt" -ge "$max_attempts" ]; then
        echo "Error: Backend is not running at http://localhost:8000"
        echo "Please start it first with: ./setup-local.sh"
        exit 1
    fi
    sleep 1
    attempt=$((attempt + 1))
done

# Fetch OpenAPI spec and save to recorder-backend/
curl http://localhost:8000/openapi.json | uv run python -m json.tool > recorder-backend/openapi.json

echo "✓ Generated recorder-backend/openapi.json ($(wc -c < recorder-backend/openapi.json | tr -d ' ') bytes)"
