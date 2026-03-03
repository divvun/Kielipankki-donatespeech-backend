"""Test discriminated union: MediaItem with itemType=image."""

from models import ImageMediaItem, ScheduleItem, MediaState


def test_media_item_image_valid():
    """Test valid MediaItem with kind=media and itemType=image."""
    item = ImageMediaItem(
        kind="media",
        itemId="image-001",
        itemType="image",
        typeId="image/jpeg",
        url="https://example.com/photo.jpg",
        default=MediaState(
            title={"fi": "Kuva", "nb": "Bilde"},
            body1={"fi": "Kuvaus", "nb": "Beskrivelse"},
            body2={"fi": "", "nb": ""},
        ),
        isRecording=False,
    )

    assert item.itemType == "image"
    assert item.typeId == "image/jpeg"
    assert item.url == "https://example.com/photo.jpg"
    assert item.isRecording is False
    assert item.default.title["fi"] == "Kuva"


def test_media_item_image_in_schedule() -> None:
    """Test MediaItem image as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "image-002",
        "itemType": "image",
        "typeId": "image/png",
        "url": "https://example.com/screenshot.png",
        "default": {
            "title": {"fi": "Ruutukaappaus", "nb": "Skjermbilde"},
            "body1": {"fi": "PNG kuva", "nb": "PNG bilde"},
            "body2": {"fi": "", "nb": ""},
        },
        "options": [],
        "isRecording": True,
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = ImageMediaItem(**item_dict)  # ty:ignore[invalid-argument-type]

    assert isinstance(schedule_item, ImageMediaItem)
    assert schedule_item.itemType == "image"
    assert schedule_item.typeId == "image/png"
    assert schedule_item.default.title["fi"] == "Ruutukaappaus"


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
            url=f"image.{mime_type.split('/')[1]}",
            default=MediaState(
                title={"fi": "Kuva", "nb": "Bilde"},
                body1={
                    "fi": f"Kuva {mime_type} muodossa",
                    "nb": f"Bilde i {mime_type} format",
                },
                body2={"fi": "", "nb": ""},
            ),
            isRecording=False,
        )

        assert item.itemType == "image"
        assert item.typeId == mime_type
