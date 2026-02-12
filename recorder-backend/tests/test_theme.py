"""Tests for theme.py - load_theme and load_all_themes endpoints."""

import json
import pytest
from tests.conftest import TEST_THEME_ID, TEST_THEME_ID_2


def test_load_theme_success(mock_env, lambda_context):
    """Test successful loading of a single theme."""
    from theme import load_theme

    event = {"pathParameters": {"id": TEST_THEME_ID}}

    response = load_theme(event, lambda_context)

    assert response["statusCode"] == 200
    assert "Access-Control-Allow-Origin" in response["headers"]

    body = json.loads(response["body"])
    assert "description" in body
    assert "image" in body
    assert "scheduleIds" in body
    assert isinstance(body["scheduleIds"], list)


def test_load_theme_structure(mock_env, lambda_context):
    """Test that loaded theme has correct structure matching test data."""
    from theme import load_theme

    event = {"pathParameters": {"id": TEST_THEME_ID}}

    response = load_theme(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])

    # Verify expected fields from test/theme.json
    assert body["description"] == "Koronavirus 2020"
    assert "jpg" in body["image"]  # Image URL should contain jpg extension
    assert len(body["scheduleIds"]) == 2


def test_load_theme_different_ids(mock_env, lambda_context):
    """Test loading themes with different IDs."""
    from theme import load_theme

    for theme_id in [TEST_THEME_ID, TEST_THEME_ID_2]:
        event = {"pathParameters": {"id": theme_id}}

        response = load_theme(event, lambda_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "description" in body
        assert "scheduleIds" in body


def test_load_theme_nonexistent_id(mock_env, lambda_context):
    """Test loading theme with non-existent ID."""
    from theme import load_theme
    from common import FileProcessingError

    event = {"pathParameters": {"id": "00000000-0000-0000-0000-000000000000"}}

    with pytest.raises(FileProcessingError):
        load_theme(event, lambda_context)


def test_load_all_themes_success(mock_env, lambda_context):
    """Test successful loading of all themes."""
    from theme import load_all_themes

    event = {}

    response = load_all_themes(event, lambda_context)

    assert response["statusCode"] == 200
    assert "Access-Control-Allow-Origin" in response["headers"]

    body = json.loads(response["body"])
    assert isinstance(body, list)
    assert len(body) > 0

    # Verify structure
    for theme_item in body:
        assert "id" in theme_item
        assert "content" in theme_item
        assert "description" in theme_item["content"]
        assert "image" in theme_item["content"]
        assert "scheduleIds" in theme_item["content"]


def test_load_all_themes_contains_expected_ids(mock_env, lambda_context):
    """Test that all uploaded test themes are present."""
    from theme import load_all_themes

    event = {}

    response = load_all_themes(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])

    ids = [theme["id"] for theme in body]

    # Check our test IDs are present
    assert TEST_THEME_ID in ids
    assert TEST_THEME_ID_2 in ids


def test_load_all_themes_count(mock_env, lambda_context):
    """Test that correct number of themes are returned."""
    from theme import load_all_themes

    event = {}

    response = load_all_themes(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])

    # We uploaded 2 test themes in conftest.py
    assert len(body) == 2


def test_load_all_themes_content_matches(mock_env, lambda_context):
    """Test that theme content matches what was uploaded."""
    from theme import load_all_themes

    event = {}

    response = load_all_themes(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])

    # Find a specific theme
    theme = next((t for t in body if t["id"] == TEST_THEME_ID), None)
    assert theme is not None

    # Verify content
    assert theme["content"]["description"] == "Koronavirus 2020"
    assert len(theme["content"]["scheduleIds"]) == 2


def test_load_theme_cors_headers(mock_env, lambda_context):
    """Test that CORS headers are properly set."""
    from theme import load_theme

    event = {"pathParameters": {"id": TEST_THEME_ID}}

    response = load_theme(event, lambda_context)

    assert response["statusCode"] == 200
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"


def test_load_all_themes_cors_headers(mock_env, lambda_context):
    """Test that CORS headers are properly set for all themes."""
    from theme import load_all_themes

    event = {}

    response = load_all_themes(event, lambda_context)

    assert response["statusCode"] == 200
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
