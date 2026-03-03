#!/usr/bin/env python3
"""
Clean up blob storage by removing old content.

This script:
- Lists all blobs in the recorder-content container
- Optionally deletes all content or specific prefixes

Works with both:
- Azure Blob Storage (via AZURE_STORAGE_CONNECTION_STRING env var)
- Local Azurite (default if env var not set)
"""

import os
import sys
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


def list_blobs(container_client):
    """List all blobs in the container."""
    blobs = list(container_client.list_blobs())
    if not blobs:
        print("Container is empty")
        return []
    
    print(f"\nFound {len(blobs)} blobs:")
    for blob in blobs:
        size_kb = blob.size / 1024
        print(f"  - {blob.name} ({size_kb:.1f} KB)")
    return blobs


def delete_all_blobs(container_client):
    """Delete all blobs in the container."""
    blobs = list(container_client.list_blobs())
    
    if not blobs:
        print("✓ Container is already empty")
        return
    
    print(f"\n⚠️  About to delete {len(blobs)} blobs")
    response = input("Continue? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Cancelled")
        return
    
    deleted = 0
    for blob in blobs:
        try:
            container_client.delete_blob(blob.name)
            print(f"✓ Deleted {blob.name}")
            deleted += 1
        except Exception as e:
            print(f"✗ Failed to delete {blob.name}: {e}")
    
    print(f"\n✨ Deleted {deleted}/{len(blobs)} blobs")


def delete_prefix(container_client, prefix):
    """Delete all blobs with a specific prefix."""
    blobs = list(container_client.list_blobs(name_starts_with=prefix))
    
    if not blobs:
        print(f"✓ No blobs found with prefix '{prefix}'")
        return
    
    print(f"\n⚠️  About to delete {len(blobs)} blobs with prefix '{prefix}':")
    for blob in blobs:
        print(f"  - {blob.name}")
    
    response = input("Continue? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Cancelled")
        return
    
    deleted = 0
    for blob in blobs:
        try:
            container_client.delete_blob(blob.name)
            print(f"✓ Deleted {blob.name}")
            deleted += 1
        except Exception as e:
            print(f"✗ Failed to delete {blob.name}: {e}")
    
    print(f"\n✨ Deleted {deleted}/{len(blobs)} blobs")


def main():
    """Clean up storage."""
    # Show which storage we're using
    if IS_AZURE:
        print("🔵 Using Azure Blob Storage")
        print(f"   Container: {CONTAINER_NAME}\n")
    else:
        print("🟡 Using local Azurite storage")
        print(f"   Container: {CONTAINER_NAME}\n")

    try:
        client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = client.get_container_client(CONTAINER_NAME)

        if not container_client.exists():
            print(f"❌ Container '{CONTAINER_NAME}' does not exist")
            sys.exit(1)

        # Show menu
        print("What would you like to do?")
        print("  1. List all blobs")
        print("  2. Delete all blobs")
        print("  3. Delete test data (schedule/*, theme/*, media/*)")
        print("  4. Delete uploads (uploads/*)")
        print("  5. Delete specific prefix")
        print("  0. Exit")
        
        choice = input("\nEnter choice: ")
        
        if choice == "1":
            list_blobs(container_client)
        elif choice == "2":
            list_blobs(container_client)
            delete_all_blobs(container_client)
        elif choice == "3":
            print("\nDeleting test data...")
            for prefix in ["schedule/", "theme/", "media/"]:
                delete_prefix(container_client, prefix)
        elif choice == "4":
            delete_prefix(container_client, "uploads/")
        elif choice == "5":
            prefix = input("Enter prefix to delete: ")
            delete_prefix(container_client, prefix)
        elif choice == "0":
            print("Exiting")
        else:
            print("Invalid choice")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
