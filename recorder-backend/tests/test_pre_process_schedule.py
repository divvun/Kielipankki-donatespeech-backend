"""Unit tests for pre_process_schedule YLE item conversion behavior."""

from unittest.mock import patch

from app.main import pre_process_schedule
from app.models import (
    Schedule,
    YleAudioMediaItem,
    YleVideoMediaItem,
    ImageMediaItem,
    MediaState,
)


def _state(label: str, url: str | None = None) -> MediaState:
    return MediaState(
        title=f"{label}",
        body1=f"{label} body1",
        body2=f"{label} body2",
        url=url if url is not None else f"https://example.org/{label}.jpg",
    )


def test_pre_process_schedule_no_credentials_converts_yle_audio_with_all_fields(
    monkeypatch,
):
    monkeypatch.delenv("YLE_CLIENT_ID", raising=False)
    monkeypatch.delenv("YLE_CLIENT_KEY", raising=False)
    monkeypatch.delenv("YLE_DECRYPT", raising=False)

    original = YleAudioMediaItem(
        kind="media",
        itemType="yle-audio",
        itemId="yle-audio-001",
        typeId="audio/m4a",
        isRecording=True,
        start=_state("start"),
        recording=_state("recording", url="1-50000093"),
        finish=_state("finish"),
    )

    schedule = Schedule(items=[original])
    processed = pre_process_schedule(schedule)

    processed_item = processed.items[0]
    assert isinstance(processed_item, YleAudioMediaItem)

    expected = original.model_dump()
    expected["itemType"] = "yle-audio"
    assert processed_item.model_dump() == expected


def test_pre_process_schedule_no_credentials_converts_yle_video_with_all_fields(
    monkeypatch,
):
    monkeypatch.delenv("YLE_CLIENT_ID", raising=False)
    monkeypatch.delenv("YLE_CLIENT_KEY", raising=False)
    monkeypatch.delenv("YLE_DECRYPT", raising=False)

    original = YleVideoMediaItem(
        kind="media",
        itemType="yle-video",
        itemId="yle-video-001",
        typeId="video/mp4",
        isRecording=False,
        start=_state("start-video", url="1-50000094"),
        recording=_state("recording-video"),
        finish=_state("finish-video"),
    )

    schedule = Schedule(items=[original])
    processed = pre_process_schedule(schedule)

    processed_item = processed.items[0]
    assert isinstance(processed_item, YleVideoMediaItem)

    expected = original.model_dump()
    expected["itemType"] = "yle-video"
    assert processed_item.model_dump() == expected


def test_pre_process_schedule_map_error_falls_back_to_fake_with_full_data(monkeypatch):
    monkeypatch.setenv("YLE_CLIENT_ID", "client-id")
    monkeypatch.setenv("YLE_CLIENT_KEY", "client-key")
    monkeypatch.setenv("YLE_DECRYPT", "decrypt-key")

    original = YleAudioMediaItem(
        kind="media",
        itemType="yle-audio",
        itemId="yle-audio-err",
        typeId="audio/mpeg",
        isRecording=True,
        start=_state("start-error"),
        recording=_state("recording-error", url="1-50000100"),
        finish=_state("finish-error"),
    )

    processed = pre_process_schedule(Schedule(items=[original]))

    processed_item = processed.items[0]
    assert isinstance(processed_item, YleAudioMediaItem)

    expected = original.model_dump()
    expected["itemType"] = "yle-audio"
    assert processed_item.model_dump() == expected


def test_pre_process_schedule_configured_keeps_real_item_and_maps_url(monkeypatch):
    monkeypatch.setenv("YLE_CLIENT_ID", "client-id")
    monkeypatch.setenv("YLE_CLIENT_KEY", "client-key")
    monkeypatch.setenv("YLE_DECRYPT", "decrypt-key")

    original = YleVideoMediaItem(
        kind="media",
        itemType="yle-video",
        itemId="yle-video-map",
        typeId="video/mp4",
        isRecording=False,
        start=_state("start-map", url="1-50000101"),
    )

    with patch(
        "app.main.map_yle_content", return_value="https://example.org/stream.m3u8"
    ):
        processed = pre_process_schedule(Schedule(items=[original]))

    processed_item = processed.items[0]
    assert isinstance(processed_item, YleVideoMediaItem)
    assert (
        processed_item.start is not None
        and processed_item.start.url == "https://example.org/stream.m3u8"
    )


def test_pre_process_schedule_maps_local_media_urls_for_non_yle_items():
    schedule = Schedule(
        start=_state("schedule-start", url="cover image.jpg"),
        finish=_state("schedule-finish", url="done.png"),
        items=[
            ImageMediaItem(
                kind="media",
                itemType="image",
                itemId="image-001",
                typeId="image/jpeg",
                isRecording=False,
                start=_state("image-start", url="photo one.jpg"),
                recording=_state("image-recording", url="photo-two.jpg"),
                finish=_state("image-finish", url="photo-three.jpg"),
            )
        ],
    )

    processed = pre_process_schedule(schedule)

    assert processed.start is not None
    assert processed.start.url == "/v1/media/cover%20image.jpg"
    assert processed.finish is not None
    assert processed.finish.url == "/v1/media/done.png"

    item = processed.items[0]
    assert isinstance(item, ImageMediaItem)
    assert item.start is not None and item.start.url == "/v1/media/photo%20one.jpg"
    assert item.recording is not None and item.recording.url == "/v1/media/photo-two.jpg"
    assert item.finish is not None and item.finish.url == "/v1/media/photo-three.jpg"
