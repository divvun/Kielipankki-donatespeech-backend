# Recorder Tooling

This directory contains scripts and utilities for managing and converting
content for the Kielipankki speech donation project.

- Use a separate Python environment (managed by uv) for tooling dependencies.
- Place all conversion, validation, and content organization scripts here.

## Setup

1. Install dependencies:

   ```sh
   uv sync
   ```

2. Activate the environment:

   ```sh
   source .venv/bin/activate
   ```

## Example Scripts

- convert_excel_to_json.py
- migrate_storage.py
- ...

## CLI

Use the central CLI entrypoint:

```sh
uv run recorder-tooling --help
```

First command (Excel -> JSON conversion):

```sh
uv run recorder-tooling convert-xlsx path/to/workbook.xlsx
```

Storage commands:

```sh
uv run recorder-tooling storage init
uv run recorder-tooling storage cleanup
```

Optional flags mirror the original script:

```sh
uv run recorder-tooling convert-xlsx path/to/workbook.xlsx \
   --output-root ../recorder-content/dev/themes \
   --overwrite
```

Direct script usage is still supported:

```sh
python convert_excel_to_json.py path/to/workbook.xlsx
```
