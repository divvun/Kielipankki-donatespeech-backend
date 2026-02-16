#!/usr/bin/env python3
"""
Convert old schedule format (with 'kind' field) to new format.

Old format uses:
- kind: "media" or "prompt"
- itemType varies based on kind

New format uses only itemType with specific values:
Media: audio, video, yle-audio, yle-video, text-content, image
Prompt: choice, multi-choice, super-choice, text-input
"""

import json
import sys
from pathlib import Path


def convert_item(old_item: dict) -> dict:
    """Convert a single item from old format to new format"""
    kind = old_item.get("kind")
    item_type = old_item.get("itemType")

    # Start with basic fields that are always present
    new_item = {
        "itemId": old_item["itemId"],
        "description": old_item["description"],
        "isRecording": old_item.get("isRecording", False),
    }

    if kind == "media":
        # Media items
        if item_type == "text":
            # text → text-content (renamed to avoid conflict with text-input)
            new_item["itemType"] = "text-content"
            new_item["url"] = old_item["url"]
            if old_item.get("typeId") is not None:
                new_item["typeId"] = old_item["typeId"]
        elif item_type in ["yle-audio", "yle-video"]:
            # YLE items - no typeId needed
            new_item["itemType"] = item_type
            new_item["url"] = old_item["url"]
        else:
            # audio, video, image - keep typeId and url
            new_item["itemType"] = item_type
            new_item["url"] = old_item["url"]
            new_item["typeId"] = old_item["typeId"]
        # Note: options field removed from all media items

    elif kind == "prompt":
        # Prompt items
        if item_type == "text":
            # text → text-input (renamed to avoid conflict with text-content)
            new_item["itemType"] = "text-input"
            # Note: typeId, url, options removed from text-input
        elif item_type == "choice":
            # choice - keep options
            new_item["itemType"] = "choice"
            new_item["options"] = old_item.get("options", [])
            # Note: typeId, url removed
        elif item_type in ["multi-choice", "super-choice"]:
            # multi-choice, super-choice - keep options and otherEntryLabel if present
            new_item["itemType"] = item_type
            new_item["options"] = old_item.get("options", [])
            if "otherEntryLabel" in old_item and old_item["otherEntryLabel"]:
                new_item["otherEntryLabel"] = old_item["otherEntryLabel"]
            # Note: typeId, url removed
        else:
            raise ValueError(f"Unknown prompt itemType: {item_type}")
    else:
        raise ValueError(f"Unknown kind: {kind}")

    return new_item


def convert_schedule(old_schedule: dict) -> dict:
    """Convert entire schedule from old format to new format"""
    new_schedule = {}

    # Copy schedule-level fields if present
    if "scheduleId" in old_schedule:
        new_schedule["scheduleId"] = old_schedule["scheduleId"]
    if "description" in old_schedule:
        new_schedule["description"] = old_schedule["description"]

    # Convert all items
    if "items" in old_schedule:
        new_schedule["items"] = [convert_item(item) for item in old_schedule["items"]]

    return new_schedule


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)

    # Read old format
    with open(input_file, "r", encoding="utf-8") as f:
        old_data = json.load(f)

    # Convert to new format
    new_data = convert_schedule(old_data)

    # Write new format
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
        f.write("\n")  # Add trailing newline

    print(f"✓ Converted {input_file} → {output_file}")
    print(f"  Items converted: {len(new_data.get('items', []))}")


if __name__ == "__main__":
    main()
