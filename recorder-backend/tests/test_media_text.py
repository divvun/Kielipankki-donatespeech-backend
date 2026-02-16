"""Test discriminated union: MediaItem with itemType=text."""

from models import TextMediaItem, ScheduleItem


def test_media_item_text_valid():
    """Test valid MediaItem with kind=media and itemType=text."""
    item = TextMediaItem(
        kind="media",
        itemId="text-001",
        itemType="text",
        typeId="text/plain",
        url="https://example.com/text-content.txt",
        description="Text content displayed to user",
        options=[],
        isRecording=False,
    )
    
    assert item.kind == "media"
    assert item.itemType == "text"
    assert item.typeId == "text/plain"
    assert item.url == "https://example.com/text-content.txt"
    assert item.isRecording is False


def test_media_item_text_in_schedule():
    """Test MediaItem text as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "text-002",
        "itemType": "text",
        "typeId": "text/html",
        "url": "https://example.com/text.html",
        "description": "HTML formatted text",
        "options": [],
        "isRecording": True,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = TextMediaItem(**item_dict)
    
    assert isinstance(schedule_item, TextMediaItem)
    assert schedule_item.kind == "media"
    assert schedule_item.itemType == "text"
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
        item = TextMediaItem(
            kind="media",
            itemId=f"text-{mime_type}",
            itemType="text",
            typeId=mime_type,
            url=f"content-{mime_type}.file",
            description=description,
            options=[],
            isRecording=False,
        )
        
        assert item.itemType == "text"
        assert item.typeId == mime_type
        assert item.description == description
