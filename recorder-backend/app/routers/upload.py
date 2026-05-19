"""Upload initialisation and recording deletion endpoints."""

import logging

from fastapi import APIRouter, HTTPException, Path

from app.media_types import is_allowed_upload_audio_extension
from app.models import InitUploadRequest, InitUploadResponse
from app.storage import (
    delete_by_prefix,
    generate_upload_sas_url,
    store_metadata,
    StorageError,
)
from app.utils import validate_uuid_v4

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/v1/upload", response_model=InitUploadResponse)
async def init_upload(request: InitUploadRequest):
    """
    Initialize an upload by storing metadata and generating a SAS URL.

    1. Validates the filename and metadata
    2. Stores metadata as JSON in Azure Blob Storage
    3. Returns a SAS URL for the client to upload the audio file directly
    """
    filename = request.filename
    metadata = request.metadata

    if not filename or "." not in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_prefix, file_suffix = filename.rsplit(".", 1)

    if not is_allowed_upload_audio_extension(file_suffix):
        raise HTTPException(
            status_code=400, detail=f"File extension .{file_suffix} not allowed"
        )

    if not validate_uuid_v4(metadata.clientId):
        raise HTTPException(status_code=400, detail="clientId is missing or invalid")

    storage_prefix = f"{metadata.clientId}/"

    if metadata.sessionId:
        if not validate_uuid_v4(metadata.sessionId):
            raise HTTPException(status_code=400, detail="sessionId is invalid")
        storage_prefix += f"{metadata.sessionId}/"

    metadata_blob_name = (
        f"uploads/audio_and_metadata/metadata/{storage_prefix}{file_prefix}.json"
    )

    try:
        metadata_dict = metadata.model_dump(exclude_none=True)
        await store_metadata(metadata_blob_name, metadata_dict)
        logger.info(f"Stored metadata for client {metadata.clientId}")
    except StorageError as e:
        logger.error(f"Error storing metadata: {e}")
        raise HTTPException(status_code=500, detail="Error storing metadata")

    audio_blob_name = f"uploads/audio_and_metadata/{storage_prefix}{filename}"

    try:
        sas_url = await generate_upload_sas_url(
            blob_name=audio_blob_name,
            content_type=metadata.contentType,
            expiry_minutes=6,
        )
        return InitUploadResponse(presignedUrl=sas_url)
    except StorageError as e:
        logger.error(f"Error generating SAS URL: {e}")
        raise HTTPException(status_code=500, detail="Error generating upload URL")


@router.delete("/v1/recordings/{client_id}")
async def delete_by_client_id(client_id: str = Path(..., description="Client UUID")):
    """Delete all recordings for a given client ID."""
    if not validate_uuid_v4(client_id):
        raise HTTPException(status_code=400, detail="Invalid clientId")

    prefix = f"uploads/audio_and_metadata/{client_id}/"
    try:
        await delete_by_prefix(prefix)
        return {"message": f"Deleted all data for client {client_id}"}
    except StorageError as e:
        logger.error(f"Error deleting by client ID: {e}")
        raise HTTPException(status_code=500, detail="Error deleting data")


@router.delete("/v1/recordings/{client_id}/{session_id}")
async def delete_by_session_id(
    client_id: str = Path(..., description="Client UUID"),
    session_id: str = Path(..., description="Session UUID"),
):
    """Delete all recordings for a given session."""
    if not validate_uuid_v4(client_id) or not validate_uuid_v4(session_id):
        raise HTTPException(status_code=400, detail="Invalid clientId or sessionId")

    prefix = f"uploads/audio_and_metadata/{client_id}/{session_id}/"
    try:
        await delete_by_prefix(prefix)
        return {"message": f"Deleted all data for session {session_id}"}
    except StorageError as e:
        logger.error(f"Error deleting by session ID: {e}")
        raise HTTPException(status_code=500, detail="Error deleting data")


@router.delete("/v1/recordings/{client_id}/{session_id}/{recording_id}")
async def delete_by_recording_id(
    client_id: str = Path(..., description="Client UUID"),
    session_id: str = Path(..., description="Session UUID"),
    recording_id: str = Path(..., description="Recording UUID"),
):
    """Delete a specific recording."""
    if not all(validate_uuid_v4(id) for id in [client_id, session_id, recording_id]):
        raise HTTPException(
            status_code=400, detail="Invalid clientId, sessionId, or recordingId"
        )

    prefix = f"uploads/audio_and_metadata/{client_id}/{session_id}/{recording_id}"
    try:
        await delete_by_prefix(prefix)
        return {"message": f"Deleted recording {recording_id}"}
    except StorageError as e:
        logger.error(f"Error deleting recording: {e}")
        raise HTTPException(status_code=500, detail="Error deleting recording")
