"""Unit tests for language-aware storage path helpers."""

import pytest

import app.storage as storage


def test_normalize_language_tag():
    assert storage.normalize_language_tag(" NB_no ") == "nb-no"


def test_build_schedule_blob_name():
    assert (
        storage.build_schedule_blob_name("abc-123", "FI")
        == "schedule/abc-123/fi.json"
    )


def test_build_theme_blob_name():
    assert storage.build_theme_blob_name("theme-1", "sma") == "theme/theme-1/sma.json"


def test_parse_localized_blob_name_valid():
    assert storage.parse_localized_blob_name("theme/id-1/NB_no.json", "theme/") == (
        "id-1",
        "nb-no",
    )


def test_parse_localized_blob_name_legacy_flat_file_is_ignored():
    assert storage.parse_localized_blob_name("theme/id-1.json", "theme/") is None


def test_collect_available_languages_ignores_invalid_and_sorts():
    blob_names = [
        "theme/id-2/fi.json",
        "theme/id-1/nb.json",
        "theme/id-1/FI.json",
        "theme/id-1.json",
        "other/id-1/fi.json",
    ]

    assert storage.collect_available_languages(blob_names, "theme/") == {
        "id-1": ["fi", "nb"],
        "id-2": ["fi"],
    }


@pytest.mark.anyio
async def test_list_available_languages_by_id(monkeypatch):
    async def fake_list_blobs_with_prefix(prefix: str, max_results: int = 1000):
        assert prefix == "schedule/"
        assert max_results == 55
        return [
            "schedule/a/fi.json",
            "schedule/a/nb.json",
            "schedule/b/sma.json",
        ]

    monkeypatch.setattr(storage, "list_blobs_with_prefix", fake_list_blobs_with_prefix)

    assert await storage.list_available_languages_by_id("schedule/", max_results=55) == {
        "a": ["fi", "nb"],
        "b": ["sma"],
    }
