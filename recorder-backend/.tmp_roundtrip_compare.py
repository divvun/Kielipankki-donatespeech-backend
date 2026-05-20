import json
import shutil
from pathlib import Path

from convert_excel_to_json import convert_workbook

ROOT = Path(__file__).resolve().parent
WORKBOOKS = sorted((ROOT / "examples" / "prod").glob("schedule-*.xlsx"))
OUT_ROOT = ROOT / "examples" / "converted-json-after-edit"

if OUT_ROOT.exists():
    shutil.rmtree(OUT_ROOT)

for workbook in WORKBOOKS:
    convert_workbook(
        workbook_path=workbook,
        output_env="prod",
        content_root=OUT_ROOT,
        strict=False,
    )


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def first_diff(expected, actual, path="$"):
    if type(expected) != type(actual):
        return {
            "path": path,
            "reason": "type-mismatch",
            "expected_type": type(expected).__name__,
            "actual_type": type(actual).__name__,
        }

    if isinstance(expected, dict):
        expected_keys = set(expected)
        actual_keys = set(actual)
        if expected_keys != actual_keys:
            return {
                "path": path,
                "reason": "key-mismatch",
                "only_expected": sorted(expected_keys - actual_keys),
                "only_actual": sorted(actual_keys - expected_keys),
            }
        for key in sorted(expected_keys):
            diff = first_diff(expected[key], actual[key], f"{path}.{key}")
            if diff:
                return diff
        return None

    if isinstance(expected, list):
        if len(expected) != len(actual):
            return {
                "path": path,
                "reason": "length-mismatch",
                "expected_len": len(expected),
                "actual_len": len(actual),
            }
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            diff = first_diff(expected_item, actual_item, f"{path}[{index}]")
            if diff:
                return diff
        return None

    if expected != actual:
        return {
            "path": path,
            "reason": "value-mismatch",
            "expected": expected,
            "actual": actual,
        }

    return None


report = {
    "workbook_count": len(WORKBOOKS),
    "summary": {
        "schedule_matches": 0,
        "schedule_mismatches": 0,
        "theme_matches": 0,
        "theme_mismatches": 0,
    },
    "mismatches": {
        "schedules": {},
        "themes": {},
    },
}

expected_schedule_dir = ROOT / "content" / "prod" / "schedules"
actual_schedule_dir = OUT_ROOT / "prod" / "schedules"
for expected_path in sorted(expected_schedule_dir.glob("*.json")):
    actual_path = actual_schedule_dir / expected_path.name
    if not actual_path.exists():
        report["summary"]["schedule_mismatches"] += 1
        report["mismatches"]["schedules"][expected_path.stem] = {
            "path": "$",
            "reason": "missing-file",
        }
        continue

    diff = first_diff(load_json(expected_path), load_json(actual_path))
    if diff:
        report["summary"]["schedule_mismatches"] += 1
        report["mismatches"]["schedules"][expected_path.stem] = diff
    else:
        report["summary"]["schedule_matches"] += 1

expected_theme_dir = ROOT / "content" / "prod" / "themes"
actual_theme_dir = OUT_ROOT / "prod" / "themes"
for expected_path in sorted(expected_theme_dir.glob("*.json")):
    actual_path = actual_theme_dir / expected_path.name
    if not actual_path.exists():
        report["summary"]["theme_mismatches"] += 1
        report["mismatches"]["themes"][expected_path.stem] = {
            "path": "$",
            "reason": "missing-file",
        }
        continue

    diff = first_diff(load_json(expected_path), load_json(actual_path))
    if diff:
        report["summary"]["theme_mismatches"] += 1
        report["mismatches"]["themes"][expected_path.stem] = diff
    else:
        report["summary"]["theme_matches"] += 1

report_path = OUT_ROOT / "compare-vs-prod.json"
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(
    json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)

print(f"wrote: {report_path}")
print(json.dumps(report["summary"], ensure_ascii=False))
