"""Shared utility helpers."""

from uuid import UUID


def validate_uuid_v4(uuid_string: str) -> bool:
    """Return True if uuid_string is a valid UUID v4."""
    try:
        UUID(uuid_string, version=4)
        return True
    except (ValueError, AttributeError):
        return False
