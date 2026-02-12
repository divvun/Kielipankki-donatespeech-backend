"""Tests for handler.py - init_upload and delete_stored_client_data endpoints."""

import json
from tests.conftest import TEST_BUCKET_NAME, TEST_CLIENT_ID


def test_init_upload_success(mock_env, lambda_context):
    """Test successful initialization of upload with valid metadata."""
    from handler import init_upload

    event = {
        "body": json.dumps(
            {
                "filename": "test_audio.m4a",
                "metadata": {
                    "clientId": TEST_CLIENT_ID,
                    "sessionId": "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e",
                    "language": "en",
                },
            }
        )
    }

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "presignedUrl" in body
    assert "https://" in body["presignedUrl"]
    assert "test_audio.m4a" in body["presignedUrl"]


def test_init_upload_no_body(mock_env, lambda_context):
    """Test init_upload with missing body."""
    from handler import init_upload

    event = {}

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["error"] == "Bad request parameters"
    assert "No body found" in body["additionalInfo"]


def test_init_upload_invalid_json(mock_env, lambda_context):
    """Test init_upload with invalid JSON in body."""
    from handler import init_upload

    event = {"body": "not valid json"}

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "Error decoding body content" in body["additionalInfo"]


def test_init_upload_missing_filename(mock_env, lambda_context):
    """Test init_upload without filename."""
    from handler import init_upload

    event = {"body": json.dumps({"metadata": {"clientId": TEST_CLIENT_ID}})}

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "filename" in body["additionalInfo"].lower()


def test_init_upload_invalid_filename_no_extension(mock_env, lambda_context):
    """Test init_upload with filename without extension."""
    from handler import init_upload

    event = {
        "body": json.dumps(
            {"filename": "audiofile", "metadata": {"clientId": TEST_CLIENT_ID}}
        )
    }

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400


def test_init_upload_invalid_filename_with_slash(mock_env, lambda_context):
    """Test init_upload with filename containing slash."""
    from handler import init_upload

    event = {
        "body": json.dumps(
            {"filename": "path/to/audio.m4a", "metadata": {"clientId": TEST_CLIENT_ID}}
        )
    }

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400


def test_init_upload_invalid_file_extension(mock_env, lambda_context):
    """Test init_upload with unsupported file extension."""
    from handler import init_upload

    event = {
        "body": json.dumps(
            {"filename": "audio.mp3", "metadata": {"clientId": TEST_CLIENT_ID}}
        )
    }

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "suffix" in body["additionalInfo"].lower()


def test_init_upload_valid_extensions(mock_env, lambda_context):
    """Test init_upload with all valid file extensions."""
    from handler import init_upload

    valid_extensions = ["m4a", "flac", "amr", "wav", "opus", "caf"]

    for ext in valid_extensions:
        event = {
            "body": json.dumps(
                {"filename": f"test.{ext}", "metadata": {"clientId": TEST_CLIENT_ID}}
            )
        }

        response = init_upload(event, lambda_context)

        assert response["statusCode"] == 200, f"Extension {ext} should be valid"


def test_init_upload_missing_metadata(mock_env, lambda_context):
    """Test init_upload without metadata."""
    from handler import init_upload

    event = {"body": json.dumps({"filename": "test.m4a"})}

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "metadata" in body["additionalInfo"].lower()


def test_init_upload_missing_client_id(mock_env, lambda_context):
    """Test init_upload without clientId in metadata."""
    from handler import init_upload

    event = {
        "body": json.dumps({"filename": "test.m4a", "metadata": {"language": "en"}})
    }

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "clientId" in body["additionalInfo"]


def test_init_upload_invalid_client_id(mock_env, lambda_context):
    """Test init_upload with invalid UUID for clientId."""
    from handler import init_upload

    event = {
        "body": json.dumps(
            {"filename": "test.m4a", "metadata": {"clientId": "not-a-valid-uuid"}}
        )
    }

    response = init_upload(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "clientId" in body["additionalInfo"]


def test_delete_client_data_success(mock_env, lambda_context):
    """Test successful deletion of client data."""
    from handler import delete_stored_client_data

    # First upload some test data
    from handler import s3_client

    s3_client.put_object(
        Bucket=TEST_BUCKET_NAME,
        Key=f"uploads/audio_and_metadata/{TEST_CLIENT_ID}/test.json",
        Body=json.dumps({"test": "data"}),
    )

    event = {"pathParameters": {"id": TEST_CLIENT_ID}, "queryStringParameters": None}

    response = delete_stored_client_data(event, lambda_context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["delete"] == "ok"


def test_delete_client_data_invalid_client_id(mock_env, lambda_context):
    """Test deletion with invalid client ID."""
    from handler import delete_stored_client_data

    event = {"pathParameters": {"id": "invalid-uuid"}, "queryStringParameters": None}

    response = delete_stored_client_data(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "clientId" in body["additionalInfo"]


def test_delete_client_data_with_session_id(mock_env, lambda_context):
    """Test deletion with session_id query parameter."""
    from handler import delete_stored_client_data

    session_id = "c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f"

    event = {
        "pathParameters": {"id": TEST_CLIENT_ID},
        "queryStringParameters": {"session_id": session_id},
    }

    response = delete_stored_client_data(event, lambda_context)

    assert response["statusCode"] == 200


def test_delete_client_data_with_recording_id(mock_env, lambda_context):
    """Test deletion with recording_id query parameter."""
    from handler import delete_stored_client_data

    recording_id = "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a"

    event = {
        "pathParameters": {"id": TEST_CLIENT_ID},
        "queryStringParameters": {"recording_id": recording_id},
    }

    response = delete_stored_client_data(event, lambda_context)

    assert response["statusCode"] == 200


def test_delete_client_data_invalid_session_id(mock_env, lambda_context):
    """Test deletion with invalid session_id."""
    from handler import delete_stored_client_data

    event = {
        "pathParameters": {"id": TEST_CLIENT_ID},
        "queryStringParameters": {"session_id": "invalid-uuid"},
    }

    response = delete_stored_client_data(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "SessionId" in body["additionalInfo"]


def test_delete_client_data_invalid_recording_id(mock_env, lambda_context):
    """Test deletion with invalid recording_id."""
    from handler import delete_stored_client_data

    event = {
        "pathParameters": {"id": TEST_CLIENT_ID},
        "queryStringParameters": {"recording_id": "invalid-uuid"},
    }

    response = delete_stored_client_data(event, lambda_context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "RecordingId" in body["additionalInfo"]
