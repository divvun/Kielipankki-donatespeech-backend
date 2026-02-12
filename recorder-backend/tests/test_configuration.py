"""Tests for configuration.py - load_configuration and load_all_configurations endpoints."""

import json
import pytest
from unittest.mock import patch
from conftest import TEST_PLAYLIST_ID, TEST_PLAYLIST_ID_2, TEST_BUCKET_NAME


def test_load_configuration_success(mock_env, lambda_context):
    """Test successful loading of a single playlist configuration."""
    from configuration import load_configuration
    
    event = {
        "pathParameters": {
            "id": TEST_PLAYLIST_ID
        }
    }
    
    response = load_configuration(event, lambda_context)
    
    assert response["statusCode"] == 200
    assert "Access-Control-Allow-Origin" in response["headers"]
    
    body = json.loads(response["body"])
    assert "items" in body
    assert len(body["items"]) > 0
    
    # Verify structure of items
    first_item = body["items"][0]
    assert "itemId" in first_item
    assert "kind" in first_item
    assert "itemType" in first_item


def test_load_configuration_processes_yle_content(mock_env, lambda_context):
    """Test that YLE content URLs are properly processed."""
    from configuration import load_configuration
    
    event = {
        "pathParameters": {
            "id": TEST_PLAYLIST_ID
        }
    }
    
    # Mock the YLE content mapping
    with patch('configuration.map_yle_content') as mock_map:
        mock_map.return_value = "https://mapped-yle-url.com/video.mp4"
        
        response = load_configuration(event, lambda_context)
        
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        
        # Find YLE items and verify they were processed
        yle_items = [item for item in body["items"] if "yle" in item.get("itemType", "")]
        if yle_items:
            # If there are YLE items, the mapping function should have been called
            assert mock_map.called


def test_load_configuration_different_ids(mock_env, lambda_context):
    """Test loading configurations with different IDs."""
    from configuration import load_configuration
    
    for playlist_id in [TEST_PLAYLIST_ID, TEST_PLAYLIST_ID_2]:
        event = {
            "pathParameters": {
                "id": playlist_id
            }
        }
        
        response = load_configuration(event, lambda_context)
        
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "items" in body


def test_load_configuration_nonexistent_id(mock_env, lambda_context):
    """Test loading configuration with non-existent ID."""
    from configuration import load_configuration
    from common import FileProcessingError
    
    event = {
        "pathParameters": {
            "id": "00000000-0000-0000-0000-000000000000"
        }
    }
    
    with pytest.raises(FileProcessingError):
        load_configuration(event, lambda_context)


def test_load_all_configurations_success(mock_env, lambda_context):
    """Test successful loading of all configurations."""
    from configuration import load_all_configurations
    
    event = {}
    
    response = load_all_configurations(event, lambda_context)
    
    assert response["statusCode"] == 200
    assert "Access-Control-Allow-Origin" in response["headers"]
    
    body = json.loads(response["body"])
    assert isinstance(body, list)
    assert len(body) > 0
    
    # Verify structure
    for config in body:
        assert "id" in config
        assert "content" in config
        assert "items" in config["content"]


def test_load_all_configurations_sorted(mock_env, lambda_context):
    """Test that configurations are returned in sorted order by ID."""
    from configuration import load_all_configurations
    
    event = {}
    
    response = load_all_configurations(event, lambda_context)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    
    # Extract IDs
    ids = [config["id"] for config in body]
    
    # Verify sorted
    assert ids == sorted(ids)


def test_load_all_configurations_contains_expected_ids(mock_env, lambda_context):
    """Test that all uploaded test configurations are present."""
    from configuration import load_all_configurations
    
    event = {}
    
    response = load_all_configurations(event, lambda_context)
    
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    
    ids = [config["id"] for config in body]
    
    # Check our test IDs are present
    assert TEST_PLAYLIST_ID in ids
    assert TEST_PLAYLIST_ID_2 in ids


def test_load_all_configurations_processes_yle_content(mock_env, lambda_context):
    """Test that YLE content is processed for all configurations."""
    from configuration import load_all_configurations
    
    event = {}
    
    with patch('configuration.map_yle_content') as mock_map:
        mock_map.return_value = "https://mapped-yle-url.com/video.mp4"
        
        response = load_all_configurations(event, lambda_context)
        
        assert response["statusCode"] == 200


def test_pre_process_configuration_file_yle_video(mock_env, lambda_context):
    """Test pre-processing of configuration with YLE video content."""
    from configuration import pre_process_configuration_file
    
    content = {
        "items": [
            {
                "itemId": "test-id",
                "itemType": "yle-video",
                "url": "1-50000093"
            }
        ]
    }
    
    with patch('configuration.map_yle_content') as mock_map:
        mock_map.return_value = "https://mapped-url.com/video.mp4"
        
        pre_process_configuration_file(content)
        
        # Verify the URL was replaced
        assert content["items"][0]["url"] == "https://mapped-url.com/video.mp4"
        mock_map.assert_called_once_with("1-50000093")


def test_pre_process_configuration_file_yle_audio(mock_env, lambda_context):
    """Test pre-processing of configuration with YLE audio content."""
    from configuration import pre_process_configuration_file
    
    content = {
        "items": [
            {
                "itemId": "test-id",
                "itemType": "yle-audio",
                "url": "1-40000123"
            }
        ]
    }
    
    with patch('configuration.map_yle_content') as mock_map:
        mock_map.return_value = "https://mapped-url.com/audio.mp3"
        
        pre_process_configuration_file(content)
        
        # Verify the URL was replaced
        assert content["items"][0]["url"] == "https://mapped-url.com/audio.mp3"
        mock_map.assert_called_once_with("1-40000123")


def test_pre_process_configuration_file_non_yle_content(mock_env, lambda_context):
    """Test that non-YLE content URLs are not modified."""
    from configuration import pre_process_configuration_file
    
    original_url = "https://example.com/video.mp4"
    content = {
        "items": [
            {
                "itemId": "test-id",
                "itemType": "video",
                "url": original_url
            }
        ]
    }
    
    with patch('configuration.map_yle_content') as mock_map:
        pre_process_configuration_file(content)
        
        # Verify the URL was NOT changed
        assert content["items"][0]["url"] == original_url
        # And mapping function was NOT called
        mock_map.assert_not_called()


def test_load_s3_conf_file_success(mock_env, lambda_context):
    """Test loading S3 configuration file."""
    from configuration import load_s3_conf_file
    
    conf_dict = load_s3_conf_file(f"configuration/{TEST_PLAYLIST_ID}.json")
    
    assert "items" in conf_dict
    assert len(conf_dict["items"]) > 0
