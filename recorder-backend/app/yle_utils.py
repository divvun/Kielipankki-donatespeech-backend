import os
import json
import logging
import urllib.request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FileProcessingError(Exception):
    """Custom exception for file processing errors."""

    pass


CLIENT_ID = os.environ.get("YLE_CLIENT_ID")
CLIENT_KEY = os.environ.get("YLE_CLIENT_KEY")

PROGRAM_INFO_URL = "https://programs.api.yle.fi/v3/schema/v1/programs/items/{program_id}.json?app_id={client_id}&app_key={client_key}"
MEDIA_URL = "https://media.api.yle.fi/v6/{media_id}/playouts.json?program_id={program_id}&protocol=HLS&app_id={client_id}&app_key={client_key}"
# Old: https://external.api.yle.fi/v1/
# New: https://programs.api.yle.fi/v3/


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
    # If YLE credentials are not configured, return the program ID as-is
    # This allows the client to handle the "fake-yle-thingy"
    if not all([CLIENT_ID, CLIENT_KEY]):
        logger.warning(
            "YLE credentials not configured - returning fake YLE URL (program ID as-is)"
        )
        return yle_program_id

    try:
        media_url = get_media_url(yle_program_id)

        with urllib.request.urlopen(media_url, timeout=10) as media_res:
            media_item_url = json.loads(media_res.read()).get("data")[0].get("url")

        logger.info("Successfully resolved YLE media URL")
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
    processed_program_info_url = PROGRAM_INFO_URL.format(
        program_id=yle_program_id, client_id=CLIENT_ID, client_key=CLIENT_KEY
    )

    with urllib.request.urlopen(processed_program_info_url, timeout=10) as res:
        program_res = json.loads(res.read())
        pub_events = program_res.get("data", {}).get("publicationEvent") or []

        if not pub_events:
            raise FileProcessingError("Media URL not found: no publication events")

        pub_event = pub_events[0]
        media_id = (pub_event.get("media") or {}).get("id")

        if not media_id:
            raise FileProcessingError("Media URL not found: media id missing")

        return MEDIA_URL.format(
            program_id=yle_program_id,
            media_id=media_id,
            client_id=CLIENT_ID,
            client_key=CLIENT_KEY,
        )
