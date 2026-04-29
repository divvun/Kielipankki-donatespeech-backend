"""Endpoint tests for language-aware schedule/theme loading."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from storage import StorageError

pytestmark = pytest.mark.anyio


def _state(label: str) -> dict:
    return {
        "title": {"fi": f"{label} fi", "nb": f"{label} nb"},
        "body1": {"fi": f"{label} body1 fi", "nb": f"{label} body1 nb"},
        "body2": {"fi": f"{label} body2 fi", "nb": f"{label} body2 nb"},
    }


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
        "title": {"fi": "Teema", "nb": "Tema"},
        "body1": {"fi": "body1 fi", "nb": "body1 nb"},
        "body2": {"fi": "body2 fi", "nb": "body2 nb"},
        "scheduleIds": ["s-1"],
    }


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


@patch("main.load_blob_json", new_callable=AsyncMock)
async def test_schedule_loads_language_specific_blob(mock_load_blob_json):
    mock_load_blob_json.return_value = _schedule_payload()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule/sched-1", params={"lang": "NB_no"})

    assert response.status_code == 200
    assert response.json()["id"] == "sched-1"
    mock_load_blob_json.assert_awaited_once_with("schedule/sched-1/nb-no.json")


@patch("main.load_blob_json", new_callable=AsyncMock)
async def test_theme_loads_language_specific_blob(mock_load_blob_json):
    mock_load_blob_json.return_value = _theme_payload()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-1", params={"lang": "fi"})

    assert response.status_code == 200
    assert response.json()["id"] == "theme-1"
    mock_load_blob_json.assert_awaited_once_with("theme/theme-1/fi.json")


@patch("main.load_blob_json", new_callable=AsyncMock)
async def test_schedule_missing_language_returns_404(mock_load_blob_json):
    mock_load_blob_json.side_effect = StorageError("not found")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/schedule/sched-404", params={"lang": "fi"})

    assert response.status_code == 404


@patch("main.load_blob_json", new_callable=AsyncMock)
async def test_theme_missing_language_returns_404(mock_load_blob_json):
    mock_load_blob_json.side_effect = StorageError("not found")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-404", params={"lang": "fi"})

    assert response.status_code == 404
