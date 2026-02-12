"""Pytest configuration and fixtures for API testing with mocked AWS S3."""

import json
import os
import pytest
from moto import mock_aws
import boto3


# Test data UUIDs
TEST_PLAYLIST_ID = "27103f9e-2b03-48d0-b442-f38a6052cfe1"
TEST_PLAYLIST_ID_2 = "0b5cf885-5049-4e7a-83e0-05a63be53639"
TEST_THEME_ID = "143a9f19-edda-40c5-9213-3c0615c7dcf0"
TEST_THEME_ID_2 = "550e8400-e29b-41d4-a716-446655440000"
TEST_BUCKET_NAME = "recorder-test-bucket"
TEST_CLIENT_ID = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mock AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"


@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    """Create a mocked S3 client."""
    with mock_aws():
        conn = boto3.client("s3", region_name="eu-west-1")
        yield conn


@pytest.fixture(scope="function")
def mock_s3_bucket(s3_client):
    """Create a mock S3 bucket with test data."""
    # Create the bucket
    s3_client.create_bucket(
        Bucket=TEST_BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"}
    )
    
    # Load test playlist data
    with open("test/playlist.json", "r") as f:
        playlist_data = json.load(f)
    
    # Load test theme data
    with open("test/theme.json", "r") as f:
        theme_data = json.load(f)
    
    # Upload playlist configurations
    s3_client.put_object(
        Bucket=TEST_BUCKET_NAME,
        Key=f"configuration/{TEST_PLAYLIST_ID}.json",
        Body=json.dumps(playlist_data)
    )
    
    s3_client.put_object(
        Bucket=TEST_BUCKET_NAME,
        Key=f"configuration/{TEST_PLAYLIST_ID_2}.json",
        Body=json.dumps(playlist_data)
    )
    
    # Upload theme files
    s3_client.put_object(
        Bucket=TEST_BUCKET_NAME,
        Key=f"theme/{TEST_THEME_ID}.json",
        Body=json.dumps(theme_data)
    )
    
    s3_client.put_object(
        Bucket=TEST_BUCKET_NAME,
        Key=f"theme/{TEST_THEME_ID_2}.json",
        Body=json.dumps(theme_data)
    )
    
    yield s3_client


@pytest.fixture(scope="function")
def mock_env(mock_s3_bucket):
    """Set up environment variables for testing."""
    os.environ["CONTENT_BUCKET_NAME"] = TEST_BUCKET_NAME
    os.environ["YLE_CLIENT_ID"] = "test-client-id"
    os.environ["YLE_CLIENT_KEY"] = "test-client-key"
    os.environ["YLE_DECRYPT"] = "false"
    
    yield
    
    # Cleanup
    for key in ["CONTENT_BUCKET_NAME", "YLE_CLIENT_ID", "YLE_CLIENT_KEY", "YLE_DECRYPT"]:
        if key in os.environ:
            del os.environ[key]


@pytest.fixture
def lambda_context():
    """Mock Lambda context object."""
    class LambdaContext:
        def __init__(self):
            self.function_name = "test-function"
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = "arn:aws:lambda:eu-west-1:123456789012:function:test-function"
            self.aws_request_id = "test-request-id"
    
    return LambdaContext()
