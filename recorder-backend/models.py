"""
Pydantic models for Kielipankki Recorder schedules and themes.

Uses discriminated unions to handle the polymorphic Item types.
"""

from typing import Literal, Optional, Union
from pydantic import BaseModel, Field


# ============================================================================
# Nested structures for media items
# ============================================================================


class MediaState(BaseModel):
    """State information displayed during media playback/recording"""

    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    imageUrl: Optional[str] = Field(None, description="Optional image URL for this state")


# ============================================================================
# Schedule Items (Discriminated Union)
# ============================================================================


class AudioMediaItem(BaseModel):
    """Audio media item with direct URL"""

    kind: Literal["media"]
    itemType: Literal["audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to audio file")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'audio/m4a', 'audio/mpeg')")
    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")


class VideoMediaItem(BaseModel):
    """Video media item with direct URL"""

    kind: Literal["media"]
    itemType: Literal["video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to video file")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'video/mp4', 'video/webm')")
    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")


class YleAudioMediaItem(BaseModel):
    """YLE audio program item"""

    kind: Literal["media"]
    itemType: Literal["yle-audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="MIME type")
    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")


class YleVideoMediaItem(BaseModel):
    """YLE video program item"""

    kind: Literal["media"]
    itemType: Literal["yle-video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="MIME type")
    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")


class TextContentItem(BaseModel):
    """Text content item"""

    kind: Literal["media"]
    itemType: Literal["text-content"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="URL to text content")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'text/plain', 'text/html')")
    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")


class ImageMediaItem(BaseModel):
    """Image media item"""

    kind: Literal["media"]
    itemType: Literal["image"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to image file")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'image/jpeg', 'image/png')")
    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")


class TextMediaItem(BaseModel):
    """Text media item for displaying text content"""

    kind: Literal["media"]
    itemType: Literal["text"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: Optional[str] = Field(None, description="Optional URL")
    typeId: Optional[str] = Field(None, description="MIME type")
    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")


class ChoicePromptItem(BaseModel):
    """Single choice prompt item"""

    kind: Literal["prompt"]
    itemType: Literal["choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    title: dict[str, str] = Field(..., description="Localized question text")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list[dict[str, str]] = Field(..., description="Localized answer options")
    isRecording: bool


class MultiChoicePromptItem(BaseModel):
    """Multiple choice prompt item with optional text entry"""

    kind: Literal["prompt"]
    itemType: Literal["multi-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    title: dict[str, str] = Field(..., description="Localized question text")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list[dict[str, str]] = Field(..., description="Localized answer options")
    isRecording: bool
    otherAnswer: Optional[dict[str, str]] = Field(
        None, description="Localized label for 'other' option"
    )
    otherEntryLabel: Optional[dict[str, str]] = Field(
        None, description="Localized label for text entry field allowing custom answers"
    )


class SuperChoicePromptItem(BaseModel):
    """Super choice prompt item with optional text entry"""

    kind: Literal["prompt"]
    itemType: Literal["super-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    title: dict[str, str] = Field(..., description="Localized question text")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list[dict[str, str]] = Field(..., description="Localized answer options")
    isRecording: bool
    otherEntryLabel: Optional[dict[str, str]] = Field(
        None, description="Localized label for text entry field allowing custom answers"
    )


class TextInputItem(BaseModel):
    """Text input prompt item"""

    kind: Literal["prompt"]
    itemType: Literal["text"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    title: dict[str, str] = Field(..., description="Localized question text")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    options: list = Field(default_factory=list, description="Empty list for text input")
    isRecording: bool
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")


# Discriminated union of all schedule item types
# Note: We cannot use a simple discriminator because both TextMediaItem and TextInputItem
# have itemType="text" but different kind values. Pydantic will try them in order.
ScheduleItem = Union[
    AudioMediaItem,
    VideoMediaItem,
    YleAudioMediaItem,
    YleVideoMediaItem,
    TextContentItem,
    ImageMediaItem,
    TextMediaItem,
    ChoicePromptItem,
    MultiChoicePromptItem,
    SuperChoicePromptItem,
    TextInputItem,
]


# ============================================================================
# Schedule
# ============================================================================


class ScheduleState(BaseModel):
    """State information for schedule start/finish screens"""

    title: dict[str, str] = Field(..., description="Localized title")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: Optional[dict[str, str]] = Field(None, description="Localized body text 2")
    imageUrl: Optional[str] = Field(None, description="Optional image URL")


class Schedule(BaseModel):
    """Schedule (playlist) containing items to present to user"""

    id: Optional[str] = None  # Will be set from filename
    scheduleId: Optional[str] = None
    title: Optional[dict[str, str]] = Field(None, description="Localized title")
    body1: Optional[dict[str, str]] = Field(None, description="Localized body text 1")
    body2: Optional[dict[str, str]] = Field(None, description="Localized body text 2")
    start: Optional[ScheduleState] = Field(None, description="State shown at schedule start")
    finish: Optional[ScheduleState] = Field(None, description="State shown at schedule finish")
    items: list[ScheduleItem]


# ============================================================================
# Theme
# ============================================================================


class Theme(BaseModel):
    """Theme containing multiple schedule IDs with localized content"""

    id: Optional[str] = None  # Will be set from filename
    title: dict[str, str] = Field(..., description="Localized title (e.g., {'fi': '...', 'nb': '...'})")
    body1: dict[str, str] = Field(..., description="Localized body text 1")
    body2: dict[str, str] = Field(..., description="Localized body text 2")
    image: Optional[str] = Field(None, description="URL to theme image")
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
