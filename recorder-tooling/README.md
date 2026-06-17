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

   Note: `validate-json` imports the Pydantic `Theme` model from the sibling
   `../recorder-backend` project via a local uv source dependency.

2. Activate the environment:

   ```sh
   source .venv/bin/activate
   ```

## Example Scripts

- src/recorder_tooling/convert_excel_to_json.py
- src/recorder_tooling/migrate_storage.py
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

Validate JSON content:

```sh
uv run recorder-tooling validate-json --content-root ../recorder-content/dev
```

Optional flags mirror the original script:

```sh
uv run recorder-tooling convert-xlsx path/to/workbook.xlsx \
   --output-root ../recorder-content/dev/themes \
   --overwrite
```

Direct script usage is still supported:

```sh
python -m recorder_tooling.convert_excel_to_json path/to/workbook.xlsx
```

Other utilities:

```sh
python -m recorder_tooling.fill_schedule_uuids path/to/schedule.json --dry-run
python -m recorder_tooling.convert_schedule old_schedule.json new_schedule.json
python -m recorder_tooling.migrate_storage --lang fi --lang nb
python -m recorder_tooling.replace_itemid path/to/schedule.json
```
