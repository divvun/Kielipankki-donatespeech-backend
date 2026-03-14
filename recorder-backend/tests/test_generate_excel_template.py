"""Tests for starter workbook template generation."""

from pathlib import Path

import pytest

from generate_excel_template import (
    ITEM_HEADERS,
    ITEM_OPTIONS_HEADERS,
    SCHEDULE_META_HEADERS,
    SHEET_ITEMS,
    SHEET_ITEM_OPTIONS,
    SHEET_SCHEDULE_META,
    SHEET_THEME,
    SHEET_THEME_SCHEDULES,
    THEME_HEADERS,
    THEME_SCHEDULE_HEADERS,
    create_template_workbook,
)


load_workbook = pytest.importorskip("openpyxl").load_workbook


def _row_values(sheet, row_index: int, count: int) -> list[str | None]:
    return [sheet.cell(row=row_index, column=idx).value for idx in range(1, count + 1)]


def test_create_template_workbook_contains_expected_sheets_and_headers(tmp_path: Path) -> None:
    output_path = tmp_path / "template.xlsx"
    create_template_workbook(output_path)

    workbook = load_workbook(output_path)

    expected_sheet_order = [
        SHEET_SCHEDULE_META,
        SHEET_ITEMS,
        SHEET_ITEM_OPTIONS,
        SHEET_THEME,
        SHEET_THEME_SCHEDULES,
    ]
    assert workbook.sheetnames == expected_sheet_order

    schedule_sheet = workbook[SHEET_SCHEDULE_META]
    assert _row_values(schedule_sheet, 1, len(SCHEDULE_META_HEADERS)) == SCHEDULE_META_HEADERS

    items_sheet = workbook[SHEET_ITEMS]
    assert _row_values(items_sheet, 1, len(ITEM_HEADERS)) == ITEM_HEADERS

    options_sheet = workbook[SHEET_ITEM_OPTIONS]
    assert _row_values(options_sheet, 1, len(ITEM_OPTIONS_HEADERS)) == ITEM_OPTIONS_HEADERS

    theme_sheet = workbook[SHEET_THEME]
    assert _row_values(theme_sheet, 1, len(THEME_HEADERS)) == THEME_HEADERS

    theme_schedules_sheet = workbook[SHEET_THEME_SCHEDULES]
    assert _row_values(theme_schedules_sheet, 1, len(THEME_SCHEDULE_HEADERS)) == THEME_SCHEDULE_HEADERS


def test_create_template_workbook_refuses_overwrite_without_force(tmp_path: Path) -> None:
    output_path = tmp_path / "template.xlsx"
    create_template_workbook(output_path)

    with pytest.raises(FileExistsError, match="Use --force"):
        create_template_workbook(output_path)


def test_create_template_workbook_overwrites_with_force(tmp_path: Path) -> None:
    output_path = tmp_path / "template.xlsx"
    create_template_workbook(output_path)

    # Corrupt the file and confirm force creates a valid workbook again.
    output_path.write_text("invalid", encoding="utf-8")
    create_template_workbook(output_path, overwrite=True)

    workbook = load_workbook(output_path)
    assert workbook.sheetnames[0] == SHEET_SCHEDULE_META
