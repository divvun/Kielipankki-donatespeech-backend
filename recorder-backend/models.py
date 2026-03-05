"""
Pydantic models for Kielipankki Recorder schedules and themes.

Uses discriminated unions to handle the polymorphic Item types.
"""

from typing import Any, Literal, Optional, Union
from pydantic import BaseModel, Field, model_validator


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
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            # Convert flat structure to nested MediaState
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class VideoMediaItem(BaseModel):
    """Video media item with direct URL"""

    kind: Literal["media"]
    itemType: Literal["video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to video file")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'video/mp4', 'video/webm')")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            # Convert flat structure to nested MediaState
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class YleAudioMediaItem(BaseModel):
    """YLE audio program item"""

    kind: Literal["media"]
    itemType: Literal["yle-audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class YleVideoMediaItem(BaseModel):
    """YLE video program item"""

    kind: Literal["media"]
    itemType: Literal["yle-video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class FakeYleAudioMediaItem(BaseModel):
    """Fake YLE audio item returned when YLE credentials are not configured"""

    kind: Literal["media"]
    itemType: Literal["fake-yle-audio"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class FakeYleVideoMediaItem(BaseModel):
    """Fake YLE video item returned when YLE credentials are not configured"""

    kind: Literal["media"]
    itemType: Literal["fake-yle-video"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="YLE program ID")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class TextContentItem(BaseModel):
    """Text content item"""

    kind: Literal["media"]
    itemType: Literal["text-content"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="URL to text content")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'text/plain', 'text/html')")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class ImageMediaItem(BaseModel):
    """Image media item"""

    kind: Literal["media"]
    itemType: Literal["image"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Direct URL to image file")
    typeId: Optional[str] = Field(None, description="MIME type (e.g., 'image/jpeg', 'image/png')")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class TextMediaItem(BaseModel):
    """Text media item for displaying text content"""

    kind: Literal["media"]
    itemType: Literal["text"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: Optional[str] = Field(None, description="Optional URL")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for media items")
    isRecording: bool
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")
    start: Optional[MediaState] = Field(None, description="State before recording starts")
    recording: Optional[MediaState] = Field(None, description="State during recording")
    finish: Optional[MediaState] = Field(None, description="State after recording finishes")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': None
            }
        return data


class ChoicePromptItem(BaseModel):
    """Single choice prompt item"""

    kind: Literal["prompt"]
    itemType: Literal["choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list[dict[str, str]] = Field(..., description="Localized answer options")
    isRecording: bool

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': data.get('url')  # Use url as imageUrl for prompts
            }
        return data


class MultiChoicePromptItem(BaseModel):
    """Multiple choice prompt item with optional text entry"""

    kind: Literal["prompt"]
    itemType: Literal["multi-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list[dict[str, str]] = Field(..., description="Localized answer options")
    isRecording: bool
    otherAnswer: Optional[dict[str, str]] = Field(
        None, description="Localized label for 'other' option"
    )
    otherEntryLabel: Optional[dict[str, str]] = Field(
        None, description="Localized label for text entry field allowing custom answers"
    )

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': data.get('url')
            }
        return data


class SuperChoicePromptItem(BaseModel):
    """Super choice prompt item with optional text entry"""

    kind: Literal["prompt"]
    itemType: Literal["super-choice"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list[dict[str, str]] = Field(..., description="Localized answer options")
    isRecording: bool
    otherEntryLabel: Optional[dict[str, str]] = Field(
        None, description="Localized label for text entry field allowing custom answers"
    )

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': data.get('url')
            }
        return data


class TextInputItem(BaseModel):
    """Text input prompt item"""

    kind: Literal["prompt"]
    itemType: Literal["text"]
    itemId: str = Field(..., description="UUID v4 of the item")
    url: str = Field(..., description="Image URL for the prompt")
    typeId: Optional[str] = Field(None, description="MIME type")
    default: MediaState = Field(..., description="Default/initial state")
    options: list = Field(default_factory=list, description="Empty list for text input")
    isRecording: bool
    metaTitle: Optional[dict[str, str]] = Field(None, description="Optional meta title")

    @model_validator(mode='before')
    @classmethod
    def build_default_state(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'title' in data and 'default' not in data:
            data['default'] = {
                'title': data.pop('title'),
                'body1': data.pop('body1'),
                'body2': data.pop('body2'),
                'imageUrl': data.get('url')
            }
        return data


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
    FakeYleAudioMediaItem,
    FakeYleVideoMediaItem,
    TextContentItem,
    ImageMediaItem,
    TextMediaItem,
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
