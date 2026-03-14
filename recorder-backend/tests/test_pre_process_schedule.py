"""Unit tests for pre_process_schedule YLE item conversion behavior."""

from unittest.mock import patch

from main import pre_process_schedule
from models import (
    FakeYleAudioMediaItem,
    FakeYleVideoMediaItem,
    Schedule,
    YleAudioMediaItem,
    YleVideoMediaItem,
)


def _state(label: str, url: str = None) -> dict:
    return {
        "title": {"fi": f"{label} fi", "nb": f"{label} nb"},
        "body1": {"fi": f"{label} body1 fi", "nb": f"{label} body1 nb"},
        "body2": {"fi": f"{label} body2 fi", "nb": f"{label} body2 nb"},
        "url": url if url is not None else f"https://example.org/{label}.jpg",
    }


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
        options=[],
        isRecording=True,
        start=_state("start"),
        recording=_state("recording", url="1-50000093"),
        finish=_state("finish"),
    )

    schedule = Schedule(items=[original])
    processed = pre_process_schedule(schedule)

    processed_item = processed.items[0]
    assert isinstance(processed_item, FakeYleAudioMediaItem)

    expected = original.model_dump()
    expected["itemType"] = "fake-yle-audio"
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
        options=[],
        isRecording=False,
        start=_state("start-video", url="1-50000094"),
        recording=_state("recording-video"),
        finish=_state("finish-video"),
    )

    schedule = Schedule(items=[original])
    processed = pre_process_schedule(schedule)

    processed_item = processed.items[0]
    assert isinstance(processed_item, FakeYleVideoMediaItem)

    expected = original.model_dump()
    expected["itemType"] = "fake-yle-video"
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
        options=[],
        isRecording=True,
        start=_state("start-error"),
        recording=_state("recording-error", url="1-50000100"),
        finish=_state("finish-error"),
    )

    with patch("main.map_yle_content", side_effect=RuntimeError("mapping failed")):
        processed = pre_process_schedule(Schedule(items=[original]))

    processed_item = processed.items[0]
    assert isinstance(processed_item, FakeYleAudioMediaItem)

    expected = original.model_dump()
    expected["itemType"] = "fake-yle-audio"
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
        options=[],
        isRecording=False,
        start=_state("start-map", url="1-50000101"),
    )

    with patch("main.map_yle_content", return_value="https://example.org/stream.m3u8"):
        processed = pre_process_schedule(Schedule(items=[original]))

    processed_item = processed.items[0]
    assert isinstance(processed_item, YleVideoMediaItem)
    assert processed_item.start.url == "https://example.org/stream.m3u8"
