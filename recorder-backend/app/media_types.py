"""Shared media MIME type helpers."""

CONTENT_TYPES_BY_EXTENSION: dict[str, str] = {
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
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "svg": "image/svg+xml",
    "bmp": "image/bmp",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "avif": "image/avif",
    "heic": "image/heic",
}

ALLOWED_UPLOAD_AUDIO_EXTENSIONS = frozenset(
    {
        "m4a",
        "flac",
        "amr",
        "wav",
        "opus",
        "caf",
    }
)


def get_content_type_for_filename(filename: str) -> str:
    """Return content type for a media filename, defaulting to binary stream."""
    extension = filename.rsplit(".", 1)[-1].lower()
    return CONTENT_TYPES_BY_EXTENSION.get(extension, "application/octet-stream")


def is_allowed_upload_audio_extension(extension: str) -> bool:
    """Return True when the extension is allowed for upload endpoints."""
    return extension.lower() in ALLOWED_UPLOAD_AUDIO_EXTENSIONS
