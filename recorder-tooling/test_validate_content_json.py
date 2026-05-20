from __future__ import annotations

import json
from pathlib import Path

from validate_content_json import validate_content_json


def test_https_urls_are_not_flagged_as_missing_media(tmp_path: Path) -> None:
    content_root = tmp_path / "content"
    themes_dir = content_root / "themes"
    media_dir = content_root / "media"
    themes_dir.mkdir(parents=True)
    media_dir.mkdir(parents=True)

    (media_dir / "placeholder.jpg").write_bytes(b"data")
    (themes_dir / "en.json").write_text(
        json.dumps(
            {
                "items": [
                    {
                        "url": "https://example.com/image.jpg",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = validate_content_json(content_root, media_dir)

    assert result.issues == []
