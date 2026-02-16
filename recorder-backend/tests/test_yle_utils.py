"""Tests for yle_utils module - YLE API integration and decryption."""

import json
import base64
from unittest.mock import patch, MagicMock
import pytest

from yle_utils import (
    map_yle_content,
    decrypt_yle_url,
    get_media_url,
    FileProcessingError,
)


class TestDecryptYleUrl:
    """Test YLE URL decryption function."""

    @patch("yle_utils.YLE_DECRYPT", b"0123456789abcdef")  # 16-byte key for AES
    def test_decrypt_yle_url_success(self):
        """Test successful decryption of YLE URL."""
        # This is a simplified test - in reality, you'd need a properly encrypted URL
        # For this test, we'll mock the entire AES decryption process
        
        # Create a mock encrypted URL (base64 encoded IV + message)
        iv = b"1234567890123456"  # 16 bytes
        encrypted_msg = b"encrypted_content_here_padded_to_16_multiple!!!"
        
        # Combine IV and encrypted message, then base64 encode
        combined = iv + encrypted_msg
        crypted_url = base64.b64encode(combined).decode()
        
        with patch("yle_utils.AES") as mock_aes:
            # Mock the AES cipher
            mock_cipher = MagicMock()
            mock_cipher.decrypt.return_value = b"https://yle.example.com/media.m3u8    "
            mock_aes.new.return_value = mock_cipher
            
            result = decrypt_yle_url(crypted_url)
            
            assert result == "https://yle.example.com/media.m3u8"
            mock_aes.new.assert_called_once()


class TestGetMediaUrl:
    """Test YLE media URL retrieval."""

    @patch("yle_utils.CLIENT_ID", "test_client_id")
    @patch("yle_utils.CLIENT_KEY", "test_client_key")
    @patch("yle_utils.urllib.request.urlopen")
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
        assert "media_id=test-media-id-123" in result
        assert "app_id=test_client_id" in result
        assert "app_key=test_client_key" in result
        assert "protocol=HLS" in result

    @patch("yle_utils.CLIENT_ID", "test_client_id")
    @patch("yle_utils.CLIENT_KEY", "test_client_key")
    @patch("yle_utils.urllib.request.urlopen")
    def test_get_media_url_no_current_publication(self, mock_urlopen):
        """Test handling when no current publication event exists."""
        # Mock response with no "currently" status
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
        
        # Should raise StopIteration when no current publication found
        with pytest.raises(StopIteration):
            get_media_url("1-50000093")


class TestMapYleContent:
    """Test main YLE content mapping function."""

    @patch("yle_utils.decrypt_yle_url")
    @patch("yle_utils.get_media_url")
    @patch("yle_utils.urllib.request.urlopen")
    def test_map_yle_content_success(
        self, mock_urlopen, mock_get_media_url, mock_decrypt
    ):
        """Test successful mapping of YLE program ID to decrypted URL."""
        # Mock get_media_url to return a URL
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json?..."
        
        # Mock the media playouts API response
        media_response = {
            "data": [{"url": "base64_encrypted_url_here"}]
        }
        
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(media_response).encode()
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response
        
        # Mock decryption
        mock_decrypt.return_value = "https://yle-vod.akamaized.net/media.m3u8"
        
        result = map_yle_content("1-50000093")
        
        assert result == "https://yle-vod.akamaized.net/media.m3u8"
        mock_get_media_url.assert_called_once_with("1-50000093")
        mock_decrypt.assert_called_once_with("base64_encrypted_url_here")

    @patch("yle_utils.get_media_url")
    def test_map_yle_content_error_handling(self, mock_get_media_url):
        """Test error handling when YLE API fails."""
        # Mock get_media_url to raise an exception
        mock_get_media_url.side_effect = Exception("API Error")
        
        with pytest.raises(FileProcessingError):
            map_yle_content("1-50000093")

    @patch("yle_utils.decrypt_yle_url")
    @patch("yle_utils.get_media_url")
    @patch("yle_utils.urllib.request.urlopen")
    def test_map_yle_content_network_timeout(
        self, mock_urlopen, mock_get_media_url, mock_decrypt
    ):
        """Test handling of network timeouts."""
        mock_get_media_url.return_value = "https://api.yle.fi/media/playouts.json"
        
        # Simulate a timeout
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Timeout")
        
        with pytest.raises(FileProcessingError):
            map_yle_content("1-50000093")

    @patch("yle_utils.decrypt_yle_url")
    @patch("yle_utils.get_media_url")
    @patch("yle_utils.urllib.request.urlopen")
    def test_map_yle_content_invalid_response(
        self, mock_urlopen, mock_get_media_url, mock_decrypt
    ):
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


class TestYleIntegration:
    """Integration tests for YLE utilities (require mocking full flow)."""

    @patch("yle_utils.CLIENT_ID", "test_id")
    @patch("yle_utils.CLIENT_KEY", "test_key")
    @patch("yle_utils.YLE_DECRYPT", b"0123456789abcdef")
    @patch("yle_utils.urllib.request.urlopen")
    @patch("yle_utils.AES")
    def test_full_yle_flow(self, mock_aes, mock_urlopen):
        """Test complete flow from program ID to decrypted URL."""
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
        media_response = {
            "data": [{"url": base64.b64encode(b"0" * 32).decode()}]
        }
        
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
        
        # 3. Mock AES decryption
        mock_cipher = MagicMock()
        mock_cipher.decrypt.return_value = b"https://decrypted.url/media.m3u8      "
        mock_aes.new.return_value = mock_cipher
        
        # Execute the full flow
        result = map_yle_content("1-50000093")
        
        assert result == "https://decrypted.url/media.m3u8"
        assert mock_urlopen.call_count == 2  # Called twice: program info + media URL
