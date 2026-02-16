"""
Azure Blob Storage abstraction layer.

This module provides async functions for interacting with Azure Blob Storage,
replacing the boto3 S3 client used in the Lambda version.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import (
    BlobSasPermissions,
    generate_blob_sas,
    ContentSettings,
)
from azure.core.exceptions import ResourceNotFoundError, AzureError

logger = logging.getLogger(__name__)


class StorageError(Exception):
    """Custom exception for storage operations."""

    pass


# --- Configuration ---

STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_NAME", "recorder-content")

# For local development with Azurite
if not STORAGE_CONNECTION_STRING:
    STORAGE_CONNECTION_STRING = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )


def get_blob_service_client() -> BlobServiceClient:
    """Create and return a BlobServiceClient."""
    return BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)


# --- Storage Operations ---


async def store_metadata(blob_name: str, metadata: dict) -> None:
    """
    Store metadata as JSON in Azure Blob Storage.

    Args:
        blob_name: The blob path/name
        metadata: Dictionary to store as JSON

    Raises:
        StorageError: If the operation fails
    """
    try:
        async with get_blob_service_client() as client:
            blob_client = client.get_blob_client(
                container=CONTAINER_NAME, blob=blob_name
            )

            json_data = json.dumps(metadata)

            await blob_client.upload_blob(
                json_data,
                overwrite=True,
                content_settings=ContentSettings(content_type="application/json"),
            )

            logger.info(f"Stored metadata to {blob_name}")
    except AzureError as e:
        logger.error(f"Azure Storage error storing metadata: {e}")
        raise StorageError(f"Failed to store metadata: {e}")
    except Exception as e:
        logger.error(f"Unexpected error storing metadata: {e}")
        raise StorageError(f"Failed to store metadata: {e}")


async def generate_upload_sas_url(
    blob_name: str,
    content_type: Optional[str] = None,
    expiry_minutes: int = 6,
) -> str:
    """
    Generate a SAS URL for uploading a blob.

    Args:
        blob_name: The blob path/name
        content_type: Optional MIME type for the blob
        expiry_minutes: How long the SAS URL should be valid (default 6 minutes)

    Returns:
        A SAS URL that allows PUT operations

    Raises:
        StorageError: If URL generation fails
    """
    try:
        async with get_blob_service_client() as client:
            # Extract account name and key from connection string
            conn_parts = dict(
                item.split("=", 1)
                for item in STORAGE_CONNECTION_STRING.split(";")
                if "=" in item
            )
            account_name = conn_parts.get("AccountName")
            account_key = conn_parts.get("AccountKey")

            if not account_name or not account_key:
                raise StorageError("Invalid connection string format")

            # Generate SAS token
            sas_token = generate_blob_sas(
                account_name=account_name,
                container_name=CONTAINER_NAME,
                blob_name=blob_name,
                account_key=account_key,
                permission=BlobSasPermissions(write=True, create=True),
                expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes),
            )

            # Construct the full URL
            blob_client = client.get_blob_client(
                container=CONTAINER_NAME, blob=blob_name
            )
            sas_url = f"{blob_client.url}?{sas_token}"

            logger.info(f"Generated SAS URL for {blob_name}")
            return sas_url

    except AzureError as e:
        logger.error(f"Azure Storage error generating SAS URL: {e}")
        raise StorageError(f"Failed to generate SAS URL: {e}")
    except Exception as e:
        logger.error(f"Unexpected error generating SAS URL: {e}")
        raise StorageError(f"Failed to generate SAS URL: {e}")


async def delete_by_prefix(prefix: str) -> int:
    """
    Delete all blobs with a given prefix.

    Args:
        prefix: The blob name prefix to match

    Returns:
        Number of blobs deleted

    Raises:
        StorageError: If deletion fails
    """
    try:
        async with get_blob_service_client() as client:
            container_client = client.get_container_client(CONTAINER_NAME)

            deleted_count = 0
            async for blob in container_client.list_blobs(name_starts_with=prefix):
                blob_client = container_client.get_blob_client(blob.name)
                await blob_client.delete_blob()
                deleted_count += 1
                logger.debug(f"Deleted blob: {blob.name}")

            logger.info(f"Deleted {deleted_count} blobs with prefix: {prefix}")
            return deleted_count

    except AzureError as e:
        logger.error(f"Azure Storage error deleting blobs: {e}")
        raise StorageError(f"Failed to delete blobs: {e}")
    except Exception as e:
        logger.error(f"Unexpected error deleting blobs: {e}")
        raise StorageError(f"Failed to delete blobs: {e}")


async def load_blob_json(blob_name: str) -> dict:
    """
    Load a JSON blob from storage.

    Args:
        blob_name: The blob path/name

    Returns:
        Parsed JSON content as a dictionary

    Raises:
        StorageError: If the blob doesn't exist or can't be parsed
    """
    try:
        async with get_blob_service_client() as client:
            blob_client = client.get_blob_client(
                container=CONTAINER_NAME, blob=blob_name
            )

            download_stream = await blob_client.download_blob()
            content = await download_stream.readall()

            return json.loads(content)

    except ResourceNotFoundError:
        logger.error(f"Blob not found: {blob_name}")
        raise StorageError(f"Blob not found: {blob_name}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in blob {blob_name}: {e}")
        raise StorageError(f"Invalid JSON in blob: {e}")
    except AzureError as e:
        logger.error(f"Azure Storage error loading blob: {e}")
        raise StorageError(f"Failed to load blob: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading blob: {e}")
        raise StorageError(f"Failed to load blob: {e}")


async def load_blob_binary(blob_name: str) -> bytes:
    """
    Load binary blob content from storage.

    Args:
        blob_name: The blob path/name

    Returns:
        Binary content

    Raises:
        StorageError: If the blob doesn't exist or can't be loaded
    """
    try:
        async with get_blob_service_client() as client:
            blob_client = client.get_blob_client(
                container=CONTAINER_NAME, blob=blob_name
            )

            download_stream = await blob_client.download_blob()
            content = await download_stream.readall()

            return content

    except ResourceNotFoundError:
        logger.error(f"Blob not found: {blob_name}")
        raise StorageError(f"Blob not found: {blob_name}")
    except AzureError as e:
        logger.error(f"Azure Storage error loading blob: {e}")
        raise StorageError(f"Failed to load blob: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading blob: {e}")
        raise StorageError(f"Failed to load blob: {e}")


async def load_blob_binary_range(
    blob_name: str, offset: int = 0, length: Optional[int] = None
) -> tuple[bytes, int]:
    """
    Load a portion of a binary blob from storage.

    Args:
        blob_name: The blob path/name
        offset: Starting byte offset (default: 0)
        length: Number of bytes to read (default: all remaining bytes)

    Returns:
        Tuple of (content bytes, total blob size)

    Raises:
        StorageError: If the blob doesn't exist or can't be loaded
    """
    try:
        async with get_blob_service_client() as client:
            blob_client = client.get_blob_client(
                container=CONTAINER_NAME, blob=blob_name
            )

            # Get blob properties to know total size
            blob_properties = await blob_client.get_blob_properties()
            total_size = blob_properties.size

            # If no length specified, read to end
            if length is None:
                length = total_size - offset

            # Download the specified range
            download_stream = await blob_client.download_blob(
                offset=offset, length=length
            )
            content = await download_stream.readall()

            return content, total_size

    except ResourceNotFoundError:
        logger.error(f"Blob not found: {blob_name}")
        raise StorageError(f"Blob not found: {blob_name}")
    except AzureError as e:
        logger.error(f"Azure Storage error loading blob: {e}")
        raise StorageError(f"Failed to load blob: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading blob: {e}")
        raise StorageError(f"Failed to load blob: {e}")


async def list_blobs_with_prefix(prefix: str, max_results: int = 1000) -> List[str]:
    """
    List all blob names with a given prefix.

    Args:
        prefix: The blob name prefix to match
        max_results: Maximum number of results to return

    Returns:
        List of blob names

    Raises:
        StorageError: If listing fails
    """
    try:
        async with get_blob_service_client() as client:
            container_client = client.get_container_client(CONTAINER_NAME)

            blob_names = []
            count = 0

            async for blob in container_client.list_blobs(name_starts_with=prefix):
                blob_names.append(blob.name)
                count += 1
                if count >= max_results:
                    break

            logger.info(f"Listed {len(blob_names)} blobs with prefix: {prefix}")
            return blob_names

    except AzureError as e:
        logger.error(f"Azure Storage error listing blobs: {e}")
        raise StorageError(f"Failed to list blobs: {e}")
    except Exception as e:
        logger.error(f"Unexpected error listing blobs: {e}")
        raise StorageError(f"Failed to list blobs: {e}")
