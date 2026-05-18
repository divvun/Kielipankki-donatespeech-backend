"""Media file serving endpoint."""

import json
import logging
import urllib.request
from io import BytesIO

from fastapi import APIRouter, Header, HTTPException, Path
from fastapi.responses import StreamingResponse

from app.storage import load_blob_binary, load_blob_binary_range, StorageError
from app.yle_utils import get_media_url, FileProcessingError

logger = logging.getLogger(__name__)

router = APIRouter()

_CONTENT_TYPES: dict[str, str] = {
    "m4a": "audio/mp4",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "flac": "audio/flac",
    "opus": "audio/opus",
    "amr": "audio/amr",
    "caf": "audio/x-caf",
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mov": "video/quicktime",
}


def _get_yle_media_info(yle_program_id: str) -> dict:
    """Fetch YLE media information for a given program ID."""
    try:
        media_url = get_media_url(yle_program_id)
        with urllib.request.urlopen(media_url, timeout=10) as res:
            return json.loads(res.read())
    except FileProcessingError as e:
        logger.error(f"Error getting YLE media URL: {e}")
        raise HTTPException(status_code=400, detail=f"Error fetching YLE media: {e}")
    except Exception as e:
        logger.error(f"Error fetching YLE media info: {e}")
        raise HTTPException(status_code=500, detail="Error fetching YLE media information")


@router.get("/v1/yle-media/{yle_program_id}")
async def get_yle_media(
    yle_program_id: str = Path(..., description="YLE program ID (e.g., 1-50525858)"),
):
    """
    Fetch media information from YLE API for a YLE program.

    This endpoint is used for YleAudioMediaItem and YleVideoMediaItem types.
    """
    return _get_yle_media_info(yle_program_id)


@router.get("/v1/media/{filename}")
async def serve_media(
    filename: str = Path(..., description="Media filename"),
    range: str = Header(None, description="HTTP Range header"),
):
    """
    Serve media files (audio/video) for playback in the client app.

    Supports HTTP range requests for streaming and seeking.
    Required for AVPlayer on iOS/macOS.

    For YLE media, use the /v1/yle-media/{yle_program_id} endpoint instead.
    """
    if "/" in filename or filename.startswith(".."):
        raise HTTPException(status_code=400, detail="Invalid filename")

    blob_name = f"media/{filename}"
    extension = filename.rsplit(".", 1)[-1].lower()
    content_type = _CONTENT_TYPES.get(extension, "application/octet-stream")

    try:
        if range:
            try:
                range_str = range.replace("bytes=", "")
                if "-" in range_str:
                    start_str, end_str = range_str.split("-", 1)
                    start = int(start_str) if start_str else 0
                    end = int(end_str) if end_str else None
                else:
                    start = int(range_str)
                    end = None

                content, total_size = await load_blob_binary_range(
                    blob_name,
                    offset=start,
                    length=(end - start + 1) if end else None,
                )
                actual_end = start + len(content) - 1

                return StreamingResponse(
                    BytesIO(content),
                    status_code=206,
                    media_type=content_type,
                    headers={
                        "Content-Length": str(len(content)),
                        "Content-Range": f"bytes {start}-{actual_end}/{total_size}",
                        "Accept-Ranges": "bytes",
                        "Content-Disposition": f"inline; filename={filename}",
                    },
                )
            except (ValueError, AttributeError):
                pass  # Fall through to full-file response.

        content = await load_blob_binary(blob_name)
        return StreamingResponse(
            BytesIO(content),
            media_type=content_type,
            headers={
                "Content-Length": str(len(content)),
                "Accept-Ranges": "bytes",
                "Content-Disposition": f"inline; filename={filename}",
            },
        )

    except StorageError:
        raise HTTPException(status_code=404, detail="Media file not found")
    except Exception as e:
        logger.error(f"Error serving media {filename}: {e}")
        raise HTTPException(status_code=500, detail="Error serving media file")
