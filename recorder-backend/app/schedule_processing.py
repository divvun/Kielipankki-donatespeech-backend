"""Schedule preprocessing helpers."""

import logging
from collections.abc import Callable
from urllib.parse import quote

from app.models import Schedule, ScheduleItem, YleAudioMediaItem, YleVideoMediaItem
from app.yle_utils import map_yle_content

logger = logging.getLogger(__name__)


def map_local_media_url(url: str | None) -> str | None:
    """Map local media filenames to the media-serving route."""
    if not url:
        return url

    if url.startswith(("http://", "https://", "/v1/media/", "/v1/yle-media/")):
        return url

    return f"/v1/media/{quote(url, safe='')}"


def _map_yle_urls_in_states(
    item: YleAudioMediaItem | YleVideoMediaItem,
    mapper: Callable[[str], str],
) -> None:
    """Map YLE program IDs in media-state URLs to stream URLs when possible."""
    for state_attr in ("start", "recording", "finish"):
        state = getattr(item, state_attr, None)
        if not state or not state.url or state.url.startswith("http"):
            continue

        try:
            state.url = mapper(state.url)
        except Exception as exc:  # Keep original URL if mapping fails.
            logger.warning("Failed to map YLE URL '%s': %s", state.url, exc)


def _map_local_media_urls_in_states(item: ScheduleItem) -> None:
    """Map local media filenames in item states to route URLs."""
    for state_attr in ("start", "recording", "finish"):
        state = getattr(item, state_attr, None)
        if not state:
            continue
        state.url = map_local_media_url(state.url)


def pre_process_schedule(
    schedule: Schedule,
    mapper: Callable[[str], str] = map_yle_content,
) -> Schedule:
    """Map YLE item URLs in-place and return the schedule."""
    processed_items: list[ScheduleItem] = []

    if schedule.start:
        schedule.start.url = map_local_media_url(schedule.start.url)
    if schedule.finish:
        schedule.finish.url = map_local_media_url(schedule.finish.url)

    for item in schedule.items:
        if isinstance(item, (YleAudioMediaItem, YleVideoMediaItem)):
            _map_yle_urls_in_states(item, mapper)
        else:
            _map_local_media_urls_in_states(item)
        processed_items.append(item)

    schedule.items = processed_items
    return schedule
