"""
Pydantic models for Kielipankki Recorder schedules and configurations.

Uses discriminated unions to handle the polymorphic Item types.
"""

from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field


# ============================================================================
# Schedule Items (Discriminated Union)
# ============================================================================


class AudioMediaItem(BaseModel):
    """Audio media item with direct URL"""

    kind: Literal["media"]
    itemType: Literal["audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to audio file")
    typeId: str = Field(..., description="MIME type (e.g., 'audio/m4a', 'audio/mpeg')")
    description: str
    options: list[str] = Field(default_factory=list, description="Should be empty for media")
    isRecording: bool


class VideoMediaItem(BaseModel):
    """Video media item with direct URL"""

    kind: Literal["media"]
    itemType: Literal["video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to video file")
    typeId: str = Field(..., description="MIME type (e.g., 'video/mp4', 'video/webm')")
    description: str
    options: list[str] = Field(default_factory=list, description="Should be empty for media")
    isRecording: bool


class YleAudioMediaItem(BaseModel):
    """YLE audio program item"""

    kind: Literal["media"]
    itemType: Literal["yle-audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="Not used for YLE content")
    description: str
    options: list[str] = Field(default_factory=list, description="Should be empty for media")
    isRecording: bool


class YleVideoMediaItem(BaseModel):
    """YLE video program item"""

    kind: Literal["media"]
    itemType: Literal["yle-video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="Not used for YLE content")
    description: str
    options: list[str] = Field(default_factory=list, description="Should be empty for media")
    isRecording: bool


class TextMediaItem(BaseModel):
    """Text content item"""

    kind: Literal["media"]
    itemType: Literal["text"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="URL to text content")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'text/plain', 'text/html')")
    description: str
    options: list[str] = Field(default_factory=list, description="Should be empty for media")
    isRecording: bool


class ImageMediaItem(BaseModel):
    """Image media item"""

    kind: Literal["media"]
    itemType: Literal["image"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to image file")
    typeId: str = Field(..., description="MIME type (e.g., 'image/jpeg', 'image/png')")
    description: str
    options: list[str] = Field(default_factory=list, description="Should be empty for media")
    isRecording: bool


# Union of all media item types (discriminated by itemType)
MediaItem = Annotated[
    Union[
        AudioMediaItem,
        VideoMediaItem,
        YleAudioMediaItem,
        YleVideoMediaItem,
        TextMediaItem,
        ImageMediaItem,
    ],
    Field(discriminator="itemType"),
]


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


# Discriminated union of schedule items (discriminated by kind: media vs prompt)
ScheduleItem = Annotated[
    Union[MediaItem, PromptItem],
    Field(discriminator="kind"),
]


# ============================================================================
# Configuration (Schedule)
# ============================================================================


class Configuration(BaseModel):
    """Configuration/Schedule with items"""

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
