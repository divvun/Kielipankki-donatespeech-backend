"""Shared pytest fixtures for models and API testing."""

import pytest
from models import MediaItem, PromptItem, Configuration, Theme


@pytest.fixture
def media_item_audio():
    """MediaItem with kind=media and itemType=audio."""
    return MediaItem(
        kind="media",
        itemId="ce3c6012-25f0-4c69-a0ad-c5dc8e41b795",
        itemType="audio",
        typeId="audio/m4a",
        url="https://example.com/audio.m4a",
        description="Audio description",
        options=[],
        isRecording=True,
    )


@pytest.fixture
def prompt_item_choice():
    """PromptItem with kind=prompt and itemType=choice."""
    return PromptItem(
        kind="prompt",
        itemId="f6267df5-ed1c-4ebf-870d-fcb823f66664",
        itemType="choice",
        typeId=None,
        url=None,
        description="Choose one option",
        options=["Option 1", "Option 2", "Option 3"],
        isRecording=False,
    )

