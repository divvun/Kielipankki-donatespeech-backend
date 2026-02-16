# Recorder Backend - FastAPI Version

**Note:** This is the modernized FastAPI version running on Azure.

## Architecture

- **Framework**: FastAPI (Python 3.11)
- **Storage**: Azure Blob Storage
- **Local Development**: Azurite (Azure Storage Emulator)
- **Deployment**: Azure Container Apps or Azure App Service

## Quick Start - Local Development

### Prerequisites

- Podman and Podman Compose (or Docker)
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended for fast package
  management)

### Setup

#### Start local environment with Azurite

```bash
./setup-local.sh
```

This will:

- Start Azurite (Azure Storage emulator)
- Start the FastAPI backend
- Create the `recorder-content` container
- Upload test theme and schedule files from `test/` directory

#### Access the services

- FastAPI Backend: <http://localhost:8000>
- API Documentation: <http://localhost:8000/docs> (Swagger UI)
- Azurite Blob Storage: <http://localhost:10000>

#### Stop services

```bash
podman-compose down
```

### Manual Setup (without Docker)

#### Install dependencies

```bash
# Using uv (recommended - much faster)
uv sync
source .venv/bin/activate  # On macOS/Linux
```

#### Run Azurite separately (using npm or Podman)

```bash
# Using npm
npm install -g azurite
azurite --silent --location ./azurite-data

# Or using Podman
podman run -p 10000:10000 mcr.microsoft.com/azure-storage/azurite azurite-blob --blobHost 0.0.0.0
```

#### Run the FastAPI app

```bash
uvicorn main:app --reload --port 8000
```

## REST API Endpoints

### Initialize Audio File Upload

Store metadata and get a SAS URL for direct blob upload.

```http
POST /v1/upload
Content-Type: application/json

{
    "filename": "audio.m4a",
    "metadata": {
        "clientId": "550e8400-e29b-41d4-a716-446655440000",
        "sessionId": "optional-session-uuid",
        "contentType": "audio/m4a",
        "timestamp": "2024-01-15T10:30:00Z",
        "duration": 45.2,
        "language": "fi"
    }
}
```

Response:

```json
{
    "presignedUrl": "https://devstoreaccount1.blob.core.windows.net/recorder-content/uploads/audio_and_metadata/550e8400.../audio.m4a?sp=cw&..."
}
```

### Delete Uploaded Data

Delete by client ID, session ID, or recording ID.

```http
DELETE /v1/upload/{clientId}
DELETE /v1/upload/{clientId}/{sessionId}
DELETE /v1/upload/{clientId}/{sessionId}/{recordingId}
```

Response:

```json
{
    "message": "Deleted all data for client {clientId}"
}
```

### Load Schedule Files

Get a single schedule or list all schedules.

```http
GET /v1/schedule/{scheduleId}
GET /v1/schedule
```

### Load Theme Files

Get a single theme or list all themes.

```http
GET /v1/theme/{themeId}
GET /v1/theme
```

## Azure Deployment

### Option 1: Azure Container Apps (Recommended)

Azure Container Apps provides automatic scaling, built-in HTTPS, and easy
deployment.

#### Create Azure Storage Account

```bash
az storage account create \
  --name recorderstorage \
  --resource-group recorder-rg \
  --location northeurope \
  --sku Standard_LRS

az storage container create \
  --name recorder-content \
  --account-name recorderstorage
```

#### Build and push container

```bash
# Build
podman build -t recorder-backend:latest .

# Tag and push to Azure Container Registry
az acr login --name yourregistry
podman tag recorder-backend:latest yourregistry.azurecr.io/recorder-backend:latest
podman push yourregistry.azurecr.io/recorder-backend:latest
```

#### Deploy to Container Apps

```bash
az containerapp create \
  --name recorder-api \
  --resource-group recorder-rg \
  --environment recorder-env \
  --image yourregistry.azurecr.io/recorder-backend:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    AZURE_STORAGE_CONNECTION_STRING="<connection-string>" \
    AZURE_STORAGE_CONTAINER_NAME="recorder-content"
```

### Option 2: Azure App Service

Simpler option for basic workloads.

```bash
az webapp create \
  --name recorder-api \
  --resource-group recorder-rg \
  --plan recorder-plan \
  --deployment-container-image-name yourregistry.azurecr.io/recorder-backend:latest

az webapp config appsettings set \
  --name recorder-api \
  --resource-group recorder-rg \
  --settings \
    AZURE_STORAGE_CONNECTION_STRING="<connection-string>" \
    AZURE_STORAGE_CONTAINER_NAME="recorder-content"
```

## Environment Variables

- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string (required
  in production)
- `AZURE_STORAGE_CONTAINER_NAME`: Container name (default: `recorder-content`)

For local development, these default to Azurite values.

## Testing

```bash
# Run with Podman Compose
podman-compose up

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/v1/theme
curl http://localhost:8000/v1/schedule
```

## Migration from Lambda

This FastAPI version maintains API compatibility with the Lambda version:

- Same request/response format for upload endpoints
- Same validation logic
- Same YLE API integration

**Endpoint changes:**

- `/v1/configuration` → `/v1/schedule` (semantic rename for clarity)
- Mobile apps need to update the base URL and schedule endpoint path

**Key differences:**

- Uses Azure Blob Storage SAS URLs instead of S3 presigned URLs
- Async operations for better performance
- Direct HTTP server instead of API Gateway + Lambda
- Simpler local development with Azurite
- `/v1/configuration` renamed to `/v1/schedule` for semantic clarity

## File Structure

```text
recorder-backend/
├── main.py                     # FastAPI application
├── storage.py                  # Azure Blob Storage abstraction
├── yle_utils.py               # YLE API integration (unchanged)
├── pyproject.toml             # Python project config (uv-managed)
├── requirements-fastapi.txt    # Legacy pip requirements (for backwards compat)
├── .python-version            # Python version specification
├── Dockerfile                  # Container image definition (uses uv)
├── docker-compose.yml          # Local dev environment
├── setup-local.sh             # Setup script for local dev (orchestration)
├── init-storage.py            # Storage initialization (uploads test data)
├── convert_schedule.py        # Convert old format JSON to new format
├── test/                      # Test data files (playlist.json, theme.json)
└── custom_fleep/              # File type detection (unchanged)
```

## Troubleshooting

### Azurite connection issues

If the API can't connect to Azurite, check:

- Azurite is running: `podman ps | grep azurite`
- Connection string is correct
- Container name is `recorder-content`

### SAS URL not working

- Ensure the blob container has appropriate CORS settings
- Check SAS token permissions and expiry time
- Verify clock sync (important for token validation)

### Import errors for Crypto module

This should no longer occur in the FastAPI version, but if you encounter it:

- Ensure `pycryptodome>=3.19.0` is installed
- The Crypto module is only used by `yle_utils.py` for YLE API

## License

See LICENSE file in the repository root.
