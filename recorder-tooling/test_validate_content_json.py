from __future__ import annotations

import json
from pathlib import Path

from recorder_tooling.validate_content_json import validate_content_json


def test_valid_theme_payload_passes(tmp_path: Path) -> None:
    theme_file = tmp_path / "fi.json"
    theme_file.write_text(
        json.dumps(
            {
                "mediaState": {
                    "title": "Hello",
                    "body1": "",
                    "body2": "",
                    "url": None,
                },
                "schedule": None,
            }
        ),
        encoding="utf-8",
    )

    result = validate_content_json(theme_file)
    assert result.issues == []


def test_invalid_theme_payload_fails(tmp_path: Path) -> None:
    theme_file = tmp_path / "nb.json"
    theme_file.write_text(
        json.dumps(
            {
                "schedule": None,
            }
        ),
        encoding="utf-8",
    )

    result = validate_content_json(theme_file)
    assert len(result.issues) == 1
    assert "mediaState" in result.issues[0].message
