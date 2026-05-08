"""
Pydantic models for Kielipankki Recorder schedules and themes.

Uses discriminated unions to handle the polymorphic Item types.
"""

from typing import Literal, Union, Optional
from pydantic import BaseModel, Field


# ============================================================================
# Nested structures for media items
# ============================================================================


class MediaState(BaseModel):
    """State information displayed during media playback/recording"""

    title: str = Field(..., description="Localized title")
    body1: str = Field(..., description="Localized body text 1")
    body2: str = Field(..., description="Localized body text 2")
    url: Optional[str] = Field(None, description="Optional URL for this state")


# ============================================================================
# Schedule Items (Discriminated Union)
# ============================================================================


class AudioMediaItem(BaseModel):
    """Audio media item with direct URL"""

    kind: Literal["media"]
    itemType: Literal["audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(
        None, description="MIME type (e.g., 'audio/m4a', 'audio/mpeg')"
    )
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before recording starts"
    )
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(
        None, description="State after recording finishes"
    )


class VideoMediaItem(BaseModel):
    """Video media item with direct URL"""

    kind: Literal["media"]
    itemType: Literal["video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(
        None, description="MIME type (e.g., 'video/mp4', 'video/webm')"
    )
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before recording starts"
    )
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(
        None, description="State after recording finishes"
    )


class YleAudioMediaItem(BaseModel):
    """YLE audio program item"""

    kind: Literal["media"]
    itemType: Literal["yle-audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(None, description="MIME type")
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before recording starts"
    )
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(
        None, description="State after recording finishes"
    )


class YleVideoMediaItem(BaseModel):
    """YLE video program item"""

    kind: Literal["media"]
    itemType: Literal["yle-video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(None, description="MIME type")
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before recording starts"
    )
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(
        None, description="State after recording finishes"
    )


class TextContentItem(BaseModel):
    """Text content item"""

    kind: Literal["media"]
    itemType: Literal["text-content"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(
        None, description="MIME type (e.g., 'text/plain', 'text/html')"
    )
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before recording starts"
    )
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(
        None, description="State after recording finishes"
    )


class ImageMediaItem(BaseModel):
    """Image media item"""

    kind: Literal["media"]
    itemType: Literal["image"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(
        None, description="MIME type (e.g., 'image/jpeg', 'image/png')"
    )
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before recording starts"
    )
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(
        None, description="State after recording finishes"
    )


class TextMediaItem(BaseModel):
    """Text media item for displaying text content"""

    kind: Literal["media"]
    itemType: Literal["text"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(None, description="MIME type")
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before recording starts"
    )
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(
        None, description="State after recording finishes"
    )


class ChoicePromptItem(BaseModel):
    """Single choice prompt item"""

    kind: Literal["prompt"]
    itemType: Literal["choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(None, description="MIME type")
    options: list[str] = Field(..., description="Localized answer options")
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before prompt is shown"
    )


class MultiChoicePromptItem(BaseModel):
    """Multiple choice prompt item with optional text entry"""

    kind: Literal["prompt"]
    itemType: Literal["multi-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(None, description="MIME type")
    options: list[str] = Field(..., description="Localized answer options")
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before prompt is shown"
    )
    otherAnswer: Optional[str] = Field(
        None, description="Localized label for 'other' option"
    )
    otherEntryLabel: Optional[str] = Field(
        None, description="Localized label for text entry field allowing custom answers"
    )


class SuperChoicePromptItem(BaseModel):
    """Super choice prompt item with optional text entry"""

    kind: Literal["prompt"]
    itemType: Literal["super-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(None, description="MIME type")
    options: list[str] = Field(..., description="Localized answer options")
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before prompt is shown"
    )
    otherEntryLabel: Optional[str] = Field(
        None, description="Localized label for text entry field allowing custom answers"
    )


class TextInputItem(BaseModel):
    """Text input prompt item"""

    kind: Literal["prompt"]
    itemType: Literal["text"]
    itemId: str = Field(..., description="UUID v4 of the item")
    typeId: Optional[str] = Field(None, description="MIME type")
    options: list = Field(default_factory=list, description="Empty list for text input")
    isRecording: bool
    start: Optional[MediaState] = Field(
        None, description="State before prompt is shown"
    )


# Discriminated union of all schedule item types
# Note: We order prompts before media items so TextInputItem (prompt/text) is tried
# before TextMediaItem (media/text). Pydantic will check kind+itemType combination.
ScheduleItem = Union[
    ChoicePromptItem,
    MultiChoicePromptItem,
    SuperChoicePromptItem,
    TextInputItem,
    AudioMediaItem,
    VideoMediaItem,
    YleAudioMediaItem,
    YleVideoMediaItem,
    TextContentItem,
    ImageMediaItem,
    TextMediaItem,
]


# ============================================================================
# Schedule
# ============================================================================


class Schedule(BaseModel):
    """Schedule (playlist) containing items to present to user"""

    id: Optional[str] = None  # Will be set from filename
    scheduleId: Optional[str] = None
    start: Optional[MediaState] = Field(
        None, description="State shown at schedule start"
    )
    finish: Optional[MediaState] = Field(
        None, description="State shown at schedule finish"
    )
    items: list[ScheduleItem]


# ============================================================================
# Theme
# ============================================================================


class Theme(BaseModel):
    """Theme containing multiple schedule IDs with localized content"""

    id: Optional[str] = None  # Will be set from filename
    mediaState: MediaState
    schedule: Optional[Schedule]


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
    duration: float | None = None
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


class ScheduleAvailability(BaseModel):
    """Availability info for one schedule across languages"""

    id: str
    availableLanguages: list[str]


class ThemeAvailability(BaseModel):
    """Availability info for one theme across languages"""

    id: str
    availableLanguages: list[str]
