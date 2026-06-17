#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import typer

from .cleanup_storage import main as cleanup_storage_main
from .count_missing_translations import write_multilang_workbook_json
from .convert_excel_to_json import convert_workbook
from .init_storage import main as init_storage_main
from .validate_content_json import main as validate_content_json_main
from .lang_json import read_json

app = typer.Typer(help="Central CLI for recorder tooling scripts.", no_args_is_help=True)
storage_app = typer.Typer(help="Storage management commands.", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Recorder tooling command group."""


@app.command("convert-xlsx")
def convert_xlsx(
    input_xlsx: Path = typer.Argument(
        ..., help="Input workbook path, for example uit-export.xlsx"
    ),
    output_root: Path = typer.Option(
        Path("../recorder-content/dev/themes"),
        "--output-root",
        help="Output themes root directory",
    ),
    overwrite: bool = typer.Option(
        False,
        "--overwrite",
        help="Overwrite existing output files",
    ),
) -> None:
    """Convert XLSX theme sheets to language-specific theme JSON files."""
    if not input_xlsx.exists():
        raise typer.BadParameter(f"Input workbook not found: {input_xlsx}")

    try:
        written = convert_workbook(
            input_xlsx=input_xlsx,
            output_root=output_root,
            overwrite=overwrite,
        )
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Wrote {len(written)} files")
    for path in written:
        typer.echo(str(path))


@app.command("count-missing-translations")
def count_missing_translations(
    input_xlsx: Path = typer.Argument(
        ..., help="Input workbook path, for example uit-export.xlsx"
    ),
) -> None:
    """Write one multi-language JSON per worksheet to the current directory."""
    if not input_xlsx.exists():
        raise typer.BadParameter(f"Input workbook not found: {input_xlsx}")

    try:
        written = write_multilang_workbook_json(input_xlsx, Path.cwd())
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Wrote {len(written)} files")
    for path in written:
        typer.echo(str(path))


@app.command("create-translation-sheet")
def create_translation_sheet(
    input_json: Path = typer.Argument(
        ..., help="Input json file path, for example themes/uit.json"
    ),
) -> None:
    """Create a new translation sheet in the workbook."""
    if not input_json.exists():
        raise typer.BadParameter(f"Input json file not found: {input_json}")

    print(f"Reading JSON from {input_json}...")
    results = read_json(input_json)
    
    print_results = set()
    for result in results:
        print_values = "\t".join(result)
        if print_values.strip():
            print_results.add(print_values)
    stem = input_json.stem
    stem_lang = {
        "d51f3f30-aa22-4e57-9cc9-c806458e4724": "lule",
        "6a7e2678-8207-4878-8f58-d527fc2e0c8c": "syd",
        "2690f660-be92-4f5a-a120-dd35725bac96": "pite",
        "8baa307a-a03a-4d8d-8bb0-a6f5932f1a6f": "skolt",
        "35398c39-f574-4350-9093-798644a95ae": "ume",
        "6e73a4d9-cb16-462f-b957-ac679486f1e7": "inari"
    }
    Path(stem_lang.get(stem, stem) + ".csv").write_text("\n".join(sorted(r.strip() if r.strip() else r for r in print_results)), encoding="utf-8")
    print(f"Total missing translations: {len(print_results)}")



@app.command("validate-json")
def validate_json(
    content_root: Path = typer.Option(
        Path("../recorder-content/dev"),
        "--content-root",
        help="Content root containing themes/, schedules/, and media/",
    ),
    media_dir: Path | None = typer.Option(
        None,
        "--media-dir",
        help="Optional override path for media directory",
    ),
) -> None:
    """Validate content JSON UUID collisions and media URL references."""
    raise typer.Exit(code=validate_content_json_main(content_root))


@storage_app.command("init")
def storage_init() -> None:
    """Initialize storage with recorder content."""
    raise typer.Exit(code=init_storage_main())


@storage_app.command("cleanup")
def storage_cleanup() -> None:
    """Clean up blobs from storage container."""
    raise typer.Exit(code=cleanup_storage_main())


app.add_typer(storage_app, name="storage")


if __name__ == "__main__":
    app()
