"""Schedule preprocessing helpers."""

import logging
from urllib.parse import quote

from app.models import Schedule, ScheduleItem, YleAudioMediaItem, YleVideoMediaItem

logger = logging.getLogger(__name__)


def map_local_media_url(url: str | None) -> str | None:
    """Map local media filenames to the media-serving route."""
    if not url:
        return url

    if url.startswith(("http://", "https://", "/v1/media/", "/v1/yle-media/")):
        return url

    return f"/v1/media/{quote(url, safe='')}"


def map_yle_program_url(url: str | None) -> str | None:
    """Map raw YLE program IDs to the lazy YLE media endpoint."""
    if not url:
        return url

    if url.startswith(("http://", "https://", "/v1/yle-media/")):
        return url

    return f"/v1/yle-media/{quote(url, safe='')}"


def _map_yle_urls_in_states(
    item: YleAudioMediaItem | YleVideoMediaItem,
) -> None:
    """Map YLE program IDs in media-state URLs to lazy endpoint URLs."""
    for state_attr in ("start", "recording", "finish"):
        state = getattr(item, state_attr, None)
        if not state:
            continue
        state.url = map_yle_program_url(state.url)


def _map_local_media_urls_in_states(item: ScheduleItem) -> None:
    """Map local media filenames in item states to route URLs."""
    for state_attr in ("start", "recording", "finish"):
        state = getattr(item, state_attr, None)
        if not state:
            continue
        state.url = map_local_media_url(state.url)


def pre_process_schedule(
    schedule: Schedule,
) -> Schedule:
    """Map schedule URLs in-place and return the schedule."""
    processed_items: list[ScheduleItem] = []

    if schedule.start:
        schedule.start.url = map_local_media_url(schedule.start.url)
    if schedule.finish:
        schedule.finish.url = map_local_media_url(schedule.finish.url)

    for item in schedule.items:
        if isinstance(item, (YleAudioMediaItem, YleVideoMediaItem)):
            _map_yle_urls_in_states(item)
        else:
            _map_local_media_urls_in_states(item)
        processed_items.append(item)

    schedule.items = processed_items
    return schedule
