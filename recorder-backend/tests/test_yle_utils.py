"""Tests for yle_utils module - YLE API integration."""

from unittest.mock import patch, MagicMock
import pytest
import requests

from app.yle_utils import (
    map_yle_content,
    get_media_url,
    FileProcessingError,
)


class TestGetMediaUrl:
    """Test YLE media URL retrieval."""

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.requests.get")
    def test_get_media_url_success(self, mock_requests_get):
        """Test successful retrieval of media URL."""
        # Mock the response from YLE program info API
        program_response = {
            "data": {
                "publicationEvent": [
                    {
                        "temporalStatus": "currently",
                        "media": {"id": "test-media-id-123"},
                    },
                    {
                        "temporalStatus": "in_future",
                        "media": {"id": "future-media-id"},
                    },
                ]
            }
        }

        mock_response = MagicMock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = program_response
        mock_requests_get.return_value = mock_response

        result = get_media_url("1-50000093")

        assert "/v6/test-media-id-123/playouts.json" in result
        assert "app_id=test_client_id" in result
        assert "app_key=test_client_key" in result

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.requests.get")
    def test_get_media_url_no_current_publication(self, mock_requests_get):
        """Test first publication event is used even when not currently."""
        # Mock response with no "currently" status; first event should still be used
        program_response = {
            "data": {
                "publicationEvent": [
                    {
                        "temporalStatus": "in_future",
                        "media": {"id": "future-media-id"},
                    }
                ]
            }
        }

        mock_response = MagicMock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = program_response
        mock_requests_get.return_value = mock_response

        result = get_media_url("1-50000093")

        assert "/v6/future-media-id/playouts.json" in result

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.requests.get")
    def test_get_media_url_uses_first_publication(self, mock_requests_get):
        """Current implementation uses the first publication event in the payload."""
        program_response = {
            "data": {
                "publicationEvent": [
                    {
                        "temporalStatus": "in_future",
                        "media": {"id": "future-media-id"},
                    },
                    {
                        "temporalStatus": "currently",
                        "media": {"id": "current-media-id"},
                    },
                ]
            }
        }

        mock_response = MagicMock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = program_response
        mock_requests_get.return_value = mock_response

        result = get_media_url("1-50000093")

        assert "/v6/future-media-id/playouts.json" in result

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.requests.get")
    def test_get_media_url_empty_publication_events(self, mock_requests_get):
        """Test handling when publication events are empty."""
        program_response = {"data": {"publicationEvent": []}}

        mock_response = MagicMock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = program_response
        mock_requests_get.return_value = mock_response

        with pytest.raises(FileProcessingError, match="No publication events found"):
            get_media_url("1-50000093")


class TestMapYleContent:
    """Test main YLE content mapping function."""

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.get_media_url")
    @patch("app.yle_utils.requests.get")
    def test_map_yle_content_success(self, mock_requests_get, mock_get_media_url):
        """Test successful mapping of YLE program ID to media URL."""
        # Mock get_media_url to return a URL
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json?..."

        mock_response = MagicMock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "data": {"hls": {"url": "https://yle-vod.akamaized.net/media.m3u8"}}
        }
        mock_requests_get.return_value = mock_response

        result = map_yle_content("1-50000093")

        assert result == "https://yle-vod.akamaized.net/media.m3u8"
        mock_get_media_url.assert_called_once_with("1-50000093")

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.get_media_url")
    def test_map_yle_content_error_handling(self, mock_get_media_url):
        """Test error handling when YLE API fails."""
        # Mock get_media_url to raise an exception
        mock_get_media_url.side_effect = Exception("API Error")

        with pytest.raises(FileProcessingError):
            map_yle_content("1-50000093")

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.get_media_url")
    @patch("app.yle_utils.requests.get")
    def test_map_yle_content_network_timeout(self, mock_requests_get, mock_get_media_url):
        """Test handling of network timeouts."""
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json"

        mock_requests_get.side_effect = requests.RequestException("Timeout")

        with pytest.raises(FileProcessingError):
            map_yle_content("1-50000093")

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.get_media_url")
    @patch("app.yle_utils.requests.get")
    def test_map_yle_content_invalid_response(self, mock_requests_get, mock_get_media_url):
        """Test handling of invalid API response."""
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json"

        mock_response = MagicMock(spec=requests.Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("invalid json")
        mock_requests_get.return_value = mock_response

        with pytest.raises(FileProcessingError):
            map_yle_content("1-50000093")

    @patch("app.yle_utils.CLIENT_ID", None)
    @patch("app.yle_utils.CLIENT_KEY", None)
    def test_map_yle_content_without_credentials_returns_program_id(self):
        """Test fallback mode when YLE credentials are not configured."""
        program_id = "1-50000093"
        assert map_yle_content(program_id) == program_id


class TestYleIntegration:
    """Integration tests for YLE utilities (require mocking full flow)."""

    @patch("app.yle_utils.CLIENT_ID", "test_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_key")
    @patch("app.yle_utils.requests.get")
    def test_full_yle_flow(self, mock_requests_get):
        """Test complete flow from program ID to media URL."""
        # Setup mocks for the entire flow

        # 1. Mock program info API response
        program_response = {
            "data": {
                "publicationEvent": [
                    {
                        "temporalStatus": "currently",
                        "media": {"id": "media-123"},
                    }
                ]
            }
        }

        media_response = {"data": {"hls": {"url": "https://decrypted.url/media.m3u8"}}}

        program_http_response = MagicMock(spec=requests.Response)
        program_http_response.raise_for_status.return_value = None
        program_http_response.json.return_value = program_response

        media_http_response = MagicMock(spec=requests.Response)
        media_http_response.raise_for_status.return_value = None
        media_http_response.json.return_value = media_response

        mock_requests_get.side_effect = [program_http_response, media_http_response]

        # Execute the full flow
        result = map_yle_content("1-50000093")

        assert result == "https://decrypted.url/media.m3u8"
        assert mock_requests_get.call_count == 2
