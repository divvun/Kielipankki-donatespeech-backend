#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import typer

from cleanup_storage import main as cleanup_storage_main
from convert_excel_to_json import convert_workbook
from init_storage import main as init_storage_main

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
