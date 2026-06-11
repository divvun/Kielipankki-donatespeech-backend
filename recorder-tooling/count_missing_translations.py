"""Write one worksheet JSON per sheet, with all language values preserved.

The workbook format is the same as convert_excel_to_json.py.
Output files are written to the current working directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from convert_excel_to_json import DRIVE_FILENAME_MAP, ParsedState, _parse_sheet
from openpyxl import load_workbook  # type: ignore[import-untyped]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write one multi-language JSON per worksheet"
    )
    parser.add_argument("input_xlsx", type=Path, help="Input workbook path")
    return parser.parse_args()


def _normalize(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _normalized_localized(values: dict[str, str]) -> dict[str, str]:
    return {
        _normalize(language).lower(): _normalize(value)
        for language, value in values.items()
        if _normalize(language)
    }


def _state_to_multilang_dict(state: ParsedState) -> dict[str, Any]:
    url = _normalize(state.url)
    if url in DRIVE_FILENAME_MAP:
        url = DRIVE_FILENAME_MAP[url]

    return {
        "title": _normalized_localized(state.title),
        "body1": _normalized_localized(state.body1),
        "body2": _normalized_localized(state.body2),
        "url": url or None,
    }


def _item_to_multilang_dict(item: dict[str, Any]) -> dict[str, Any]:
    converted: dict[str, Any] = {
        "itemId": item.get("itemId", ""),
        "kind": item.get("kind", "media"),
        "itemType": item.get("itemType", "image"),
        "typeId": item.get("typeId"),
        "isRecording": bool(item.get("isRecording", False)),
    }

    for state_name in ("start", "recording", "finish"):
        state = item.get(state_name)
        if isinstance(state, ParsedState):
            converted[state_name] = _state_to_multilang_dict(state)

    return converted


def _sheet_payload_multilang(ws: Any) -> tuple[str, dict[str, Any]]:
    theme_id, theme_url, theme_title, schedule_data = _parse_sheet(ws)

    payload = {
        "mediaState": {
            "title": _normalized_localized(theme_title),
            "body1": {},
            "body2": {},
            "url": _normalize(theme_url) or None,
        },
        "schedule": {
            "scheduleId": schedule_data.get("scheduleId") or None,
            "start": _state_to_multilang_dict(schedule_data["start"]),
            "finish": _state_to_multilang_dict(schedule_data["finish"]),
            "items": [
                _item_to_multilang_dict(item)
                for item in schedule_data.get("items", [])
            ],
        },
    }

    return theme_id, payload


def _safe_output_stem(value: str) -> str:
    stem = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in value)
    stem = stem.strip("._")
    return stem or "sheet"


def write_multilang_workbook_json(input_xlsx: Path, output_dir: Path) -> list[Path]:
    wb = load_workbook(input_xlsx, data_only=True)
    written: list[Path] = []

    for ws in wb.worksheets:
        theme_id, payload = _sheet_payload_multilang(ws)
        stem = _safe_output_stem(theme_id or ws.title)
        out_path = output_dir / f"{stem}.json"

        # Avoid overwriting if multiple sheets sanitize to same name.
        suffix = 2
        while out_path.exists():
            out_path = output_dir / f"{stem}_{suffix}.json"
            suffix += 1

        out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(out_path)

    return written


def main() -> int:
    args = parse_args()

    if not args.input_xlsx.exists():
        print(f"Error: input workbook not found: {args.input_xlsx}")
        return 1

    try:
        written = write_multilang_workbook_json(args.input_xlsx, Path.cwd())
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Wrote {len(written)} files")
    for path in written:
        print(path)

    return 0
