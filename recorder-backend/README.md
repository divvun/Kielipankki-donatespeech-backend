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

## MAUI App Integration

### Connecting to Local Backend

The MAUI app can communicate with the local FastAPI backend during development.
Use platform-specific base URLs:

| Platform | Base URL | Notes |
|----------|----------|-------|
| macOS (native) | `http://localhost:8000` | Direct access to Mac's localhost |
| iOS Simulator | `http://localhost:8000` | Simulator shares Mac's network |
| Android Emulator | `http://10.0.2.2:8000` | Special IP mapping to host's localhost |
| Physical Devices | `http://<your-mac-ip>:8000` | Use Mac's LAN IP (e.g., 192.168.1.100) |

**Example platform detection in MAUI:**

```csharp
public static string GetBaseUrl()
{
    #if ANDROID
        return DeviceInfo.DeviceType == DeviceType.Virtual 
            ? "http://10.0.2.2:8000"  // Emulator
            : "http://192.168.1.100:8000";  // Physical device
    #elif IOS
        return "http://localhost:8000";
    #elif MACCATALYST
        return "http://localhost:8000";
    #else
        return "http://localhost:8000";
    #endif
}
```

### Generating C# API Client

The backend provides an OpenAPI specification that can be used to generate a
type-safe C# client for MAUI.

#### Option 1: NSwag (Recommended)

**In your MAUI project, create `nswag.json`:**

```json
{
  "runtime": "Net80",
  "defaultVariables": null,
  "documentGenerator": {
    "fromDocument": {
      "url": "http://localhost:8000/openapi.json",
      "output": null
    }
  },
  "codeGenerators": {
    "openApiToCSharpClient": {
      "className": "RecorderApiClient",
      "namespace": "KielipankkiRecorder.Api",
      "generateClientInterfaces": true,
      "generateExceptionClasses": true,
      "exceptionClass": "RecorderApiException",
      "wrapResponses": false,
      "generateResponseClasses": false,
      "useBaseUrl": true,
      "httpClientType": "System.Net.Http.HttpClient",
      "output": "Generated/RecorderApiClient.cs"
    }
  }
}
```

**Generate the client:**

```bash
# Install NSwag CLI (one-time)
dotnet tool install -g NSwag.ConsoleCore

# Start the backend
cd recorder-backend
./setup-local.sh

# Generate C# client (run from MAUI project root)
nswag run nswag.json
```

**Add to MAUI project:**

```xml
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
</ItemGroup>
```

#### Option 2: Kiota (Microsoft's Modern Tool)

```bash
# Install Kiota (one-time)
dotnet tool install -g Microsoft.OpenApi.Kiota

# Generate C# client
kiota generate \
  -l CSharp \
  -c RecorderApiClient \
  -n KielipankkiRecorder.Api \
  -d http://localhost:8000/openapi.json \
  -o ./Generated
```

**Add to MAUI project:**

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Kiota.Abstractions" Version="1.7.0" />
  <PackageReference Include="Microsoft.Kiota.Http.HttpClientLibrary" Version="1.3.0" />
  <PackageReference Include="Microsoft.Kiota.Serialization.Json" Version="1.1.0" />
</ItemGroup>
```

### Using the Generated Client

```csharp
// Configure the client
var httpClient = new HttpClient
{
    BaseAddress = new Uri(GetBaseUrl())
};
var client = new RecorderApiClient(httpClient);

// Load schedules
var schedules = await client.Schedule.GetAsync();

// Load specific theme
var theme = await client.Theme["test-theme"].GetAsync();

// Initialize upload
var uploadRequest = new InitUploadRequest
{
    Filename = "recording.m4a",
    Metadata = new UploadMetadata
    {
        ClientId = Guid.NewGuid().ToString(),
        SessionId = sessionId,
        ContentType = "audio/m4a",
        Timestamp = DateTime.UtcNow.ToString("o"),
        Duration = 45.2,
        Language = "fi"
    }
};

var response = await client.Upload.PostAsync(uploadRequest);
var sasUrl = response.PresignedUrl;

// Upload audio file directly to blob storage using SAS URL
using var audioStream = File.OpenRead(audioFilePath);
var uploadClient = new HttpClient();
await uploadClient.PutAsync(sasUrl, new StreamContent(audioStream));
```

### OpenAPI Specification

The OpenAPI specification is available at:
- **Runtime**: `http://localhost:8000/openapi.json`
- **Versioned**: `openapi.json` (checked into this repository)

The versioned file can be used for offline client generation during CI/CD
builds.

### Testing Local Connection

```bash
# Terminal 1: Start backend
cd recorder-backend
./setup-local.sh

# Terminal 2: Test from command line
curl http://localhost:8000/v1/schedule
curl http://localhost:8000/v1/theme

# For Android emulator testing
curl http://10.0.2.2:8000/v1/schedule
```

### Troubleshooting MAUI Connection

**"Connection refused" on Android emulator:**
- Use `http://10.0.2.2:8000` instead of `localhost`
- Ensure backend is running: `podman ps | grep recorder-api`
- Check backend logs: `podman logs recorder-api`

**"Connection refused" on physical device:**
- Ensure Mac and device are on same WiFi network
- Use Mac's LAN IP address (find with `ifconfig en0 | grep inet`)
- Ensure Mac's firewall allows incoming connections on port 8000

**SSL/TLS errors:**
- Local development uses HTTP (not HTTPS)
- For iOS/Android, you may need to configure `NSAppTransportSecurity` (iOS) or
  `android:usesCleartextTraffic="true"` (Android) to allow HTTP in development

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
