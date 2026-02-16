#!/usr/bin/env python3
"""Initialize Azurite storage with test data."""

from azure.storage.blob import BlobServiceClient
import json
import time

# Wait a bit for Azurite to be ready
time.sleep(1)

connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

try:
    client = BlobServiceClient.from_connection_string(connection_string)
    container_client = client.get_container_client("recorder-content")

    # Create container
    if not container_client.exists():
        container_client.create_container()
        print("✓ Created container 'recorder-content'")
    else:
        print("✓ Container 'recorder-content' already exists")

    # Upload test theme
    blob_client = client.get_blob_client(
        container="recorder-content", blob="theme/test-theme.json"
    )
    test_theme = {
        "id": "test-theme",
        "name": "Test Theme",
        "description": "A test theme for local development",
        "primaryColor": "#007bff",
    }
    blob_client.upload_blob(json.dumps(test_theme, indent=2), overwrite=True)
    print("✓ Uploaded theme/test-theme.json")

    # Upload test schedule
    blob_client = client.get_blob_client(
        container="recorder-content", blob="schedule/test-schedule.json"
    )
    test_schedule = {
        "id": "test-schedule",
        "name": "Test Schedule",
        "description": "Test playlist schedule",
        "items": [
            {
                "itemId": "1",
                "kind": "prompt",
                "text": "Please read the following sentence",
            }
        ],
    }
    blob_client.upload_blob(json.dumps(test_schedule, indent=2), overwrite=True)
    print("✓ Uploaded schedule/test-schedule.json")

    print("\n✨ Storage initialized successfully!")
    print("\nYou can now test the API:")
    print("  curl http://localhost:8000/v1/theme")
    print("  curl http://localhost:8000/v1/schedule")
    print("  open http://localhost:8000/docs")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
    exit(1)
