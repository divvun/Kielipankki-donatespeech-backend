"""
FastAPI backend for the Kielipankki speech donation recorder.

This replaces the AWS Lambda + API Gateway architecture with a simpler
FastAPI REST API that can run locally (with Azurite) or on Azure.
"""

import logging
from uuid import UUID

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware

from models import (
    Schedule,
    Theme,
    ScheduleListItem,
    ThemeListItem,
    YleAudioMediaItem,
    YleVideoMediaItem,
    InitUploadRequest,
    InitUploadResponse,
)
from storage import (
    store_metadata,
    generate_upload_sas_url,
    delete_by_prefix,
    load_blob_json,
    list_blobs_with_prefix,
    StorageError,
)
from yle_utils import map_yle_content

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Kielipankki Recorder Backend",
    description="Speech donation recorder backend with Azure Blob Storage",
    version="2.0.0",
)

# CORS middleware - allows all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Utility Functions ---


def validate_uuid_v4(uuid_string: str) -> bool:
    """Validate that a string is a valid UUID v4."""
    try:
        UUID(uuid_string, version=4)
        return True
    except (ValueError, AttributeError):
        return False


def pre_process_schedule(schedule: Schedule) -> Schedule:
    """Pre-process schedule by mapping YLE content URLs."""
    for item in schedule.items:
        # Use pattern matching to handle YLE items
        match item:
            case YleAudioMediaItem() | YleVideoMediaItem():
                item.url = map_yle_content(item.url)
    return schedule


# --- API Endpoints ---


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "kielipankki-recorder-backend"}


@app.post("/v1/upload", response_model=InitUploadResponse)
async def init_upload(request: InitUploadRequest):
    """
    Initialize an upload by storing metadata and generating a SAS URL.

    This endpoint:
    1. Validates the filename and metadata
    2. Stores metadata as JSON in Azure Blob Storage
    3. Returns a SAS URL for the client to upload the audio file directly
    """
    filename = request.filename
    metadata = request.metadata

    # Validate filename
    if not filename or "." not in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_prefix, file_suffix = filename.rsplit(".", 1)
    allowed_extensions = {"m4a", "flac", "amr", "wav", "opus", "caf"}

    if file_suffix.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail=f"File extension .{file_suffix} not allowed"
        )

    # Validate clientId
    if not validate_uuid_v4(metadata.clientId):
        raise HTTPException(status_code=400, detail="clientId is missing or invalid")

    # Build storage path
    storage_prefix = f"{metadata.clientId}/"

    # Validate sessionId if present
    if metadata.sessionId:
        if not validate_uuid_v4(metadata.sessionId):
            raise HTTPException(status_code=400, detail="sessionId is invalid")
        storage_prefix += f"{metadata.sessionId}/"

    # Store metadata
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

    # Generate SAS URL for upload (6 minutes = 360 seconds)
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


@app.delete("/v1/upload/{client_id}")
async def delete_by_client_id(client_id: str = Path(..., description="Client UUID")):
    """Delete all uploads for a given client ID."""
    if not validate_uuid_v4(client_id):
        raise HTTPException(status_code=400, detail="Invalid clientId")

    prefix = f"uploads/audio_and_metadata/{client_id}/"
    try:
        await delete_by_prefix(prefix)
        return {"message": f"Deleted all data for client {client_id}"}
    except StorageError as e:
        logger.error(f"Error deleting by client ID: {e}")
        raise HTTPException(status_code=500, detail="Error deleting data")


@app.delete("/v1/upload/{client_id}/{session_id}")
async def delete_by_session_id(
    client_id: str = Path(..., description="Client UUID"),
    session_id: str = Path(..., description="Session UUID"),
):
    """Delete all uploads for a given session."""
    if not validate_uuid_v4(client_id) or not validate_uuid_v4(session_id):
        raise HTTPException(status_code=400, detail="Invalid clientId or sessionId")

    prefix = f"uploads/audio_and_metadata/{client_id}/{session_id}/"
    try:
        await delete_by_prefix(prefix)
        return {"message": f"Deleted all data for session {session_id}"}
    except StorageError as e:
        logger.error(f"Error deleting by session ID: {e}")
        raise HTTPException(status_code=500, detail="Error deleting data")


@app.delete("/v1/upload/{client_id}/{session_id}/{recording_id}")
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


@app.get("/v1/schedule/{schedule_id}", response_model=Schedule)
async def load_schedule(schedule_id: str = Path(..., description="Schedule ID")):
    """Load a specific schedule file."""
    blob_name = f"schedule/{schedule_id}.json"

    try:
        schedule_dict = await load_blob_json(blob_name)
        # Parse and validate using the Schedule model
        schedule = Schedule(**schedule_dict)
        schedule.id = schedule_id
        # Pre-process YLE URLs
        schedule = pre_process_schedule(schedule)
        return schedule
    except StorageError as e:
        logger.error(f"Error loading schedule {schedule_id}: {e}")
        raise HTTPException(status_code=404, detail="Schedule not found")


@app.get("/v1/schedule", response_model=list[ScheduleListItem])
async def load_all_schedules():
    """Load all schedule files."""
    try:
        blob_list = await list_blobs_with_prefix("schedule/")

        schedules = []
        for blob_name in blob_list:
            # Skip the directory marker
            filename = blob_name.replace("schedule/", "")
            if not filename:
                continue

            schedule_dict = await load_blob_json(blob_name)
            # Parse and validate using the Schedule model
            schedule = Schedule(**schedule_dict)
            schedule_id = filename.replace(".json", "").strip()
            schedule.id = schedule_id
            # Pre-process YLE URLs
            schedule = pre_process_schedule(schedule)

            schedules.append(
                ScheduleListItem(
                    id=schedule_id,
                    content=schedule,
                )
            )

        return schedules
    except StorageError as e:
        logger.error(f"Error loading all schedules: {e}")
        raise HTTPException(status_code=500, detail="Error loading schedules")


@app.get("/v1/theme/{theme_id}", response_model=Theme)
async def load_theme(theme_id: str = Path(..., description="Theme ID")):
    """Load a specific theme file."""
    blob_name = f"theme/{theme_id}.json"

    try:
        theme_dict = await load_blob_json(blob_name)
        # Parse and validate using the Theme model
        theme = Theme(**theme_dict)
        theme.id = theme_id
        return theme
    except StorageError as e:
        logger.error(f"Error loading theme {theme_id}: {e}")
        raise HTTPException(status_code=404, detail="Theme not found")


@app.get("/v1/theme", response_model=list[ThemeListItem])
async def load_all_themes():
    """Load all theme files."""
    try:
        blob_list = await list_blobs_with_prefix("theme/")

        themes = []
        for blob_name in blob_list:
            # Skip the directory marker
            filename = blob_name.replace("theme/", "")
            if not filename:
                continue

            theme_dict = await load_blob_json(blob_name)
            # Parse and validate using the Theme model
            theme = Theme(**theme_dict)
            theme_id = filename.replace(".json", "").strip()
            theme.id = theme_id

            themes.append(
                ThemeListItem(
                    id=theme_id,
                    content=theme,
                )
            )

        return themes
    except StorageError as e:
        logger.error(f"Error loading all themes: {e}")
        raise HTTPException(status_code=500, detail="Error loading themes")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
