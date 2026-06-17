"""Tests for YLE media endpoint routing."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_yle_media_endpoint(monkeypatch):
    """The canonical YLE media route should resolve program IDs."""
    monkeypatch.setattr("app.routers.media.map_yle_content", lambda pid: f"mapped:{pid}")

    response = client.get("/v1/yle-media/1-50525862")

    assert response.status_code == 200
    assert response.json() == "mapped:1-50525862"


def test_yle_media_compat_endpoint(monkeypatch):
    """Compatibility route should handle accidentally prefixed YLE URLs."""
    monkeypatch.setattr("app.routers.media.map_yle_content", lambda pid: f"mapped:{pid}")

    response = client.get("/v1/media/v1/yle-media/1-50525862")

    assert response.status_code == 200
    assert response.json() == "mapped:1-50525862"
