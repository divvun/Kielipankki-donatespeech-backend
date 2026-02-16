"""Test discriminated union: MediaItem with itemType=yle-audio."""

from models import MediaItem, ScheduleItem


def test_media_item_yle_audio_valid():
    """Test valid MediaItem with kind=media and itemType=yle-audio."""
    item = MediaItem(
        kind="media",
        itemId="yle-audio-001",
        itemType="yle-audio",
        typeId="audio/mp3",
        url="1-50000093",  # YLE Areena program identifier
        description="YLE audio content",
        options=[],
        isRecording=False,
    )
    
    assert item.kind == "media"
    assert item.itemType == "yle-audio"
    assert item.typeId == "audio/mp3"
    assert item.url == "1-50000093"  # YLE program ID format
    assert item.isRecording is False


def test_media_item_yle_audio_in_schedule():
    """Test MediaItem yle-audio as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "yle-audio-002",
        "itemType": "yle-audio",
        "typeId": "audio/m4a",
        "url": "1-50000094",
        "description": "Another YLE audio",
        "options": [],
        "isRecording": True,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = MediaItem(**item_dict)
    
    assert isinstance(schedule_item, MediaItem)
    assert schedule_item.kind == "media"
    assert schedule_item.itemType == "yle-audio"
    assert schedule_item.url == "1-50000094"  # YLE program ID preserved


def test_media_item_yle_audio_various_ids():
    """Test MediaItem yle-audio with various YLE program IDs."""
    yle_ids = ["1-50000093", "1-60000001", "1-70000500", "2-999999"]
    
    for yle_id in yle_ids:
        item = MediaItem(
            kind="media",
            itemId=f"yle-{yle_id}",
            itemType="yle-audio",
            typeId="audio/mp3",
            url=yle_id,
            description=f"YLE content {yle_id}",
            options=[],
            isRecording=False,
        )
        
        assert item.itemType == "yle-audio"
        assert item.url == yle_id  # YLE ID stored directly for backend decryption
