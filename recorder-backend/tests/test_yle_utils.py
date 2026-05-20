"""Tests for yle_utils module - YLE API integration."""

import json
from unittest.mock import patch, MagicMock
import pytest

from app.yle_utils import (
    map_yle_content,
    get_media_url,
    FileProcessingError,
)


class TestGetMediaUrl:
    """Test YLE media URL retrieval."""

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_get_media_url_success(self, mock_urlopen):
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

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(program_response).encode()
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        result = get_media_url("1-50000093")

        # Verify it returns the correct media URL format
        assert "program_id=1-50000093" in result
        assert "/v6/test-media-id-123/playouts.json" in result
        assert "app_id=test_client_id" in result
        assert "app_key=test_client_key" in result
        assert "protocol=HLS" in result

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_get_media_url_no_current_publication(self, mock_urlopen):
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

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(program_response).encode()
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        result = get_media_url("1-50000093")

        assert "program_id=1-50000093" in result
        assert "/v6/future-media-id/playouts.json" in result

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_get_media_url_prefers_current_publication(self, mock_urlopen):
        """Test currently active publication event is preferred over the first one."""
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

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(program_response).encode()
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        result = get_media_url("1-50000093")

        assert "program_id=1-50000093" in result
        assert "/v6/current-media-id/playouts.json" in result

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_get_media_url_empty_publication_events(self, mock_urlopen):
        """Test handling when publication events are empty."""
        program_response = {"data": {"publicationEvent": []}}

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(program_response).encode()
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        with pytest.raises(FileProcessingError, match="no publication events"):
            get_media_url("1-50000093")


class TestMapYleContent:
    """Test main YLE content mapping function."""

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.get_media_url")
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_map_yle_content_success(self, mock_urlopen, mock_get_media_url):
        """Test successful mapping of YLE program ID to media URL."""
        # Mock get_media_url to return a URL
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json?..."

        # Mock the media playouts API response
        media_response = {"data": [{"url": "https://yle-vod.akamaized.net/media.m3u8"}]}

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(media_response).encode()
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

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
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_map_yle_content_network_timeout(self, mock_urlopen, mock_get_media_url):
        """Test handling of network timeouts."""
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json"

        # Simulate a timeout
        import urllib.error

        mock_urlopen.side_effect = urllib.error.URLError("Timeout")

        with pytest.raises(FileProcessingError):
            map_yle_content("1-50000093")

    @patch("app.yle_utils.CLIENT_ID", "test_client_id")
    @patch("app.yle_utils.CLIENT_KEY", "test_client_key")
    @patch("app.yle_utils.get_media_url")
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_map_yle_content_invalid_response(self, mock_urlopen, mock_get_media_url):
        """Test handling of invalid API response."""
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json"

        # Mock invalid JSON response
        mock_response = MagicMock()
        mock_response.read.return_value = b"invalid json"
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

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
    @patch("app.yle_utils.urllib.request.urlopen")
    def test_full_yle_flow(self, mock_urlopen):
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

        # 2. Mock media playouts API response
        media_response = {"data": [{"url": "https://decrypted.url/media.m3u8"}]}

        # Setup urlopen to return different responses for different calls
        responses = [
            json.dumps(program_response).encode(),
            json.dumps(media_response).encode(),
        ]

        mock_response_objs = []
        for response_data in responses:
            mock_resp = MagicMock()
            mock_resp.read.return_value = response_data
            mock_resp.__enter__.return_value = mock_resp
            mock_resp.__exit__.return_value = None
            mock_response_objs.append(mock_resp)

        mock_urlopen.side_effect = mock_response_objs

        # Execute the full flow
        result = map_yle_content("1-50000093")

        assert result == "https://decrypted.url/media.m3u8"
        assert mock_urlopen.call_count == 2  # Called twice: program info + media URL
