#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import typer

from convert_excel_to_json import convert_workbook

app = typer.Typer(help="Central CLI for recorder tooling scripts.", no_args_is_help=True)


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


if __name__ == "__main__":
    app()
