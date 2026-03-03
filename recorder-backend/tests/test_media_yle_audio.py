"""Test discriminated union: MediaItem with itemType=yle-audio."""

from models import YleAudioMediaItem, ScheduleItem


def test_media_item_yle_audio_valid():
    """Test valid MediaItem with kind=media and itemType=yle-audio."""
    item = YleAudioMediaItem(
        kind="media",
        itemId="yle-audio-001",
        itemType="yle-audio",
        url="1-50000093",  # YLE Areena program identifier
        default={
            "title": {"fi": "YLE audio", "nb": "YLE lyd"},
            "body1": {"fi": "YLE sisältö", "nb": "YLE innhold"},
            "body2": {"fi": "", "nb": ""},
        },
        isRecording=False,
    )

    assert item.itemType == "yle-audio"
    assert item.url == "1-50000093"  # YLE program ID format
    assert item.isRecording is False


def test_media_item_yle_audio_in_schedule():
    """Test MediaItem yle-audio as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "yle-audio-002",
        "itemType": "yle-audio",
        "typeId": None,
        "url": "1-50000094",
        "title": {"fi": "YLE ohjelma", "nb": "YLE program"},
        "body1": {"fi": "Toinen audio", "nb": "YLE lyd"},
        "body2": {"fi": "", "nb": ""},
        "options": [],
        "isRecording": True,
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = YleAudioMediaItem(**item_dict)

    assert isinstance(schedule_item, YleAudioMediaItem)
    assert schedule_item.itemType == "yle-audio"
    assert schedule_item.url == "1-50000094"  # YLE program ID preserved


def test_media_item_yle_audio_various_ids():
    """Test MediaItem yle-audio with various YLE program IDs."""
    yle_ids = ["1-50000093", "1-60000001", "1-70000500", "2-999999"]

    for yle_id in yle_ids:
        item = YleAudioMediaItem(
            kind="media",
            itemId=f"yle-{yle_id}",
            itemType="yle-audio",
            url=yle_id,
            default={
                "title": {"fi": "YLE audio", "nb": "YLE lyd"},
                "body1": {"fi": f"YLE sisältö {yle_id}", "nb": f"YLE innhold {yle_id}"},
                "body2": {"fi": "", "nb": ""},
            },
            isRecording=False,
        )

        assert item.itemType == "yle-audio"
        assert item.url == yle_id  # YLE ID stored directly for backend decryption
