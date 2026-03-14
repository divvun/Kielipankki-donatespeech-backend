"""Tests for Excel-to-JSON content conversion."""

import json
from pathlib import Path

import pytest

from convert_excel_to_json import WorkbookStructureError, convert_workbook
from models import Schedule, Theme


Workbook = pytest.importorskip("openpyxl").Workbook


def _create_workbook(path: Path, include_invalid_item: bool = False, include_items: bool = True) -> None:
    workbook = Workbook()

    schedule_meta = workbook.active
    schedule_meta.title = "ScheduleMeta"
    schedule_headers = [
        "scheduleId",
        "start_title_fi",
        "start_title_nb",
        "start_body1_fi",
        "start_body1_nb",
        "start_body2_fi",
        "start_body2_nb",
        "start_imageUrl",
        "finish_title_fi",
        "finish_title_nb",
        "finish_body1_fi",
        "finish_body1_nb",
        "finish_body2_fi",
        "finish_body2_nb",
        "finish_imageUrl",
    ]
    schedule_meta.append(schedule_headers)
    schedule_meta.append(
        [
            "schedule-001",
            "Aloitetaan",
            "Start",
            "Kuvaus",
            "Description",
            "",
            "",
            "https://example.org/start.jpg",
            "Valmis",
            "Done",
            "Kiitos",
            "Thanks",
            "",
            "",
            "https://example.org/finish.jpg",
        ]
    )

    if include_items:
        items = workbook.create_sheet("Items")
        item_headers = [
            "order",
            "itemId",
            "kind",
            "itemType",
            "url",
            "typeId",
            "isRecording",
            "default_title_fi",
            "default_title_nb",
            "default_body1_fi",
            "default_body1_nb",
            "default_body2_fi",
            "default_body2_nb",
            "default_imageUrl",
            "finish_title_fi",
            "finish_title_nb",
            "finish_body1_fi",
            "finish_body1_nb",
            "finish_body2_fi",
            "finish_body2_nb",
            "finish_imageUrl",
            "metaTitle_fi",
            "metaTitle_nb",
            "otherAnswer_fi",
            "otherAnswer_nb",
            "otherEntryLabel_fi",
            "otherEntryLabel_nb",
        ]
        items.append(item_headers)

        items.append(
            [
                1,
                "image-001",
                "media",
                "image",
                "https://example.org/image.jpg",
                "image/jpeg",
                True,
                "Kuva",
                "Bilde",
                "Kuvan kuvaus",
                "Bildeforklaring",
                "",
                "",
                "https://example.org/default.jpg",
                "Hienoa",
                "Bra",
                "Jatketaan",
                "Fortsett",
                "",
                "",
                "https://example.org/finish-item.jpg",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )

        items.append(
            [
                2,
                "choice-001",
                "prompt",
                "choice",
                "https://example.org/prompt.png",
                "",
                False,
                "Valitse",
                "Velg",
                "Valitse yksi",
                "Velg en",
                "",
                "",
                "https://example.org/prompt-default.jpg",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )

        if include_invalid_item:
            items.append(
                [
                    3,
                    "",
                    "media",
                    "audio",
                    "",
                    "audio/m4a",
                    "maybe",
                    "Ääni",
                    "Lyd",
                    "Kuvaus",
                    "Beskrivelse",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )

        options = workbook.create_sheet("ItemOptions")
        options.append(["itemId", "optionIndex", "option_fi", "option_nb"])
        options.append(["choice-001", 0, "Vaihtoehto A", "Alternativ A"])
        options.append(["choice-001", 1, "Vaihtoehto B", "Alternativ B"])

    theme = workbook.create_sheet("Theme")
    theme_headers = [
        "themeId",
        "title_fi",
        "title_nb",
        "body1_fi",
        "body1_nb",
        "body2_fi",
        "body2_nb",
        "image",
    ]
    theme.append(theme_headers)
    theme.append(
        [
            "theme-001",
            "Teema",
            "Tema",
            "Teeman kuvaus",
            "Tema beskrivelse",
            "",
            "",
            "https://example.org/theme.jpg",
        ]
    )

    theme_schedules = workbook.create_sheet("ThemeSchedules")
    theme_schedules.append(["scheduleId"])
    theme_schedules.append(["schedule-001"])

    workbook.save(path)


def test_convert_workbook_generates_schedule_and_theme(tmp_path: Path) -> None:
    workbook_path = tmp_path / "content.xlsx"
    output_root = tmp_path / "content"
    _create_workbook(workbook_path)

    result = convert_workbook(
        workbook_path=workbook_path,
        output_env="dev",
        content_root=output_root,
    )

    schedule_path = Path(result.schedule_path)
    theme_path = Path(result.theme_path) if result.theme_path else None

    assert schedule_path.exists()
    assert theme_path is not None
    assert theme_path.exists()

    with open(schedule_path, "r", encoding="utf-8") as schedule_file:
        schedule_data = json.load(schedule_file)
    parsed_schedule = Schedule(**schedule_data)
    assert parsed_schedule.scheduleId == "schedule-001"
    assert len(parsed_schedule.items) == 2

    choice_item = next(item for item in parsed_schedule.items if item.itemId == "choice-001")
    assert len(choice_item.options) == 2

    with open(theme_path, "r", encoding="utf-8") as theme_file:
        theme_data = json.load(theme_file)
    parsed_theme = Theme(**theme_data)
    assert parsed_theme.scheduleIds == ["schedule-001"]


def test_convert_workbook_best_effort_skips_invalid_rows(tmp_path: Path) -> None:
    workbook_path = tmp_path / "content_with_invalid_rows.xlsx"
    output_root = tmp_path / "content"
    _create_workbook(workbook_path, include_invalid_item=True)

    result = convert_workbook(
        workbook_path=workbook_path,
        output_env="dev",
        content_root=output_root,
    )

    assert any(row.sheet == "Items" for row in result.skipped_rows)

    with open(result.schedule_path, "r", encoding="utf-8") as schedule_file:
        schedule_data = json.load(schedule_file)
    parsed_schedule = Schedule(**schedule_data)

    assert len(parsed_schedule.items) == 2
    assert all(item.itemId for item in parsed_schedule.items)


def test_convert_workbook_strict_fails_when_rows_skipped(tmp_path: Path) -> None:
    workbook_path = tmp_path / "content_strict.xlsx"
    output_root = tmp_path / "content"
    _create_workbook(workbook_path, include_invalid_item=True)

    with pytest.raises(WorkbookStructureError, match="Strict mode enabled"):
        convert_workbook(
            workbook_path=workbook_path,
            output_env="dev",
            content_root=output_root,
            strict=True,
        )


def test_convert_workbook_missing_items_sheet_fails(tmp_path: Path) -> None:
    workbook_path = tmp_path / "content_missing_items.xlsx"
    output_root = tmp_path / "content"
    _create_workbook(workbook_path, include_items=False)

    with pytest.raises(WorkbookStructureError, match="Missing required sheet: Items"):
        convert_workbook(
            workbook_path=workbook_path,
            output_env="dev",
            content_root=output_root,
        )
