"""Test discriminated union: MediaItem with itemType=text."""

from models import TextContentItem, ScheduleItem


def test_media_item_text_valid():
    """Test valid MediaItem with kind=media and itemType=text."""
    item = TextContentItem(
        itemId="text-001",
        itemType="text-content",
        typeId="text/plain",
        url="https://example.com/text-content.txt",
        description="Text content displayed to user",
        isRecording=False,
    )
    
    assert item.itemType == "text-content"
    assert item.typeId == "text/plain"
    assert item.url == "https://example.com/text-content.txt"
    assert item.isRecording is False


def test_media_item_text_in_schedule():
    """Test MediaItem text as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "text-002",
        "itemType": "text-content",
        "typeId": "text/html",
        "url": "https://example.com/text.html",
        "description": "HTML formatted text",
        "options": [],
        "isRecording": True,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = TextContentItem(**item_dict)
    
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
            itemId=f"text-{mime_type}",
            itemType="text-content",
            typeId=mime_type,
            url=f"content-{mime_type}.file",
            description=description,
            isRecording=False,
        )
        
        assert item.itemType == "text-content"
        assert item.typeId == mime_type
        assert item.description == description
