#!/bin/bash
# Setup script for local development with Azurite

set -e

echo "Setting up local development environment..."

# Check if podman is running
if ! podman info > /dev/null 2>&1; then
    echo "Error: Podman is not running. Please start Podman and try again."
    exit 1
fi

# Check if uv is installed (optional but recommended)
if command -v uv &> /dev/null; then
    echo "✓ uv is installed"
else
    echo "Note: uv is not installed. Consider installing it for faster package management:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# Start Azurite and API services
echo "Starting Azurite and API services..."
podman-compose up -d

# Wait for Azurite to be ready
echo "Waiting for Azurite to start..."
sleep 5

# Create the container using Azure CLI or Python
echo "Creating blob container 'recorder-content'..."
source .venv/bin/activate
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
    
    # Upload test playlist (schedule) file
    print("Uploading test playlist...")
    with open("test/playlist.json", "rb") as f:
        playlist_data = f.read()
    blob_client = client.get_blob_client(container="recorder-content", blob="schedule/test-playlist.json")
    blob_client.upload_blob(playlist_data, overwrite=True)
    print("✓ Uploaded test playlist file")
    
    # Upload test theme file
    print("Uploading test theme...")
    with open("test/theme.json", "rb") as f:
        theme_data = f.read()
    blob_client = client.get_blob_client(container="recorder-content", blob="theme/test-theme.json")
    blob_client.upload_blob(theme_data, overwrite=True)
    print("✓ Uploaded test theme file")
    
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
echo "To stop services: podman-compose down"
echo "To view logs: podman-compose logs -f"
