#!/bin/bash
# Setup script for local development with Azurite

set -e

echo "Setting up local development environment..."

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start Azurite and API services
echo "Starting Azurite and API services..."
docker-compose up -d

# Wait for Azurite to be ready
echo "Waiting for Azurite to start..."
sleep 5

# Create the container using Azure CLI or Python
echo "Creating blob container 'recorder-content'..."
python3 - <<'EOF'
from azure.storage.blob import BlobServiceClient
import time

# Wait a bit more to ensure Azurite is fully ready
time.sleep(2)

connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

try:
    client = BlobServiceClient.from_connection_string(connection_string)
    container_client = client.get_container_client("recorder-content")
    
    if not container_client.exists():
        container_client.create_container()
        print("✓ Container 'recorder-content' created")
    else:
        print("✓ Container 'recorder-content' already exists")
    
    # Upload test theme file
    blob_client = client.get_blob_client(container="recorder-content", blob="theme/test-theme.json")
    test_theme = {
        "id": "test-theme",
        "name": "Test Theme",
        "description": "A test theme for local development"
    }
    import json
    blob_client.upload_blob(json.dumps(test_theme), overwrite=True)
    print("✓ Uploaded test theme file")
    
    # Upload test configuration file
    blob_client = client.get_blob_client(container="recorder-content", blob="configuration/test-config.json")
    test_config = {
        "id": "test-config",
        "name": "Test Configuration",
        "items": []
    }
    blob_client.upload_blob(json.dumps(test_config), overwrite=True)
    print("✓ Uploaded test configuration file")
    
except Exception as e:
    print(f"Error: {e}")
    exit(1)
EOF

echo ""
echo "✓ Local development environment is ready!"
echo ""
echo "Services running:"
echo "  - Azurite Blob Storage: http://localhost:10000"
echo "  - FastAPI Backend: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
