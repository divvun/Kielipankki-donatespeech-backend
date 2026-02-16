"""Test discriminated union: MediaItem with itemType=yle-video."""

from models import MediaItem, ScheduleItem


def test_media_item_yle_video_valid():
    """Test valid MediaItem with kind=media and itemType=yle-video."""
    item = MediaItem(
        kind="media",
        itemId="yle-video-001",
        itemType="yle-video",
        typeId="video/mp4",
        url="1-50000093",  # YLE Areena program identifier
        description="YLE video content",
        options=[],
        isRecording=True,
    )
    
    assert item.kind == "media"
    assert item.itemType == "yle-video"
    assert item.typeId == "video/mp4"
    assert item.url == "1-50000093"  # YLE program ID format
    assert item.isRecording is True


def test_media_item_yle_video_in_schedule():
    """Test MediaItem yle-video as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "yle-video-002",
        "itemType": "yle-video",
        "typeId": "video/webm",
        "url": "1-50000094",
        "description": "Another YLE video",
        "options": [],
        "isRecording": False,
    }
    
    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = MediaItem(**item_dict)
    
    assert isinstance(schedule_item, MediaItem)
    assert schedule_item.kind == "media"
    assert schedule_item.itemType == "yle-video"
    assert schedule_item.url == "1-50000094"  # YLE program ID preserved


def test_media_item_yle_video_various_ids():
    """Test MediaItem yle-video with various YLE program IDs."""
    yle_ids = ["1-50000093", "1-60000001", "1-70000500", "2-999999"]
    
    for yle_id in yle_ids:
        item = MediaItem(
            kind="media",
            itemId=f"yle-vid-{yle_id}",
            itemType="yle-video",
            typeId="video/mp4",
            url=yle_id,
            description=f"YLE video {yle_id}",
            options=[],
            isRecording=True,
        )
        
        assert item.itemType == "yle-video"
        assert item.url == yle_id  # YLE ID stored directly for backend decryption
