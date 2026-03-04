# Recorder Backend - FastAPI Version

**Note:** This is the modernized FastAPI version running on Azure.

![Deploy Dev](https://github.com/divvun/Kielipankki-donatespeech-backend/actions/workflows/deploy-dev.yml/badge.svg)
![Tests](https://github.com/divvun/Kielipankki-donatespeech-backend/actions/workflows/test.yml/badge.svg)

## Architecture

- **Framework**: FastAPI (Python 3.11)
- **Storage**: Azure Blob Storage
- **Local Development**: Azurite (Azure Storage Emulator)
- **Deployment**: Azure Container Apps or Azure App Service

## Deployment

### Continuous Deployment

The backend automatically deploys to environments based on branch activity:

- **Development Environment**: Auto-deploys on every push to `main` branch
- **Production Environment**: *(Planned)* Will deploy from tagged releases
  (e.g., `v1.0.0`)

### Current Setup (Dev Only)

Push to `main` branch triggers automatic deployment:

1. Tests run automatically
2. Docker image builds from [Dockerfile](Dockerfile)
3. Image pushes to Azure Container Registry with tags:
   - `dev-<commit-sha>` (specific version)
   - `dev-latest` (rolling latest)
4. Azure Container App updates with new image
5. Deployment completes with zero downtime

**View Deployment Status:**

- GitHub Actions: [Deployment Workflows](../../actions)
- Development URL: Provided by Container App ingress

### GitHub Secrets Required

Configure these in repository Settings → Secrets and variables → Actions:

| Secret | Description | Example |
|--------|-------------|---------|
| `AZURE_CLIENT_ID` | Service principal client ID | `12345678-1234-1234-1234-123456789abc` |
| `AZURE_TENANT_ID` | Azure AD tenant ID | `87654321-4321-4321-4321-cba987654321` |
| `AZURE_SUBSCRIPTION_ID` | Target subscription ID | `abcdef12-3456-7890-abcd-ef1234567890` |
| `DEV_ACR_NAME` | Container registry name | `acrkielipankkirec` |
| `DEV_RESOURCE_GROUP` | Resource group name | `rg-kielipankki-recorder-dev` |
| `DEV_CONTAINER_APP` | Container app name | `ca-recorder-backend-dev` |

### Azure Resources Required

**Development Environment:**
- Resource Group: `rg-kielipankki-recorder-dev`
- Storage Account: With container `recorder-content`
- Container Registry: For Docker images
- Key Vault: For YLE API credentials
- Container Apps Environment: Runtime environment
- Container App: The application instance

**Setup Steps:**
1. Create Azure resources (see deployment guide)
2. Configure service principal with federated credential for `main` branch
3. Add GitHub secrets listed above
4. Push to `main` to trigger first deployment

### Manual Deployment

To deploy manually:
```bash
# Build image
docker build -t <acr-name>.azurecr.io/recorder-backend:dev-manual .

# Login and push
az acr login --name <acr-name>
docker push <acr-name>.azurecr.io/recorder-backend:dev-manual

# Update Container App
az containerapp update \
  --name ca-recorder-backend-dev \
  --resource-group rg-kielipankki-recorder-dev \
  --image <acr-name>.azurecr.io/recorder-backend:dev-manual
```

### Future: Production Deployment

When production is ready:

1. Create production Azure resources (mirroring dev setup)
2. Add production federated credential for tag pattern `v*`
3. Configure production GitHub secrets
4. Create tag to deploy: `git tag v1.0.0 && git push origin v1.0.0`

## Quick Start - Local Development

### Prerequisites

- Podman and Podman Compose (or Docker)
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended for fast package
  management)

### Development Tools

This project uses **uv** as the package manager for Python dependencies:

- **Package Manager**: `uv` (fast, modern Python package manager)
- **Python Binary**: `.venv/bin/python` (virtual environment created by uv)
- **Install Dependencies**: `uv sync`
- **Run Scripts**: `uv run python <script.py>` or activate venv first

To activate the virtual environment:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

Once activated, use Python directly:
```bash
python test_models.py
pytest
```

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
DELETE /v1/recordings/{clientId}
DELETE /v1/recordings/{clientId}/{sessionId}
DELETE /v1/recordings/{clientId}/{sessionId}/{recordingId}
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

## Frontend Integration

### Tauri App

The frontend is built with Tauri, providing a native desktop application
experience.

#### Connecting to Local Backend

During development, the Tauri app connects to `http://localhost:8000`.

```typescript
// Example API configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Fetch schedules
const schedules = await fetch(`${API_BASE_URL}/v1/schedule`).then(r => r.json());

// Fetch theme
const theme = await fetch(`${API_BASE_URL}/v1/theme/${themeId}`).then(r => r.json());
```

### OpenAPI Specification

The OpenAPI specification is available at:

- **Runtime**: `http://localhost:8000/openapi.json`
- **Versioned**: `openapi.json` (checked into this repository)

The versioned file can be used for generating TypeScript types or API clients.

#### Generating/Updating openapi.json

To create or update the versioned `openapi.json` file:

```bash
# Start the backend
./setup-local.sh

# In another terminal, download the OpenAPI spec
curl http://localhost:8000/openapi.json > openapi.json

# Or with proper formatting
curl http://localhost:8000/openapi.json | uv run python -m json.tool > openapi.json
```

This should be done whenever the API changes (new endpoints, modified
request/response models, etc.) to keep the versioned specification in sync with
the implementation.

### Testing Local Connection

```bash
# Terminal 1: Start backend
cd recorder-backend
./setup-local.sh

# Terminal 2: Test from command line
curl http://localhost:8000/v1/schedule
curl http://localhost:8000/v1/theme
```

### Cleaning Up Storage

The `cleanup-storage.py` script helps you remove old content from blob storage
(both local Azurite and Azure remote).

**For local Azurite:**

```bash
.venv/bin/python cleanup-storage.py
```

**For Azure remote storage:**

```bash
export AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
.venv/bin/python cleanup-storage.py
```

**Interactive menu options:**
1. List all blobs - See what's currently stored
2. Delete all blobs - Remove everything (with confirmation)
3. Delete test data - Remove only schedule/*, theme/*, media/* (what
   init-storage.py uploaded)
4. Delete uploads - Remove user-uploaded recordings (uploads/*)
5. Delete specific prefix - Target a specific path

**Common workflow:**

```bash
# 1. List current content
.venv/bin/python cleanup-storage.py
# Choose option 1

# 2. Remove test data to start fresh
.venv/bin/python cleanup-storage.py
# Choose option 3

# 3. Re-initialize with fresh test data
.venv/bin/python init-storage.py
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
- Frontend app needs to update the base URL and schedule endpoint path

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
├── cleanup-storage.py         # Storage cleanup (removes old content)
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
