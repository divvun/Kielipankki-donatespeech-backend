"""
Tests for upload and recording management endpoints.

Tests cover:
- POST /v1/upload - Upload initialization with validation
- DELETE /v1/recordings/{client_id} - Delete all client recordings
- DELETE /v1/recordings/{client_id}/{session_id} - Delete session recordings
- DELETE /v1/recordings/{client_id}/{session_id}/{recording_id} - Delete specific recording
"""

import pytest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport

from main import app
from storage import StorageError

# Configure anyio for pytest
pytestmark = pytest.mark.anyio


# Test fixtures


@pytest.fixture
def valid_client_id():
    """Valid UUID v4 client ID."""
    return "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture
def valid_session_id():
    """Valid UUID v4 session ID."""
    return "7c9e6679-7425-40de-944b-e07fc1f90ae7"


@pytest.fixture
def valid_recording_id():
    """Valid UUID v4 recording ID."""
    return "3fa85f64-5717-4562-b3fc-2c963f66afa6"


@pytest.fixture
def valid_upload_request(valid_client_id):
    """Valid upload request payload."""
    return {
        "filename": "test-recording.m4a",
        "metadata": {
            "clientId": valid_client_id,
            "contentType": "audio/m4a",
        },
    }


@pytest.fixture
def valid_upload_request_with_session(valid_client_id, valid_session_id):
    """Valid upload request with session ID."""
    return {
        "filename": "test-recording.m4a",
        "metadata": {
            "clientId": valid_client_id,
            "sessionId": valid_session_id,
            "contentType": "audio/m4a",
        },
    }


# POST /v1/upload tests


class TestInitUpload:
    """Tests for POST /v1/upload endpoint."""

    
    @patch("main.generate_upload_sas_url")
    @patch("main.store_metadata")
    async def test_init_upload_success(
        self, mock_store_metadata, mock_generate_sas, valid_upload_request
    ):
        """Test successful upload initialization."""
        mock_store_metadata.return_value = None
        mock_generate_sas.return_value = "https://storage.blob.core.windows.net/test?sas=token"

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=valid_upload_request)

        assert response.status_code == 200
        assert "presignedUrl" in response.json()
        assert response.json()["presignedUrl"].startswith("https://")
        mock_store_metadata.assert_called_once()
        mock_generate_sas.assert_called_once()

    
    @patch("main.generate_upload_sas_url")
    @patch("main.store_metadata")
    async def test_init_upload_with_session_id(
        self,
        mock_store_metadata,
        mock_generate_sas,
        valid_upload_request_with_session,
    ):
        """Test upload initialization with session ID."""
        mock_store_metadata.return_value = None
        mock_generate_sas.return_value = "https://storage.blob.core.windows.net/test?sas=token"

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/v1/upload", json=valid_upload_request_with_session
            )

        assert response.status_code == 200
        # Verify session ID is included in the metadata blob path
        call_args = mock_store_metadata.call_args[0]
        metadata_blob_name = call_args[0]
        assert valid_upload_request_with_session["metadata"]["sessionId"] in metadata_blob_name

    
    async def test_init_upload_invalid_filename_empty(self, valid_client_id):
        """Test upload with empty filename."""
        request = {
            "filename": "",
            "metadata": {"clientId": valid_client_id, "contentType": "audio/m4a"},
        }

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=request)

        assert response.status_code == 400
        assert "Invalid filename" in response.json()["detail"]

    
    async def test_init_upload_invalid_filename_no_extension(self, valid_client_id):
        """Test upload with filename without extension."""
        request = {
            "filename": "testfile",
            "metadata": {"clientId": valid_client_id, "contentType": "audio/m4a"},
        }

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=request)

        assert response.status_code == 400
        assert "Invalid filename" in response.json()["detail"]

    
    async def test_init_upload_invalid_filename_with_slash(self, valid_client_id):
        """Test upload with filename containing slash."""
        request = {
            "filename": "../evil.m4a",
            "metadata": {"clientId": valid_client_id, "contentType": "audio/m4a"},
        }

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=request)

        assert response.status_code == 400
        assert "Invalid filename" in response.json()["detail"]

    
    async def test_init_upload_invalid_file_extension(self, valid_client_id):
        """Test upload with disallowed file extension."""
        request = {
            "filename": "test.mp3",
            "metadata": {"clientId": valid_client_id, "contentType": "audio/mp3"},
        }

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=request)

        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"]

    
    async def test_init_upload_allowed_extensions(self, valid_client_id):
        """Test all allowed file extensions."""
        allowed_extensions = ["m4a", "flac", "amr", "wav", "opus", "caf"]

        for ext in allowed_extensions:
            request = {
                "filename": f"test.{ext}",
                "metadata": {"clientId": valid_client_id, "contentType": f"audio/{ext}"},
            }

            with patch("main.store_metadata"), patch("main.generate_upload_sas_url") as mock_sas:
                mock_sas.return_value = "https://storage.blob.core.windows.net/test?sas=token"
                transport = ASGITransport(app=app)
                async with AsyncClient(transport=transport, base_url="http://test") as client:
                    response = await client.post("/v1/upload", json=request)

                assert response.status_code == 200, f"Extension {ext} should be allowed"

    
    async def test_init_upload_invalid_client_id(self):
        """Test upload with invalid client ID."""
        request = {
            "filename": "test.m4a",
            "metadata": {"clientId": "not-a-uuid", "contentType": "audio/m4a"},
        }

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=request)

        assert response.status_code == 400
        assert "clientId" in response.json()["detail"]

    
    async def test_init_upload_invalid_session_id(self, valid_client_id):
        """Test upload with invalid session ID."""
        request = {
            "filename": "test.m4a",
            "metadata": {
                "clientId": valid_client_id,
                "sessionId": "not-a-uuid",
                "contentType": "audio/m4a",
            },
        }

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=request)

        assert response.status_code == 400
        assert "sessionId" in response.json()["detail"]

    
    @patch("main.store_metadata")
    async def test_init_upload_storage_error_metadata(
        self, mock_store_metadata, valid_upload_request
    ):
        """Test upload when metadata storage fails."""
        mock_store_metadata.side_effect = StorageError("Storage failed")

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=valid_upload_request)

        assert response.status_code == 500
        assert "Error storing metadata" in response.json()["detail"]

    
    @patch("main.generate_upload_sas_url")
    @patch("main.store_metadata")
    async def test_init_upload_storage_error_sas(
        self, mock_store_metadata, mock_generate_sas, valid_upload_request
    ):
        """Test upload when SAS URL generation fails."""
        mock_store_metadata.return_value = None
        mock_generate_sas.side_effect = StorageError("SAS generation failed")

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/v1/upload", json=valid_upload_request)

        assert response.status_code == 500
        assert "Error generating upload URL" in response.json()["detail"]


# DELETE /v1/recordings tests


class TestDeleteRecordings:
    """Tests for DELETE /v1/recordings endpoints."""

    
    @patch("main.delete_by_prefix")
    async def test_delete_by_client_id_success(
        self, mock_delete, valid_client_id
    ):
        """Test successful deletion by client ID."""
        mock_delete.return_value = None

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(f"/v1/recordings/{valid_client_id}")

        assert response.status_code == 200
        assert "Deleted all data for client" in response.json()["message"]
        mock_delete.assert_called_once()
        call_args = mock_delete.call_args[0][0]
        assert valid_client_id in call_args

    
    async def test_delete_by_client_id_invalid_uuid(self):
        """Test deletion with invalid client ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete("/v1/recordings/not-a-uuid")

        assert response.status_code == 400
        assert "Invalid clientId" in response.json()["detail"]

    
    @patch("main.delete_by_prefix")
    async def test_delete_by_client_id_storage_error(
        self, mock_delete, valid_client_id
    ):
        """Test deletion when storage error occurs."""
        mock_delete.side_effect = StorageError("Delete failed")

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(f"/v1/recordings/{valid_client_id}")

        assert response.status_code == 500
        assert "Error deleting data" in response.json()["detail"]

    
    @patch("main.delete_by_prefix")
    async def test_delete_by_session_id_success(
        self, mock_delete, valid_client_id, valid_session_id
    ):
        """Test successful deletion by session ID."""
        mock_delete.return_value = None

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/{valid_client_id}/{valid_session_id}"
            )

        assert response.status_code == 200
        assert "Deleted all data for session" in response.json()["message"]
        call_args = mock_delete.call_args[0][0]
        assert valid_client_id in call_args
        assert valid_session_id in call_args

    
    async def test_delete_by_session_id_invalid_client_id(self, valid_session_id):
        """Test deletion with invalid client ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/not-a-uuid/{valid_session_id}"
            )

        assert response.status_code == 400
        assert "Invalid clientId or sessionId" in response.json()["detail"]

    
    async def test_delete_by_session_id_invalid_session_id(self, valid_client_id):
        """Test deletion with invalid session ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/{valid_client_id}/not-a-uuid"
            )

        assert response.status_code == 400
        assert "Invalid clientId or sessionId" in response.json()["detail"]

    
    @patch("main.delete_by_prefix")
    async def test_delete_by_session_id_storage_error(
        self, mock_delete, valid_client_id, valid_session_id
    ):
        """Test deletion by session when storage error occurs."""
        mock_delete.side_effect = StorageError("Delete failed")

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/{valid_client_id}/{valid_session_id}"
            )

        assert response.status_code == 500
        assert "Error deleting data" in response.json()["detail"]

    
    @patch("main.delete_by_prefix")
    async def test_delete_by_recording_id_success(
        self, mock_delete, valid_client_id, valid_session_id, valid_recording_id
    ):
        """Test successful deletion by recording ID."""
        mock_delete.return_value = None

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/{valid_client_id}/{valid_session_id}/{valid_recording_id}"
            )

        assert response.status_code == 200
        assert "Deleted recording" in response.json()["message"]
        call_args = mock_delete.call_args[0][0]
        assert valid_client_id in call_args
        assert valid_session_id in call_args
        assert valid_recording_id in call_args

    
    async def test_delete_by_recording_id_invalid_client_id(
        self, valid_session_id, valid_recording_id
    ):
        """Test deletion with invalid client ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/not-a-uuid/{valid_session_id}/{valid_recording_id}"
            )

        assert response.status_code == 400
        assert "Invalid" in response.json()["detail"]

    
    async def test_delete_by_recording_id_invalid_session_id(
        self, valid_client_id, valid_recording_id
    ):
        """Test deletion with invalid session ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/{valid_client_id}/not-a-uuid/{valid_recording_id}"
            )

        assert response.status_code == 400
        assert "Invalid" in response.json()["detail"]

    
    async def test_delete_by_recording_id_invalid_recording_id(
        self, valid_client_id, valid_session_id
    ):
        """Test deletion with invalid recording ID."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/{valid_client_id}/{valid_session_id}/not-a-uuid"
            )

        assert response.status_code == 400
        assert "Invalid" in response.json()["detail"]

    
    @patch("main.delete_by_prefix")
    async def test_delete_by_recording_id_storage_error(
        self, mock_delete, valid_client_id, valid_session_id, valid_recording_id
    ):
        """Test deletion by recording when storage error occurs."""
        mock_delete.side_effect = StorageError("Delete failed")

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                f"/v1/recordings/{valid_client_id}/{valid_session_id}/{valid_recording_id}"
            )

        assert response.status_code == 500
        assert "Error deleting recording" in response.json()["detail"]
