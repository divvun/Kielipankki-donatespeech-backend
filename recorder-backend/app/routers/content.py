"""Theme content endpoints."""

import logging

from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import ValidationError

from app.models import Theme, ThemeAvailability
from app.schedule_processing import pre_process_schedule, map_local_media_url
from app.storage import (
    load_blob_json,
    list_blobs_with_prefix,
    build_theme_blob_name,
    list_available_languages_by_id,
    normalize_language_tag,
    StorageError,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/v1/theme/{theme_id}", response_model=Theme)
async def load_theme(
    theme_id: str = Path(..., description="Theme ID"),
    lang: str = Query(..., description="Language code, for example 'fi' or 'nb'"),
):
    """Load a specific theme file for one language."""
    blob_name = build_theme_blob_name(theme_id, lang)
    try:
        theme_dict = await load_blob_json(blob_name)
        theme = Theme(**theme_dict)
        theme.id = theme_id
        theme.mediaState.url = map_local_media_url(theme.mediaState.url)
        if theme.schedule is not None:
            theme.schedule = pre_process_schedule(theme.schedule)
        return theme
    except ValidationError as e:
        logger.error(f"Invalid theme payload for {theme_id}/{lang}: {e}")
        raise HTTPException(status_code=422, detail="Invalid theme payload")
    except StorageError as e:
        logger.error(f"Error loading theme {theme_id}: {e}")
        raise HTTPException(status_code=404, detail="Theme not found")


@router.get("/v1/theme", response_model=list[ThemeAvailability])
async def list_themes():
    """List all themes with their available languages."""
    try:
        langs_by_id = await list_available_languages_by_id("theme/")
        return [
            ThemeAvailability(id=theme_id, availableLanguages=langs)
            for theme_id, langs in langs_by_id.items()
        ]
    except StorageError as e:
        logger.error(f"Error listing themes: {e}")
        raise HTTPException(status_code=500, detail="Error listing themes")


@router.get("/v1/theme/{theme_id}/languages", response_model=ThemeAvailability)
async def theme_languages(theme_id: str = Path(..., description="Theme ID")):
    """Return which languages are available for one theme."""
    try:
        blob_list = await list_blobs_with_prefix(f"theme/{theme_id}/")
        prefix = f"theme/{theme_id}/"
        languages = sorted(
            {
                normalize_language_tag(b[len(prefix) :][: -len(".json")])
                for b in blob_list
                if b.startswith(prefix)
                and b.endswith(".json")
                and "/" not in b[len(prefix) :]
            }
        )
        if not languages:
            raise HTTPException(status_code=404, detail="Theme not found")
        return ThemeAvailability(id=theme_id, availableLanguages=languages)
    except StorageError as e:
        logger.error(f"Error listing languages for theme {theme_id}: {e}")
        raise HTTPException(status_code=500, detail="Error listing theme languages")
