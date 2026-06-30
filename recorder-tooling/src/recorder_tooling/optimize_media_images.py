#!/usr/bin/env python3
"""Optimize image files for faster media loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png"}


@dataclass
class OptimizationSummary:
    files_processed: int
    files_changed: int
    bytes_before: int
    bytes_after: int


def _iter_image_files(media_root: Path) -> list[Path]:
    return sorted(
        path
        for path in media_root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def _resize_if_needed(image: Image.Image, max_dimension: int | None) -> Image.Image:
    if not max_dimension:
        return image

    width, height = image.size
    if max(width, height) <= max_dimension:
        return image

    resized = image.copy()
    resized.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
    return resized


def optimize_media_images(
    media_root: Path,
    jpeg_quality: int,
    max_dimension: int | None,
    dry_run: bool,
) -> OptimizationSummary:
    files = _iter_image_files(media_root)
    bytes_before = sum(path.stat().st_size for path in files)

    files_changed = 0
    files_processed = 0

    for image_path in files:
        files_processed += 1
        original_bytes = image_path.read_bytes()
        original_size = len(original_bytes)

        with Image.open(image_path) as opened:
            working = _resize_if_needed(opened, max_dimension)
            needs_mode_conversion = image_path.suffix.lower() in {".jpg", ".jpeg"} and working.mode not in {
                "RGB",
                "L",
            }
            if needs_mode_conversion:
                working = working.convert("RGB")

            output_path = image_path.with_suffix(image_path.suffix + ".optimized")
            save_kwargs: dict[str, bool | int | str] = {}
            if image_path.suffix.lower() in {".jpg", ".jpeg"}:
                save_kwargs = {
                    "quality": jpeg_quality,
                    "optimize": True,
                    "progressive": True,
                }
            elif image_path.suffix.lower() == ".png":
                save_kwargs = {
                    "optimize": True,
                    "compress_level": 9,
                }

            working.save(output_path, format=opened.format, **save_kwargs)

        optimized_bytes = output_path.read_bytes()
        optimized_size = len(optimized_bytes)

        # Keep the original when optimization provides no meaningful gain.
        if optimized_size < original_size:
            files_changed += 1
            if not dry_run:
                image_path.write_bytes(optimized_bytes)

        output_path.unlink(missing_ok=True)

    bytes_after = bytes_before
    if files_changed:
        bytes_after = sum(path.stat().st_size for path in files)
        if dry_run:
            # Estimate post-optimization bytes from the computed per-file deltas.
            bytes_after = bytes_before
            for image_path in files:
                with Image.open(image_path) as opened:
                    working = _resize_if_needed(opened, max_dimension)
                    needs_mode_conversion = image_path.suffix.lower() in {
                        ".jpg",
                        ".jpeg",
                    } and working.mode not in {"RGB", "L"}
                    if needs_mode_conversion:
                        working = working.convert("RGB")

                    output_path = image_path.with_suffix(image_path.suffix + ".estimate")
                    save_kwargs: dict[str, bool | int | str] = {}
                    if image_path.suffix.lower() in {".jpg", ".jpeg"}:
                        save_kwargs = {
                            "quality": jpeg_quality,
                            "optimize": True,
                            "progressive": True,
                        }
                    elif image_path.suffix.lower() == ".png":
                        save_kwargs = {
                            "optimize": True,
                            "compress_level": 9,
                        }

                    working.save(output_path, format=opened.format, **save_kwargs)
                    optimized_size = output_path.stat().st_size
                    output_path.unlink(missing_ok=True)
                    original_size = image_path.stat().st_size
                    if optimized_size < original_size:
                        bytes_after -= original_size - optimized_size

    return OptimizationSummary(
        files_processed=files_processed,
        files_changed=files_changed,
        bytes_before=bytes_before,
        bytes_after=bytes_after,
    )