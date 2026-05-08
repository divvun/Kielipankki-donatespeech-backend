"""Test discriminated union: MediaItem with itemType=text."""

from pydantic import TypeAdapter

from app.models import TextContentItem, ScheduleItem


def test_media_item_text_valid():
    """Test valid MediaItem with kind=media and itemType=text."""
    item = TextContentItem(
        kind="media",
        itemId="text-001",
        itemType="text-content",
        typeId="text/plain",
        isRecording=False,
    )

    assert item.itemType == "text-content"
    assert item.typeId == "text/plain"
    assert item.isRecording is False


def test_media_item_text_in_schedule()-> None:
    """Test MediaItem text as ScheduleItem discriminated union."""
    item = TextContentItem(
        kind="media",
        itemId="text-002",
        itemType="text-content",
        typeId="text/html",
        isRecording=True,
        start=None,
        recording=None,
        finish=None,
    )

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = TypeAdapter(ScheduleItem).validate_python(
        item.model_dump()
    )

    assert isinstance(schedule_item, TextContentItem)
    assert schedule_item.itemType == "text-content"
    assert schedule_item.typeId == "text/html"


def test_media_item_text_various_formats():
    """Test MediaItem text with various MIME types and content."""
    formats = [
        ("text/plain", "plain text"),
        ("text/html", "HTML formatted"),
        ("text/markdown", "Markdown formatted"),
        ("application/json", "JSON structure"),
    ]

    for mime_type, description in formats:
        item = TextContentItem(
            kind="media",
            itemId=f"text-{mime_type}",
            itemType="text-content",
            typeId=mime_type,
            isRecording=False,
        )

        assert item.itemType == "text-content"
        assert item.typeId == mime_type
