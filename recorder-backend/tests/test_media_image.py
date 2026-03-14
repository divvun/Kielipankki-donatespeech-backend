"""Test discriminated union: MediaItem with itemType=image."""

from models import ImageMediaItem, ScheduleItem


def test_media_item_image_valid():
    """Test valid MediaItem with kind=media and itemType=image."""
    item = ImageMediaItem(
        kind="media",
        itemId="image-001",
        itemType="image",
        typeId="image/jpeg",
        isRecording=False,
    )

    assert item.itemType == "image"
    assert item.typeId == "image/jpeg"
    assert item.isRecording is False


def test_media_item_image_in_schedule() -> None:
    """Test MediaItem image as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "image-002",
        "itemType": "image",
        "typeId": "image/png",
        "options": [],
        "isRecording": True,
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = ImageMediaItem(**item_dict)  # ty:ignore[invalid-argument-type]

    assert isinstance(schedule_item, ImageMediaItem)
    assert schedule_item.itemType == "image"
    assert schedule_item.typeId == "image/png"


def test_media_item_image_various_formats():
    """Test MediaItem image with various image format MIME types."""
    formats = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "image/svg+xml",
        "image/bmp",
        "image/tiff",
    ]

    for mime_type in formats:
        item = ImageMediaItem(
            kind="media",
            itemId=f"image-{mime_type.split('/')[1]}",
            itemType="image",
            typeId=mime_type,
            isRecording=False,
        )

        assert item.itemType == "image"
        assert item.typeId == mime_type
