"""Initialize blob storage with content files."""

from __future__ import annotations

import os
import time
from pathlib import Path

from azure.storage.blob import BlobServiceClient

AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONNECTION_STRING = (
    os.environ.get("AZURE_STORAGE_CONNECTION_STRING") or AZURITE_CONNECTION_STRING
)
CONTAINER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_NAME") or "recorder-content"
IS_AZURE = bool(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))
CONTENT_ENV = "prod" if IS_AZURE else "dev"


def init_storage_main(content_dir: Path) -> int:
    """Initialize storage with content files."""
    target = "prod" if IS_AZURE else "dev"
    if IS_AZURE:
        print("🔵 Using Azure Blob Storage (Production)")
        print(f"   Container: {CONTAINER_NAME}")
        print(f"   Source: {content_dir}/{target}/\n")
    else:
        print("🟡 Using local Azurite storage (Development)")
        print(f"   Container: {CONTAINER_NAME}")
        print(f"   Source: {content_dir}/{target}/\n")
        time.sleep(2)

    try:
        client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = client.get_container_client(CONTAINER_NAME)

        if not container_client.exists():
            container_client.create_container()
            print(f"✓ Created container '{CONTAINER_NAME}'")
        else:
            print(f"✓ Container '{CONTAINER_NAME}' already exists")

        if not content_dir.exists():
            print(f"❌ Error: Content directory not found: {content_dir}")
            return 1

        themes_dir = content_dir / target / "themes"
        if themes_dir.exists():
            theme_files = list(themes_dir.rglob("*.json"))
            if theme_files:
                print(f"\nUploading {len(theme_files)} theme files...")
                for theme_file in theme_files:
                    relative = theme_file.relative_to(themes_dir)
                    blob_name = f"theme/{relative.as_posix()}"
                    with open(theme_file, "rb") as file_obj:
                        blob_client = client.get_blob_client(
                            container=CONTAINER_NAME,
                            blob=blob_name,
                        )
                        blob_client.upload_blob(file_obj, overwrite=True)
                    print(f"✓ Uploaded {blob_name}")

            else:
                print("⚠ Warning: No theme files found")
        else:
            print(f"⚠ Warning: Themes directory not found: {themes_dir}")

        media_dir = content_dir / target / "media"
        if media_dir.exists():
            media_files = [f for f in media_dir.rglob("*") if f.is_file()]
            if media_files:
                print(f"\nUploading {len(media_files)} media files...")
                for media_file in media_files:
                    relative = media_file.relative_to(media_dir)
                    blob_name = f"media/{relative.as_posix()}"
                    with open(media_file, "rb") as file_obj:
                        blob_client = client.get_blob_client(
                            container=CONTAINER_NAME,
                            blob=blob_name,
                        )
                        blob_client.upload_blob(file_obj, overwrite=True)
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
    except Exception as exc:
        print(f"❌ Error: {exc}")
        import traceback

        traceback.print_exc()
        return 1

    return 0
