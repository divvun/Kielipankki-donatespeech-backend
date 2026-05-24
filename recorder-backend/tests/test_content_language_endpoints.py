"""Endpoint tests for language-aware theme loading."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.storage import StorageError

pytestmark = pytest.mark.anyio


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


async def test_theme_requires_lang_query_param():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-1")

    assert response.status_code == 422


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
async def test_theme_maps_local_media_url_to_media_route(mock_load_blob_json):
    payload = _theme_payload()
    payload["mediaState"]["url"] = "local image.jpg"
    mock_load_blob_json.return_value = payload

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-2", params={"lang": "fi"})

    assert response.status_code == 200
    assert response.json()["mediaState"]["url"] == "/v1/media/local%20image.jpg"


@patch("app.routers.content.load_blob_json", new_callable=AsyncMock)
async def test_theme_missing_language_returns_404(mock_load_blob_json):
    mock_load_blob_json.side_effect = StorageError("not found")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/theme/theme-404", params={"lang": "fi"})

    assert response.status_code == 404


# ── list endpoints ────────────────────────────────────────────────────────────


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
