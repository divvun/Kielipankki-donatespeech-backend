#!/usr/bin/env python3
"""
Initialize blob storage with content files.

This script:
- Creates the recorder-content container
- Uploads content/dev/ files to local Azurite storage
- Uploads content/prod/ files to Azure remote storage

Works with both:
- Azure Blob Storage (via AZURE_STORAGE_CONNECTION_STRING env var)
- Local Azurite (default if env var not set)
"""

import os
import sys
import time
from pathlib import Path

from azure.storage.blob import BlobServiceClient

# Azurite connection string (standard development credentials) - used as fallback
AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

# Use Azure Storage if env var is set, otherwise use local Azurite
CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING") or AZURITE_CONNECTION_STRING
CONTAINER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_NAME") or "recorder-content"

# Determine if we're using Azure or Azurite
IS_AZURE = bool(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))

# Select content directory based on target storage
CONTENT_ENV = "prod" if IS_AZURE else "dev"


def main():
    """Initialize storage with content files."""
    # Show which storage we're using
    if IS_AZURE:
        print("🔵 Using Azure Blob Storage (Production)")
        print(f"   Container: {CONTAINER_NAME}")
        print("   Source: content/prod/\n")
    else:
        print("🟡 Using local Azurite storage (Development)")
        print(f"   Container: {CONTAINER_NAME}")
        print("   Source: content/dev/\n")
        # Wait briefly for Azurite to be ready
        time.sleep(2)

    try:
        client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = client.get_container_client(CONTAINER_NAME)

        # Create container
        if not container_client.exists():
            container_client.create_container()
            print(f"✓ Created container '{CONTAINER_NAME}'")
        else:
            print(f"✓ Container '{CONTAINER_NAME}' already exists")

        # Get content directory
        content_dir = Path(__file__).parent / "content" / CONTENT_ENV
        
        if not content_dir.exists():
            print(f"❌ Error: Content directory not found: {content_dir}")
            sys.exit(1)

        # Upload schedules
        schedules_dir = content_dir / "schedules"
        if schedules_dir.exists():
            schedule_files = list(schedules_dir.glob("*.json"))
            if schedule_files:
                print(f"\nUploading {len(schedule_files)} schedule files...")
                for schedule_file in schedule_files:
                    with open(schedule_file, "rb") as f:
                        blob_client = client.get_blob_client(
                            container=CONTAINER_NAME,
                            blob=f"schedule/{schedule_file.name}",
                        )
                        blob_client.upload_blob(f, overwrite=True)
                    print(f"✓ Uploaded schedule/{schedule_file.name}")
            else:
                print("⚠ Warning: No schedule files found")
        else:
            print(f"⚠ Warning: Schedules directory not found: {schedules_dir}")

        # Upload themes
        themes_dir = content_dir / "themes"
        if themes_dir.exists():
            theme_files = list(themes_dir.glob("*.json"))
            if theme_files:
                print(f"\nUploading {len(theme_files)} theme files...")
                for theme_file in theme_files:
                    with open(theme_file, "rb") as f:
                        blob_client = client.get_blob_client(
                            container=CONTAINER_NAME,
                            blob=f"theme/{theme_file.name}",
                        )
                        blob_client.upload_blob(f, overwrite=True)
                    print(f"✓ Uploaded theme/{theme_file.name}")
            else:
                print("⚠ Warning: No theme files found")
        else:
            print(f"⚠ Warning: Themes directory not found: {themes_dir}")

        print("\n✨ Storage initialized successfully!")
        
        if IS_AZURE:
            print("\n🔵 Azure Blob Storage is now populated with production data.")
            print("   Your Container App should now return data from /v1/theme and /v1/schedule endpoints.")
        else:
            print("\n🟡 Local Azurite storage is now populated with development data.")
            print("\nYou can now test the API:")
            print("  curl http://localhost:8000/v1/theme")
            print("  curl http://localhost:8000/v1/schedule")
            print("  open http://localhost:8000/docs")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
