"""Tests for shared media type helper functions."""

from app.media_types import (
    get_content_type_for_filename,
    is_allowed_upload_audio_extension,
)


def test_get_content_type_for_known_image_extension() -> None:
    """Returns expected MIME type for known image extensions."""
    assert get_content_type_for_filename("photo.jpg") == "image/jpeg"
    assert get_content_type_for_filename("icon.SVG") == "image/svg+xml"


def test_get_content_type_for_known_audio_extension() -> None:
    """Returns expected MIME type for known audio extensions."""
    assert get_content_type_for_filename("recording.m4a") == "audio/mp4"
    assert get_content_type_for_filename("sample.FLAC") == "audio/flac"


def test_get_content_type_defaults_to_octet_stream_for_unknown_extension() -> None:
    """Falls back to application/octet-stream for unknown extensions."""
    assert get_content_type_for_filename("archive.bin") == "application/octet-stream"
    assert get_content_type_for_filename("no_extension") == "application/octet-stream"


def test_is_allowed_upload_audio_extension_accepts_supported_extensions() -> None:
    """Upload allowlist accepts supported audio extensions."""
    assert is_allowed_upload_audio_extension("m4a")
    assert is_allowed_upload_audio_extension("WAV")


def test_is_allowed_upload_audio_extension_rejects_unsupported_extensions() -> None:
    """Upload allowlist rejects unsupported extensions."""
    assert not is_allowed_upload_audio_extension("mp3")
    assert not is_allowed_upload_audio_extension("png")
