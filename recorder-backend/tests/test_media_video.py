"""Test discriminated union: MediaItem with itemType=video."""

from typing import Any

from pydantic import TypeAdapter

from app.models import VideoMediaItem, ScheduleItem


def test_media_item_video_valid():
    """Test valid MediaItem with kind=media and itemType=video."""
    item = VideoMediaItem(
        kind="media",
        itemId="f3c991c0-e2f2-4d4d-980d-0883230d84a1",
        itemType="video",
        typeId="video/mp4",
        isRecording=True,
    )

    assert item.itemType == "video"
    assert item.typeId == "video/mp4"
    assert item.isRecording is True


def test_media_item_video_in_schedule() -> None:
    """Test MediaItem video as ScheduleItem discriminated union."""
    item_dict: dict[str, Any] = {
        "kind": "media",
        "itemId": "f3c991c0-e2f2-4d4d-980d-0883230d84a1",
        "itemType": "video",
        "typeId": "video/webm",
        "options": [],
        "isRecording": False,
    }

    # Parse as ScheduleItem union
    schedule_item: ScheduleItem = TypeAdapter(ScheduleItem).validate_python(item_dict)

    assert isinstance(schedule_item, VideoMediaItem)
    assert schedule_item.itemType == "video"
    assert schedule_item.typeId == "video/webm"


def test_media_item_video_various_codecs():
    """Test MediaItem video with various MIME types."""
    mime_types = ["video/mp4", "video/webm", "video/avi", "video/quicktime"]

    for mime_type in mime_types:
        item = VideoMediaItem(
            kind="media",
            itemId="f3c991c0-e2f2-4d4d-980d-0883230d84a1",
            itemType="video",
            typeId=mime_type,
            isRecording=False,
        )

        assert item.itemType == "video"
        assert item.typeId == mime_type
