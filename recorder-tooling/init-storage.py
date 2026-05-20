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
import json
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
CONNECTION_STRING = (
    os.environ.get("AZURE_STORAGE_CONNECTION_STRING") or AZURITE_CONNECTION_STRING
)
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

        # Get content directory (now in ../recorder-content/)
        content_dir = Path(__file__).parent.parent / "recorder-content" / CONTENT_ENV

        if not content_dir.exists():
            print(f"❌ Error: Content directory not found: {content_dir}")
            sys.exit(1)

        # Upload schedules (supports both flat id.json and per-language id/lang.json layouts)
        schedules_dir = content_dir / "schedules"
        uploaded_schedule_keys: set[str] = set()
        if schedules_dir.exists():
            schedule_files = list(schedules_dir.rglob("*.json"))
            if schedule_files:
                print(f"\nUploading {len(schedule_files)} schedule files...")
                for schedule_file in schedule_files:
                    relative = schedule_file.relative_to(schedules_dir)
                    blob_name = f"schedule/{relative.as_posix()}"
                    with open(schedule_file, "rb") as f:
                        blob_client = client.get_blob_client(
                            container=CONTAINER_NAME,
                            blob=blob_name,
                        )
                        blob_client.upload_blob(f, overwrite=True)
                    uploaded_schedule_keys.add(blob_name)
                    print(f"✓ Uploaded {blob_name}")
            else:
                print("⚠ Warning: No schedule files found")
        else:
            print(f"⚠ Warning: Schedules directory not found: {schedules_dir}")

        # Upload themes (supports both flat id.json and per-language id/lang.json layouts)
        themes_dir = content_dir / "themes"
        if themes_dir.exists():
            theme_files = list(themes_dir.rglob("*.json"))
            if theme_files:
                print(f"\nUploading {len(theme_files)} theme files...")
                for theme_file in theme_files:
                    relative = theme_file.relative_to(themes_dir)
                    blob_name = f"theme/{relative.as_posix()}"
                    with open(theme_file, "rb") as f:
                        blob_client = client.get_blob_client(
                            container=CONTAINER_NAME,
                            blob=blob_name,
                        )
                        blob_client.upload_blob(f, overwrite=True)
                    print(f"✓ Uploaded {blob_name}")

                # Derive schedule blobs from theme payloads for local content packs
                # where schedule JSON files are embedded under each theme file.
                generated_schedules = 0
                for theme_file in theme_files:
                    relative = theme_file.relative_to(themes_dir)
                    parts = relative.as_posix().split("/")
                    if len(parts) != 2:
                        continue

                    language_filename = parts[1]
                    if not language_filename.endswith(".json"):
                        continue

                    language = language_filename[: -len(".json")]

                    with open(theme_file, "r", encoding="utf-8") as f:
                        theme_payload = json.load(f)

                    schedule_payload = theme_payload.get("schedule")
                    if not isinstance(schedule_payload, dict):
                        continue

                    schedule_id = schedule_payload.get("scheduleId")
                    if not schedule_id:
                        continue

                    schedule_blob_name = f"schedule/{schedule_id}/{language}.json"
                    if schedule_blob_name in uploaded_schedule_keys:
                        continue

                    schedule_blob_client = client.get_blob_client(
                        container=CONTAINER_NAME,
                        blob=schedule_blob_name,
                    )
                    schedule_blob_client.upload_blob(
                        json.dumps(schedule_payload, ensure_ascii=False),
                        overwrite=True,
                    )
                    uploaded_schedule_keys.add(schedule_blob_name)
                    generated_schedules += 1
                    print(f"✓ Generated {schedule_blob_name} from {relative.as_posix()}")

                if generated_schedules > 0:
                    print(
                        f"✓ Generated {generated_schedules} schedule blobs from theme files"
                    )
            else:
                print("⚠ Warning: No theme files found")
        else:
            print(f"⚠ Warning: Themes directory not found: {themes_dir}")

        # Upload media assets used by schedule/theme payloads.
        media_dir = content_dir / "media"
        if media_dir.exists():
            media_files = [f for f in media_dir.rglob("*") if f.is_file()]
            if media_files:
                print(f"\nUploading {len(media_files)} media files...")
                for media_file in media_files:
                    relative = media_file.relative_to(media_dir)
                    blob_name = f"media/{relative.as_posix()}"
                    with open(media_file, "rb") as f:
                        blob_client = client.get_blob_client(
                            container=CONTAINER_NAME,
                            blob=blob_name,
                        )
                        blob_client.upload_blob(f, overwrite=True)
                    print(f"✓ Uploaded {blob_name}")
            else:
                print("⚠ Warning: No media files found")
        else:
            print(f"⚠ Warning: Media directory not found: {media_dir}")

        print("\n✨ Storage initialized successfully!")

        if IS_AZURE:
            print("\n🔵 Azure Blob Storage is now populated with production data.")
            print(
                "   Your Container App should now return data from /v1/theme and /v1/schedule endpoints."
            )
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
