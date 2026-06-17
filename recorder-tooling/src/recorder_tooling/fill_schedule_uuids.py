#!/usr/bin/env python3
"""Fill UUID values for scheduleId and itemId fields in a schedule JSON file.

By default, only empty values are filled. Use --force to regenerate all IDs.
"""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _should_fill(value: Any, force: bool) -> bool:
    if force:
        return True
    return not isinstance(value, str) or value.strip() == ""


def fill_ids(obj: Any, force: bool) -> tuple[int, int]:
    """Return (filled_schedule_ids, filled_item_ids)."""
    schedule_count = 0
    item_count = 0

    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "scheduleId" and _should_fill(value, force):
                obj[key] = _new_uuid()
                schedule_count += 1
            elif key == "itemId" and _should_fill(value, force):
                obj[key] = _new_uuid()
                item_count += 1

            child_schedule, child_item = fill_ids(obj[key], force)
            schedule_count += child_schedule
            item_count += child_item

    elif isinstance(obj, list):
        for item in obj:
            child_schedule, child_item = fill_ids(item, force)
            schedule_count += child_schedule
            item_count += child_item

    return schedule_count, item_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill scheduleId/itemId UUIDs in a schedule JSON file."
    )
    parser.add_argument("file", type=Path, help="Path to schedule JSON file")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate all scheduleId/itemId values, including non-empty ones",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing the file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path: Path = args.file

    if not path.exists():
        print(f"Error: file does not exist: {path}")
        return 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}")
        return 1

    filled_schedule, filled_item = fill_ids(data, args.force)

    if args.dry_run:
        print(
            f"Would update {filled_schedule} scheduleId and {filled_item} itemId values in {path}"
        )
        return 0

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Updated {path}")
    print(f"scheduleId values filled: {filled_schedule}")
    print(f"itemId values filled: {filled_item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
