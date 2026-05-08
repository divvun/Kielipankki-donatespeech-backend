#!/usr/bin/env python3
"""
Migrate flat blob layout to per-language layout.

Flat layout (old):  schedule/{id}.json       theme/{id}.json
New layout:         schedule/{id}/{lang}.json theme/{id}/{lang}.json

Usage:
    python migrate-storage.py --lang fi [--lang nb] [--apply]

Options:
    --lang LANG     Language tag to assign to flat blobs. Can be repeated.
                    At least one is required.
    --apply         Actually perform the migration. Without this flag the
                    script only prints what it would do (dry run).
    --prefix PREFIX Blob prefix to migrate: 'schedule/' or 'theme/'
                    (default: migrate both)

Examples:
    # Dry run — show what would happen
    python migrate-storage.py --lang fi --lang nb

    # Apply only to schedules
    python migrate-storage.py --lang fi --lang nb --apply --prefix schedule/

    # Apply to everything
    python migrate-storage.py --lang fi --lang nb --apply
"""

import argparse
import os
import sys

from azure.storage.blob import BlobServiceClient

AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONNECTION_STRING = (
    os.environ.get("AZURE_STORAGE_CONNECTION_STRING") or AZURITE_CONNECTION_STRING
)
CONTAINER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_NAME") or "recorder-content"


def _is_flat_blob(blob_name: str, prefix: str) -> bool:
    """Return True for flat blobs like 'schedule/{id}.json' (no sub-directory)."""
    if not blob_name.startswith(prefix):
        return False
    suffix = blob_name[len(prefix) :]
    # Flat: no slash, ends with .json
    return suffix.endswith(".json") and "/" not in suffix


def _migrate_prefix(
    client: BlobServiceClient,
    prefix: str,
    languages: list[str],
    apply: bool,
) -> tuple[int, int]:
    """
    Migrate flat blobs under *prefix* to per-language layout.

    Returns (migrated_count, skipped_count).
    """
    container = client.get_container_client(CONTAINER_NAME)
    flat_blobs = [
        b.name
        for b in container.list_blobs(name_starts_with=prefix)
        if _is_flat_blob(b.name, prefix)
    ]

    if not flat_blobs:
        print(f"  No flat blobs found under '{prefix}'")
        return 0, 0

    migrated = 0
    skipped = 0

    for blob_name in sorted(flat_blobs):
        # e.g. 'schedule/abc-123.json' → id = 'abc-123'
        suffix = blob_name[len(prefix) :]
        item_id = suffix[: -len(".json")]

        # Download content once
        src_client = client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
        content = src_client.download_blob().readall()

        target_names = [f"{prefix}{item_id}/{lang}.json" for lang in languages]
        already_exists = []
        to_write = []

        for target in target_names:
            tgt_client = client.get_blob_client(container=CONTAINER_NAME, blob=target)
            try:
                tgt_client.get_blob_properties()
                already_exists.append(target)
            except Exception:
                to_write.append(target)

        if already_exists:
            print(f"  SKIP {blob_name} — target(s) already exist: {already_exists}")
            skipped += 1
            continue

        for target in to_write:
            if apply:
                tgt_client = client.get_blob_client(
                    container=CONTAINER_NAME, blob=target
                )
                tgt_client.upload_blob(content, overwrite=False, content_settings=None)
            print(f"  {'COPY' if apply else '[dry] would copy'} {blob_name} → {target}")

        migrated += 1

    return migrated, skipped


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--lang",
        action="append",
        required=True,
        metavar="LANG",
        help="Language tag to assign (e.g. fi, nb). Repeat for multiple.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the migration (default: dry run).",
    )
    parser.add_argument(
        "--prefix",
        choices=["schedule/", "theme/"],
        default=None,
        help="Restrict migration to one prefix (default: both).",
    )
    args = parser.parse_args()

    languages = [lang.strip().lower().replace("_", "-") for lang in args.lang]
    prefixes = [args.prefix] if args.prefix else ["schedule/", "theme/"]

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"Migration mode: {mode}")
    print(f"Languages: {languages}")
    print(f"Prefixes: {prefixes}")
    print(f"Container: {CONTAINER_NAME}\n")

    if not args.apply:
        print("(Use --apply to actually perform these changes.)\n")

    try:
        client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    except Exception as e:
        print(f"Failed to connect: {e}", file=sys.stderr)
        sys.exit(1)

    total_migrated = 0
    total_skipped = 0

    for prefix in prefixes:
        print(f"--- {prefix} ---")
        migrated, skipped = _migrate_prefix(client, prefix, languages, args.apply)
        print(f"  Done: {migrated} migrated, {skipped} skipped\n")
        total_migrated += migrated
        total_skipped += skipped

    print(f"Total: {total_migrated} migrated, {total_skipped} skipped")

    if not args.apply and total_migrated > 0:
        print("\nRun with --apply to perform the migration.")


if __name__ == "__main__":
    main()
