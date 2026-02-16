#!/usr/bin/env python3
"""
Initialize Azurite blob storage with test data.

This script:
- Creates the recorder-content container
- Uploads test files from the test/ directory
"""

import sys
import time
from pathlib import Path

from azure.storage.blob import BlobServiceClient

# Azurite connection string (standard development credentials)
CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONTAINER_NAME = "recorder-content"


def main():
    """Initialize storage with test data."""
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

        # Upload test playlist (schedule) file
        test_dir = Path(__file__).parent / "test"
        playlist_file = test_dir / "0b5cf885-5049-4e7a-83e0-05a63be53639.json"

        if playlist_file.exists():
            print("Uploading test playlist...")
            with open(playlist_file, "rb") as f:
                blob_client = client.get_blob_client(
                    container=CONTAINER_NAME,
                    blob="schedule/0b5cf885-5049-4e7a-83e0-05a63be53639.json",
                )
                blob_client.upload_blob(f, overwrite=True)
            print("✓ Uploaded schedule/0b5cf885-5049-4e7a-83e0-05a63be53639.json")
        else:
            print(f"⚠ Warning: {playlist_file} not found, skipping")

        # Upload test theme file
        theme_file = test_dir / "8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9.json"

        if theme_file.exists():
            print("Uploading test theme...")
            with open(theme_file, "rb") as f:
                blob_client = client.get_blob_client(
                    container=CONTAINER_NAME,
                    blob="theme/8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9.json",
                )
                blob_client.upload_blob(f, overwrite=True)
            print("✓ Uploaded theme/8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9.json")
        else:
            print(f"⚠ Warning: {theme_file} not found, skipping")

        # Upload media files referenced by the schedule
        print("Uploading media files...")
        media_files = [
            "arvi-euroviisut.m4a",
            "lordi-euroviisut.mp4",
        ]

        for media_file in media_files:
            file_path = test_dir / media_file
            if file_path.exists():
                with open(file_path, "rb") as f:
                    blob_client = client.get_blob_client(
                        container=CONTAINER_NAME,
                        blob=f"media/{media_file}",
                    )
                    blob_client.upload_blob(f, overwrite=True)
                print(f"✓ Uploaded media/{media_file}")
            else:
                print(f"⚠ Warning: {file_path} not found, skipping")

        print("\n✨ Storage initialized successfully!")
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
