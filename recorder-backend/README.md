# Recorder backend lambda functions

## REST APIs

### Initialize audio file upload and store related metadata call

```json
POST v1/init-upload 
{
    "filename": "audio.m4a",
    "metadata": {
        "key" : "value"
    }
}

>>>

{
    "presignedUrl" : "https://s3/presigned-upload.com"
}
```

### Delete all uploaded metadata and audio for client with the given id or specific session or recording if those parameters are provided

```json
DELETE v1/upload/[clientID]?session_id=<>&recording_id=<>
>>>

{
    "delete" : "ok"
}
```

### Load single playlist configuration from s3

```json
GET v1/configuration/[ID]

>>>

#Whatever is stored in the configuration file in the s3 bucket configuration/[id].json

    "items": [
        {
            "itemId": "ce3c6012-25f0-4c69-a0ad-c5dc8e41b795",
            "kind": "media",
            "itemType": "audio",
            "typeId": "audio/m4a",
            "url": "arvi-euroviisut.m4a",
            "description": "Arvi Lind esittelee",
            "options": []
        },
        ...
    ]

```

### Load all playlist configurations

```json
GET v1/configuration

>>>

# Returns all the configuration files in s3 with "configuration/" prefix. The data has the file id and content.
    [
        {"id": "27103f9e-2b03-48d0-b442-f38a6052cfe1",
         "content": {
            "items": [
                {
                    "itemId": "ce3c6012-25f0-4c69-a0ad-c5dc8e41b795",
                    "kind": "media",
                    "itemType": "audio",
                    "typeId": "audio/m4a",
                    "url": "arvi-euroviisut.m4a",
                    "description": "Arvi Lind esittelee",
                    "options": []
                },
                ...
            ]
        ...
    ]


```

### Load single theme from s3

```json
GET v1/theme/[ID]

>>>>

#What ever is stored in the theme file in the s3 bucket theme/[id].json
{
    "description": "Koronavirus 2020",
    "image": "https://jdjalassljkdda/something.jpg",
    "scheduleIds": [
        "0b5cf885-5049-4e7a-83e0-05a63be53639",
        "143a9f19-edda-40c5-9213-3c0615c7dcf0"
    ]
}

```

### Load all themes

```json
GET v1/theme/

>>>

# Returns all the theme files in s3 with "theme/" prefix. The data has the file id and content.
    [
        {"id": "27103f9e-2b03-48d0-b442-f38a6052cfe1",
         "content": {
            "items": [
                {
                    "description": "Koronavirus 2020",
                    "image": "https://jdjalassljkdda/something.jpg",
                    "scheduleIds": [
                        "0b5cf885-5049-4e7a-83e0-05a63be53639",
                        "143a9f19-edda-40c5-9213-3c0615c7dcf0"
                    ]
                },
                ...
            ]
        ...
    ]

```

### To test locally setup AWS-credentials and use ipython

```python
%load_ext autoreload
%autoreload 2
import os  
os.environ['CONTENT_BUCKET_NAME'] = 'recorder-test'
os.environ['YLE_CLIENT_ID'] ="XXX"
os.environ['YLE_CLIENT_KEY'] = "XXX"
os.environ['YLE_DECRYPT'] = "XXX"

from handler import *
init_upload({'body': '{"filename":"jee", "metadata": {"kukkuu": "jee"}}'}, {})

```

---

## FastAPI Local Development with Azurite

### Prerequisites

- Python 3.11+
- Podman Desktop (recommended - no sudo required) or Docker
- Azure CLI (optional, for deployment)

### Setup

1. **Start Azurite (Azure Storage Emulator)**:
   
   Using Podman (recommended):
   ```bash
   podman-compose up -d
   ```
   
   Or using Docker:
   ```bash
   docker-compose up -d
   ```

   This starts Azurite and initializes it with test configuration/theme files.

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI application**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   
   Interactive API documentation at `http://localhost:8000/docs`

4. **Test the endpoints**:
   ```bash
   # List all configurations
   curl http://localhost:8000/v1/configuration
   
   # Get specific configuration
   curl http://localhost:8000/v1/configuration/test-config-1
   
   # List all themes
   curl http://localhost:8000/v1/theme
   
   # Initialize upload (requires valid request body)
   curl -X POST http://localhost:8000/v1/init-upload \
     -H "Content-Type: application/json" \
     -d @test/sample-init-upload.json
   ```

### Environment Variables

- `AZURE_STORAGE_CONNECTION_STRING`: Connection string for Azure Storage
  - Default for local: `DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;`
- `AZURE_STORAGE_CONTAINER`: Name of the blob container
  - Default: `recorder-content-dev`

### Stopping Services

Using Podman:
```bash
podman-compose down
```

Or using Docker:
```bash
docker-compose down
```
