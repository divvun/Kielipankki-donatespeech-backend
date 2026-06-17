#!/usr/bin/env python3
"""Replace itemId values in a schedule JSON file with new UUIDs."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replace all itemId values in schedule JSON with new UUIDs."
    )
    parser.add_argument("file", type=Path, help="Path to schedule JSON file")
    return parser.parse_args()


def replace_item_ids(payload: dict[str, Any]) -> int:
    items = payload.get("items")
    if not isinstance(items, list):
        return 0

    updated = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        item["itemId"] = str(uuid.uuid4())
        updated += 1

    return updated


def main() -> int:
    args = parse_args()
    path: Path = args.file

    if not path.exists():
        print(f"Error: file does not exist: {path}")
        return 1

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}")
        return 1

    if not isinstance(payload, dict):
        print("Error: JSON root must be an object")
        return 1

    updated = replace_item_ids(payload)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Updated {path}")
    print(f"itemId values replaced: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
