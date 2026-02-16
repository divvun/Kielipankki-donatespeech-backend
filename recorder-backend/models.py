"""
Pydantic models for Kielipankki Recorder schedules and themes.

Uses discriminated unions to handle the polymorphic Item types.
"""

from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field


# ============================================================================
# Schedule Items (Discriminated Union)
# ============================================================================


class AudioMediaItem(BaseModel):
    """Audio media item with direct URL"""

    itemType: Literal["audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to audio file")
    typeId: str = Field(..., description="MIME type (e.g., 'audio/m4a', 'audio/mpeg')")
    description: str
    isRecording: bool


class VideoMediaItem(BaseModel):
    """Video media item with direct URL"""

    itemType: Literal["video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to video file")
    typeId: str = Field(..., description="MIME type (e.g., 'video/mp4', 'video/webm')")
    description: str
    isRecording: bool


class YleAudioMediaItem(BaseModel):
    """YLE audio program item"""

    itemType: Literal["yle-audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    description: str
    isRecording: bool


class YleVideoMediaItem(BaseModel):
    """YLE video program item"""

    itemType: Literal["yle-video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    description: str
    isRecording: bool


class TextContentItem(BaseModel):
    """Text content item"""

    itemType: Literal["text-content"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="URL to text content")
    typeId: Optional[str] = Field(
        None, description="MIME type (e.g., 'text/plain', 'text/html')"
    )
    description: str
    isRecording: bool


class ImageMediaItem(BaseModel):
    """Image media item"""

    itemType: Literal["image"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to image file")
    typeId: str = Field(..., description="MIME type (e.g., 'image/jpeg', 'image/png')")
    description: str
    isRecording: bool


class ChoicePromptItem(BaseModel):
    """Single choice prompt item"""

    itemType: Literal["choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    description: str = Field(..., description="Question text shown to user")
    options: list[str] = Field(..., description="Answer options to choose from")
    isRecording: bool


class MultiChoicePromptItem(BaseModel):
    """Multiple choice prompt item with optional text entry"""

    itemType: Literal["multi-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    description: str = Field(..., description="Question text shown to user")
    options: list[str] = Field(..., description="Multiple answer options")
    isRecording: bool
    otherEntryLabel: Optional[str] = Field(
        None,
        description="Label for text entry field allowing custom answers",
    )


class SuperChoicePromptItem(BaseModel):
    """Super choice prompt item with optional text entry"""

    itemType: Literal["super-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    description: str = Field(..., description="Question text shown to user")
    options: list[str] = Field(..., description="Super choice answer options")
    isRecording: bool
    otherEntryLabel: Optional[str] = Field(
        None,
        description="Label for text entry field allowing custom answers",
    )


class TextInputItem(BaseModel):
    """Text input prompt item"""

    itemType: Literal["text-input"]
    itemId: str = Field(..., description="UUID v4 of the item")
    description: str = Field(..., description="Question text shown to user")
    isRecording: bool


# Discriminated union of all schedule item types (discriminated by itemType)
ScheduleItem = Annotated[
    Union[
        AudioMediaItem,
        VideoMediaItem,
        YleAudioMediaItem,
        YleVideoMediaItem,
        TextContentItem,
        ImageMediaItem,
        ChoicePromptItem,
        MultiChoicePromptItem,
        SuperChoicePromptItem,
        TextInputItem,
    ],
    Field(discriminator="itemType"),
]


# ============================================================================
# Schedule
# ============================================================================


class Schedule(BaseModel):
    """Schedule (playlist) containing items to present to user"""

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


class ScheduleListItem(BaseModel):
    """Single schedule in list response"""

    id: str
    content: Schedule


class ThemeListItem(BaseModel):
    """Single theme in list response"""

    id: str
    content: Theme
