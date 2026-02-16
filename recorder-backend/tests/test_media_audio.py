"""Test discriminated union: MediaItem with itemType=audio."""

from models import MediaItem, ScheduleItem


def test_media_item_audio_valid():
    """Test valid MediaItem with kind=media and itemType=audio."""
    item = MediaItem(
        kind="media",
        itemId="ce3c6012-25f0-4c69-a0ad-c5dc8e41b795",
        itemType="audio",
        typeId="audio/m4a",
        url="https://example.com/audio.m4a",
        description="Audio description",
        options=[],
        isRecording=True,
    )
    
    assert item.kind == "media"
    assert item.itemType == "audio"
    assert item.typeId == "audio/m4a"
    assert item.url == "https://example.com/audio.m4a"
    assert item.isRecording is True
    assert item.options == []


def test_media_item_audio_in_schedule():
    """Test MediaItem audio as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "ce3c6012-25f0-4c69-a0ad-c5dc8e41b795",
        "itemType": "audio",
        "typeId": "audio/m4a",
        "url": "https://example.com/audio.m4a",
        "description": "Audio description",
        "options": [],
        "isRecording": True,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = MediaItem(**item_dict)
    
    assert isinstance(schedule_item, MediaItem)
    assert schedule_item.kind == "media"
    assert schedule_item.itemType == "audio"


def test_media_item_audio_minimal():
    """Test MediaItem audio with minimal required fields."""
    item = MediaItem(
        kind="media",
        itemId="ce3c6012-25f0-4c69-a0ad-c5dc8e41b795",
        itemType="audio",
        typeId=None,
        url="audio.m4a",
        description="Minimal audio",
        options=[],
        isRecording=False,
    )
    
    assert item.kind == "media"
    assert item.itemType == "audio"
    assert item.typeId is None
    assert item.url == "audio.m4a"
