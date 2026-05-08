"""Endpoint tests for language-aware schedule/theme loading."""

from app.models import MediaState

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.storage import StorageError

pytestmark = pytest.mark.anyio


def _state(label: str) -> MediaState:
    return MediaState(
        title=f"{label} fi",
        body1=f"{label} body1 fi",
        body2=f"{label} body2 fi",
        url=f"https://example.org/{label}.jpg",
    )


def _schedule_payload() -> dict:
    return {
        "items": [
            {
                "kind": "prompt",
                "itemType": "text",
                "itemId": "550e8400-e29b-41d4-a716-446655440000",
                "typeId": None,
                "options": [],
                "isRecording": False,
                "start": _state("prompt-start"),
            }
        ]
    }


def _theme_payload() -> dict:
    return {
        "mediaState": {
            "title": "Teema",
            "body1": "body1 fi",
            "body2": "body2 fi",
            "url": "https://example.org/theme.jpg",
        },
        "schedule": {"items": []},
    }


# ── single-item lang required ─────────────────────────────────────────────────


async def test_schedule_requires_lang_query_param():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule/sched-1")

    assert response.status_code == 422


async def test_theme_requires_lang_query_param():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-1")

    assert response.status_code == 422


@patch("app.routers.content.load_blob_json", new_callable=AsyncMock)
async def test_schedule_loads_language_specific_blob(mock_load_blob_json):
    mock_load_blob_json.return_value = _schedule_payload()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule/sched-1", params={"lang": "NB_no"})

    assert response.status_code == 200
    assert response.json()["id"] == "sched-1"
    mock_load_blob_json.assert_awaited_once_with("schedule/sched-1/nb-no.json")


@patch("app.routers.content.load_blob_json", new_callable=AsyncMock)
async def test_theme_loads_language_specific_blob(mock_load_blob_json):
    mock_load_blob_json.return_value = _theme_payload()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-1", params={"lang": "fi"})

    assert response.status_code == 200
    assert response.json()["id"] == "theme-1"
    mock_load_blob_json.assert_awaited_once_with("theme/theme-1/fi.json")


@patch("app.routers.content.load_blob_json", new_callable=AsyncMock)
async def test_schedule_missing_language_returns_404(mock_load_blob_json):
    mock_load_blob_json.side_effect = StorageError("not found")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule/sched-404", params={"lang": "fi"})

    assert response.status_code == 404


@patch("app.routers.content.load_blob_json", new_callable=AsyncMock)
async def test_theme_missing_language_returns_404(mock_load_blob_json):
    mock_load_blob_json.side_effect = StorageError("not found")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-404", params={"lang": "fi"})

    assert response.status_code == 404


# ── list endpoints ────────────────────────────────────────────────────────────


@patch("app.routers.content.list_available_languages_by_id", new_callable=AsyncMock)
async def test_list_schedules_returns_availability(mock_list):
    mock_list.return_value = {"sched-a": ["fi", "nb"], "sched-b": ["sma"]}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule")

    assert response.status_code == 200
    data = response.json()
    assert {"id": "sched-a", "availableLanguages": ["fi", "nb"]} in data
    assert {"id": "sched-b", "availableLanguages": ["sma"]} in data
    mock_list.assert_awaited_once_with("schedule/")


@patch("app.routers.content.list_available_languages_by_id", new_callable=AsyncMock)
async def test_list_themes_returns_availability(mock_list):
    mock_list.return_value = {"theme-x": ["fi"]}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme")

    assert response.status_code == 200
    assert response.json() == [{"id": "theme-x", "availableLanguages": ["fi"]}]


# ── per-ID discovery endpoints ────────────────────────────────────────────────


@patch("app.routers.content.list_blobs_with_prefix", new_callable=AsyncMock)
async def test_schedule_languages_returns_sorted_list(mock_list_blobs):
    mock_list_blobs.return_value = [
        "schedule/sched-1/nb.json",
        "schedule/sched-1/fi.json",
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule/sched-1/languages")

    assert response.status_code == 200
    assert response.json() == {"id": "sched-1", "availableLanguages": ["fi", "nb"]}


@patch("app.routers.content.list_blobs_with_prefix", new_callable=AsyncMock)
async def test_schedule_languages_returns_404_when_empty(mock_list_blobs):
    mock_list_blobs.return_value = []

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule/missing-id/languages")

    assert response.status_code == 404


@patch("app.routers.content.list_blobs_with_prefix", new_callable=AsyncMock)
async def test_theme_languages_returns_sorted_list(mock_list_blobs):
    mock_list_blobs.return_value = [
        "theme/theme-1/sma.json",
        "theme/theme-1/fi.json",
    ]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-1/languages")

    assert response.status_code == 200
    assert response.json() == {"id": "theme-1", "availableLanguages": ["fi", "sma"]}


@patch("app.routers.content.list_blobs_with_prefix", new_callable=AsyncMock)
async def test_theme_languages_returns_404_when_empty(mock_list_blobs):
    mock_list_blobs.return_value = []

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/missing-id/languages")

    assert response.status_code == 404
