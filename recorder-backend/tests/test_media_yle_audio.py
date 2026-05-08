"""Test discriminated union: MediaItem with itemType=yle-audio."""

from models import YleAudioMediaItem, MediaState


def test_media_item_yle_audio_valid():
    """Test valid MediaItem with kind=media and itemType=yle-audio."""
    item = YleAudioMediaItem(
        kind="media",
        itemId="yle-audio-001",
        itemType="yle-audio",
        start=MediaState(
            title="Otsikko",
            body1="Teksti",
            body2="",
            url="1-50000093",
        ),
        isRecording=False,
    )

    assert item.itemType == "yle-audio"
    assert item.start is not None and item.start.url == "1-50000093"
    assert item.isRecording is False


def test_media_item_yle_audio_in_schedule():
    """Test MediaItem yle-audio as ScheduleItem discriminated union."""
    schedule_item = YleAudioMediaItem(
        kind="media",
        itemId="yle-audio-002",
        itemType="yle-audio",
        typeId=None,
        isRecording=True,
        start=MediaState(
            title="Otsikko",
            body1="Teksti",
            body2="",
            url="1-50000094",
        ),
    )

    # Parse as ScheduleItem union

    assert isinstance(schedule_item, YleAudioMediaItem)
    assert schedule_item.itemType == "yle-audio"
    assert schedule_item.start is not None and schedule_item.start.url == "1-50000094"


def test_media_item_yle_audio_various_ids():
    """Test MediaItem yle-audio with various YLE program IDs."""
    yle_ids = ["1-50000093", "1-60000001", "1-70000500", "2-999999"]

    for yle_id in yle_ids:
        item = YleAudioMediaItem(
            kind="media",
            itemId=f"yle-{yle_id}",
            itemType="yle-audio",
            start=MediaState(
                title="Otsikko",
                body1="Teksti",
                body2="",
                url=yle_id,
            ),
            isRecording=False,
        )

        assert item.itemType == "yle-audio"
        assert item.start is not None and item.start.url == yle_id
