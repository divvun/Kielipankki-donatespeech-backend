#!/usr/bin/env python3
"""Validate one theme JSON file using backend Pydantic Theme model."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError


@dataclass
class ValidationIssue:
    file_path: Path
    message: str


@dataclass
class ValidationResult:
    files_checked: int
    issues: list[ValidationIssue]


def _import_theme_model() -> type:
    try:
        from app.models import Theme  # type: ignore[import-untyped]
    except Exception as exc:  # pragma: no cover - import boundary
        raise RuntimeError(
            "Could not import Theme model. Ensure kielipankki-recorder-backend is installed."
        ) from exc

    return Theme


def validate_content_json(theme_file: Path) -> ValidationResult:
    issues: list[ValidationIssue] = []
    resolved_theme_file = theme_file.resolve()

    if not resolved_theme_file.exists():
        issues.append(
            ValidationIssue(
                file_path=resolved_theme_file,
                message="Theme file not found.",
            )
        )
        return ValidationResult(files_checked=0, issues=issues)

    try:
        payload = json.loads(resolved_theme_file.read_text(encoding="utf-8"))
    except Exception as exc:
        issues.append(
            ValidationIssue(
                file_path=resolved_theme_file,
                message=f"Invalid JSON: {exc}",
            )
        )
        return ValidationResult(files_checked=1, issues=issues)

    if not isinstance(payload, dict):
        issues.append(
            ValidationIssue(
                file_path=resolved_theme_file,
                message="Theme JSON root must be an object.",
            )
        )
        return ValidationResult(files_checked=1, issues=issues)

    try:
        theme_model = _import_theme_model()
        theme_model(**payload)
    except RuntimeError as exc:
        issues.append(
            ValidationIssue(
                file_path=resolved_theme_file,
                message=str(exc),
            )
        )
    except ValidationError as exc:
        issues.append(
            ValidationIssue(
                file_path=resolved_theme_file,
                message=str(exc),
            )
        )

    return ValidationResult(files_checked=1, issues=issues)


def main(theme_dir: Path) -> int:
    for theme_file in theme_dir.glob("themes/*/*.json"):
        result = validate_content_json(theme_file)
        if not result.issues:
            continue

        print(f"Validation failed with {len(result.issues)} issues:")
        for issue in result.issues:
            print(f"- {issue.file_path}: {issue.message}")
        return 1

    print("Validation passed")
    return 0