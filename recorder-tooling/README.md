# Recorder Tooling

This directory contains scripts and utilities for managing and converting content for the Kielipankki speech donation project.

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
