"""Test discriminated union: MediaItem with itemType=image."""

from models import MediaItem, ScheduleItem


def test_media_item_image_valid():
    """Test valid MediaItem with kind=media and itemType=image."""
    item = MediaItem(
        kind="media",
        itemId="image-001",
        itemType="image",
        typeId="image/jpeg",
        url="https://example.com/photo.jpg",
        description="Photo displayed to user",
        options=[],
        isRecording=False,
    )
    
    assert item.kind == "media"
    assert item.itemType == "image"
    assert item.typeId == "image/jpeg"
    assert item.url == "https://example.com/photo.jpg"
    assert item.isRecording is False


def test_media_item_image_in_schedule():
    """Test MediaItem image as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "image-002",
        "itemType": "image",
        "typeId": "image/png",
        "url": "https://example.com/screenshot.png",
        "description": "PNG screenshot",
        "options": [],
        "isRecording": True,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = MediaItem(**item_dict)
    
    assert isinstance(schedule_item, MediaItem)
    assert schedule_item.kind == "media"
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
        item = MediaItem(
            kind="media",
            itemId=f"image-{mime_type.split('/')[1]}",
            itemType="image",
            typeId=mime_type,
            url=f"image.{mime_type.split('/')[1]}",
            description=f"Image in {mime_type} format",
            options=[],
            isRecording=False,
        )
        
        assert item.itemType == "image"
        assert item.typeId == mime_type
