"""Test discriminated union: MediaItem with itemType=yle-video."""

from models import YleVideoMediaItem, ScheduleItem, MediaState


def test_media_item_yle_video_valid():
    """Test valid MediaItem with kind=media and itemType=yle-video."""
    item = YleVideoMediaItem(
        kind="media",
        itemId="yle-video-001",
        itemType="yle-video",
        start=MediaState(
            title={"fi": "Otsikko"},
            body1={"fi": "Teksti"},
            body2={"fi": ""},
            url="1-50000093",
        ),
        isRecording=True,
    )

    assert item.itemType == "yle-video"
    assert item.start.url == "1-50000093"
    assert item.isRecording is True


def test_media_item_yle_video_in_schedule():
    """Test MediaItem yle-video as ScheduleItem discriminated union."""
    item_dict = {
        "kind": "media",
        "itemId": "yle-video-002",
        "itemType": "yle-video",
        "typeId": None,
        "options": [],
        "isRecording": False,
        "start": {
            "title": {"fi": "Otsikko"},
            "body1": {"fi": "Teksti"},
            "body2": {"fi": ""},
            "url": "1-50000094",
        },
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = YleVideoMediaItem(**item_dict)

    assert isinstance(schedule_item, YleVideoMediaItem)
    assert schedule_item.itemType == "yle-video"
    assert schedule_item.start.url == "1-50000094"


def test_media_item_yle_video_various_ids():
    """Test MediaItem yle-video with various YLE program IDs."""
    yle_ids = ["1-50000093", "1-60000001", "1-70000500", "2-999999"]

    for yle_id in yle_ids:
        item = YleVideoMediaItem(
            kind="media",
            itemId=f"yle-vid-{yle_id}",
            itemType="yle-video",
            start=MediaState(
                title={"fi": "Otsikko"},
                body1={"fi": "Teksti"},
                body2={"fi": ""},
                url=yle_id,
            ),
            isRecording=True,
        )

        assert item.itemType == "yle-video"
        assert item.start.url == yle_id
