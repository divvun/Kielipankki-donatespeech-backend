"""
Pydantic models for Kielipankki Recorder schedules and configurations.

Uses discriminated unions to handle the polymorphic Item types.
"""

from typing import Literal, Optional, Union
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Schedule Items (Discriminated Union)
# ============================================================================


class MediaItem(BaseModel):
    """Media schedule item (video, audio, images, etc.)"""

    kind: Literal["media"]
    itemId: str = Field(..., description="UUID v4 of the item")
    itemType: Literal["audio", "video", "yle-audio", "yle-video", "text", "image"]
    typeId: Optional[str] = Field(
        None, description="MIME type (e.g., 'audio/m4a', 'video/mp4', 'image/jpeg')"
    )
    url: str = Field(..., description="URL or YLE program ID")
    description: str
    options: list[str] = Field(default_factory=list, description="Should be empty for media")
    isRecording: bool


class PromptItem(BaseModel):
    """Prompt/question schedule item for user input"""

    kind: Literal["prompt"]
    itemId: str = Field(..., description="UUID v4 of the item")
    itemType: Literal["choice", "multi-choice", "super-choice", "text"]
    typeId: None = Field(None, description="Always null for prompts")
    url: None = Field(None, description="Always null for prompts")
    description: str = Field(..., description="Question text shown to user")
    options: list[str] = Field(
        default_factory=list,
        description="Answer options (required for choice/multi-choice/super-choice)",
    )
    isRecording: bool
    otherEntryLabel: Optional[str] = Field(
        None,
        description="Label for text entry field (required for multi-choice/super-choice)",
    )


# Discriminated union of schedule items
ScheduleItem = Union[MediaItem, PromptItem]


# ============================================================================
# Configuration (Schedule)
# ============================================================================


class Configuration(BaseModel):
    """Configuration/Schedule with items"""

    model_config = ConfigDict(discriminator="kind")

    id: Optional[str] = None  # Will be set from filename
    scheduleId: Optional[str] = None
    description: str
    items: list[ScheduleItem]


# ============================================================================
# Theme
# ============================================================================


class Theme(BaseModel):
    """Theme containing multiple schedule IDs"""

    id: Optional[str] = None  # Will be set from filename
    description: str
    image: Optional[str] = None
    scheduleIds: list[str] = Field(default_factory=list)


# ============================================================================
# Upload and Metadata
# ============================================================================


class UploadMetadata(BaseModel):
    """Metadata associated with an upload"""

    clientId: str = Field(..., description="UUID v4 client identifier")
    sessionId: Optional[str] = Field(None, description="UUID v4 session identifier")
    recordingId: Optional[str] = Field(None, description="UUID v4 recording identifier")
    contentType: Optional[str] = Field(None, description="MIME type of the audio file")
    timestamp: Optional[str] = None
    duration: Optional[float] = None
    language: Optional[str] = None
    # Other metadata fields accepted as-is


class InitUploadRequest(BaseModel):
    """Request body for initializing an upload"""

    filename: str = Field(..., description="Name of the audio file to upload")
    metadata: UploadMetadata


class InitUploadResponse(BaseModel):
    """Response containing the SAS URL for direct upload"""

    presignedUrl: str


# ============================================================================
# API Response Wrappers
# ============================================================================


class ConfigurationListItem(BaseModel):
    """Single configuration in list response"""

    id: str
    content: Configuration


class ThemeListItem(BaseModel):
    """Single theme in list response"""

    id: str
    content: Theme
