import os
import logging
import requests

from app.settings import get_settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FileProcessingError(Exception):
    """Custom exception for file processing errors."""

    pass


# Keep these patchable in tests; when unset, values are resolved lazily per call.
_UNSET = object()
CLIENT_ID = _UNSET
CLIENT_KEY = _UNSET

def map_yle_content(yle_program_id: str) -> str:
    """Maps YLE program ID to a media URL.

    Args:
        yle_program_id: The YLE program ID to be mapped.

    Returns:
        The media URL corresponding to the YLE program ID.
        If YLE credentials are not configured, returns the program ID as-is
        (a "fake-yle-thingy" for the client to handle).

    Raises:
        FileProcessingError: If there is an error during the mapping process.
    """
    client_id, client_key = _get_client_credentials()

    # If YLE credentials are not configured, return the program ID as-is
    # This allows the client to handle the "fake-yle-thingy"
    if not all([client_id, client_key]):
        logger.warning(
            "YLE credentials not configured - returning fake YLE URL (program ID as-is)"
        )
        return yle_program_id

    try:
        media_url = get_media_url(yle_program_id)

        media_response = requests.get(media_url, timeout=10)
        media_response.raise_for_status()
        media_data = media_response.json().get("data", {})
        hls = media_data.get("hls", {})
        media_item_url = hls.get("url")
        if not media_item_url:
            logger.error("No media item URL found in the media response for YLE program ID: {}".format(yle_program_id))
            raise FileProcessingError("No media item URL found in the media response")
        logger.info("Successfully mapped YLE program ID {} to media URL: {}".format(yle_program_id, media_item_url))
        return media_item_url
    except Exception as e:
        logger.error("Error resolving yle URL: {}".format(e))
        raise FileProcessingError(e)


def get_media_url(yle_program_id: str) -> str:
    """Fetches the media URL for a given YLE program ID.

    Args:
        yle_program_id: The YLE program ID for which to fetch the media URL.

    Returns:
        The media URL corresponding to the given YLE program ID.
    """
    client_id, client_key = _get_client_credentials()

    if not all([client_id, client_key]):
        raise FileProcessingError("YLE credentials not configured")

    base_url = f"https://programs.api.yle.fi/v3/schema/v1/items/{yle_program_id}?app_id={client_id}&app_key={client_key}"

    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        program_data = response.json()

        publication_events = program_data.get("data", {}).get("publicationEvent", [])
        if not publication_events:
            raise FileProcessingError("No publication events found for the given YLE program ID")

        media = publication_events[0].get("media")
        media_id = media.get("id") if media else None
        logger.debug("Resolved YLE media ID for %s: %s", yle_program_id, media_id)

        if not media_id:
            logger.error("No media ID found in the publication event for YLE program ID: {}".format(yle_program_id))
            raise FileProcessingError("No media ID found in the publication event")

        media_url = f"https://media.api.yle.fi/v6/{media_id}/playouts.json?app_id={client_id}&app_key={client_key}"
        return media_url
    except requests.RequestException as error:
        logger.error("Error fetching program information: {}".format(error))
        raise FileProcessingError(f"Error fetching program information: {error}")

def _get_client_credentials() -> tuple[str | None, str | None]:
    settings = get_settings()
    client_id = (
        CLIENT_ID
        if CLIENT_ID is not _UNSET
        else settings.yle_client_id or os.environ.get("YLE_CLIENT_ID")
    )
    client_key = (
        CLIENT_KEY
        if CLIENT_KEY is not _UNSET
        else settings.yle_client_key or os.environ.get("YLE_CLIENT_KEY")
    )
    return client_id, client_key
