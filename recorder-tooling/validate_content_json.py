#!/usr/bin/env python3
"""Validate recorder content JSON files.

Checks:
- No duplicate UUID values inside a single language JSON file.
- Every filename referenced by a 'url' attribute exists under the media directory.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)
SCHEDULE_ITEM_PATH_RE = re.compile(r"^schedule\.items\[(\d+)\](?:\.|$)")


@dataclass
class ValidationIssue:
    file_path: Path
    message: str


@dataclass
class ValidationResult:
    files_checked: int
    issues: list[ValidationIssue]


def _is_language_json(path: Path) -> bool:
    return path.suffix == ".json" and len(path.stem) >= 2


def _collect_json_files(content_root: Path) -> list[Path]:
    files: list[Path] = []
    for section in ("themes", "schedules"):
        section_dir = content_root / section
        if not section_dir.exists():
            continue
        for path in section_dir.rglob("*.json"):
            if _is_language_json(path):
                files.append(path)
    return sorted(files)


def _collect_uuid_paths(node: object, path: str, found: dict[str, list[str]]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = f"{path}.{key}" if path else key
            _collect_uuid_paths(value, next_path, found)
        return

    if isinstance(node, list):
        for index, value in enumerate(node):
            _collect_uuid_paths(value, f"{path}[{index}]", found)
        return

    if isinstance(node, str) and UUID_RE.fullmatch(node):
        found.setdefault(node, []).append(path)


def _collect_url_values(node: object, path: str, found: list[tuple[str, str]]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = f"{path}.{key}" if path else key
            if key == "url" and isinstance(value, str) and value.strip():
                found.append((value.strip(), next_path))
            _collect_url_values(value, next_path, found)
        return

    if isinstance(node, list):
        for index, value in enumerate(node):
            _collect_url_values(value, f"{path}[{index}]", found)


def _media_indexes(media_dir: Path) -> tuple[set[str], set[str]]:
    rel_paths: set[str] = set()
    basenames: set[str] = set()

    if not media_dir.exists():
        return rel_paths, basenames

    for media_file in media_dir.rglob("*"):
        if not media_file.is_file():
            continue
        rel_paths.add(media_file.relative_to(media_dir).as_posix())
        basenames.add(media_file.name)

    return rel_paths, basenames


def _url_file_exists(url_value: str, rel_paths: set[str], basenames: set[str]) -> bool:
    parsed = urlparse(url_value)
    if parsed.scheme == "https":
        return True
    raw_path = (parsed.path or url_value).strip()
    if not raw_path:
        return True

    normalized = raw_path.lstrip("/")
    if normalized.startswith("media/"):
        normalized = normalized[len("media/") :]

    if normalized in rel_paths:
        return True

    file_name = Path(normalized).name
    return file_name in basenames


def _is_yle_schedule_item_url(payload: object, json_path: str) -> bool:
    match = SCHEDULE_ITEM_PATH_RE.match(json_path)
    if not match:
        return False

    if not isinstance(payload, dict):
        return False

    schedule = payload.get("schedule")
    if not isinstance(schedule, dict):
        return False

    items = schedule.get("items")
    if not isinstance(items, list):
        return False

    index = int(match.group(1))
    if index >= len(items):
        return False

    item = items[index]
    if not isinstance(item, dict):
        return False

    item_type = item.get("itemType")
    return isinstance(item_type, str) and item_type.startswith("yle-")


def validate_content_json(content_root: Path, media_dir: Path) -> ValidationResult:
    issues: list[ValidationIssue] = []
    json_files = _collect_json_files(content_root)

    if not json_files:
        issues.append(
            ValidationIssue(
                file_path=content_root,
                message="No JSON files found under themes/ or schedules/.",
            )
        )
        return ValidationResult(files_checked=0, issues=issues)

    rel_paths, basenames = _media_indexes(media_dir)
    if not rel_paths:
        issues.append(
            ValidationIssue(
                file_path=media_dir,
                message="Media directory is missing or has no files.",
            )
        )

    for json_file in json_files:
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append(
                ValidationIssue(
                    file_path=json_file,
                    message=f"Invalid JSON: {exc}",
                )
            )
            continue

        uuid_locations: dict[str, list[str]] = {}
        _collect_uuid_paths(payload, "", uuid_locations)
        for uuid_value, paths in uuid_locations.items():
            if len(paths) <= 1:
                continue
            issues.append(
                ValidationIssue(
                    file_path=json_file,
                    message=(
                        f"Duplicate UUID in file: {uuid_value} at {', '.join(paths)}"
                    ),
                )
            )

        urls: list[tuple[str, str]] = []
        _collect_url_values(payload, "", urls)
        for url_value, json_path in urls:
            if _is_yle_schedule_item_url(payload, json_path):
                continue
            if _url_file_exists(url_value, rel_paths, basenames):
                continue
            issues.append(
                ValidationIssue(
                    file_path=json_file,
                    message=(
                        f"Missing media file for url at {json_path}: '{url_value}'"
                    ),
                )
            )

    return ValidationResult(files_checked=len(json_files), issues=issues)


def main(content_root: Path, media_dir: Path | None = None) -> int:
    resolved_content_root = content_root.resolve()
    resolved_media_dir = (media_dir or (content_root / "media")).resolve()

    if not resolved_content_root.exists():
        print(f"Error: content root not found: {resolved_content_root}")
        return 1

    result = validate_content_json(resolved_content_root, resolved_media_dir)

    print(f"Checked {result.files_checked} JSON files")
    if not result.issues:
        print("Validation passed")
        return 0

    print(f"Validation failed with {len(result.issues)} issues:")
    for issue in result.issues:
        print(f"- {issue.file_path}: {issue.message}")
    return 1
