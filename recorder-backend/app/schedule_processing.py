"""Schedule preprocessing helpers."""

import logging
from collections.abc import Callable

from app.models import Schedule, ScheduleItem, YleAudioMediaItem, YleVideoMediaItem
from app.yle_utils import map_yle_content

logger = logging.getLogger(__name__)


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


def pre_process_schedule(
    schedule: Schedule,
    mapper: Callable[[str], str] = map_yle_content,
) -> Schedule:
    """Map YLE item URLs in-place and return the schedule."""
    processed_items: list[ScheduleItem] = []

    for item in schedule.items:
        if isinstance(item, (YleAudioMediaItem, YleVideoMediaItem)):
            _map_yle_urls_in_states(item, mapper)
        processed_items.append(item)

    schedule.items = processed_items
    return schedule
