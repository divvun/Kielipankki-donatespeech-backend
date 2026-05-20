# Project Structure: Three-Directory Organization

This project is now organized into three separate, parallel directories with independent responsibilities:

## Directory Structure

```
Kielipankki-donatespeech-backend/
├── recorder-backend/          # FastAPI application (main backend)
├── recorder-tooling/          # Content conversion and management scripts
└── recorder-content/          # Content files (themes, media, excel source)
```

## Directory Details

### 1. `recorder-backend/` — FastAPI Application

**Purpose:** Core speech donation recorder application.

**Contents:**
- `app/` — FastAPI application code
- `tests/` — Unit and integration tests
- `pyproject.toml` — Backend dependencies (FastAPI, uvicorn, etc.)
- `.venv/` — Virtual environment (created by `uv sync`)

**Setup:**
```bash
cd recorder-backend
uv sync
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 2. `recorder-tooling/` — Content Management Tools

**Purpose:** Scripts for converting, generating, and managing content files.

**Contents:**
- `convert_excel_to_json.py` — Convert Excel worksheets to theme JSON files
- `convert_schedule.py` — Convert between schedule format versions
- `init-storage.py` — Initialize Azurite or Azure Blob Storage with content
- `migrate-storage.py` — Migrate storage layout (flat → per-language)
- `fill_schedule_uuids.py` — Generate or fill UUID fields in schedules
- `cleanup-storage.py` — Clean up blob storage
- `custom_fleep/` — Custom file type detection utility
- `example-theme.csv` — Example content creation template
- `pyproject.toml` — Tooling dependencies (openpyxl, azure-storage-blob, etc.)

**Setup:**
```bash
cd recorder-tooling
uv sync
source .venv/bin/activate

# Example: Convert Excel to JSON
python convert_excel_to_json.py ../recorder-content/dev/your-theme.xlsx

# Example: Initialize local storage
python init-storage.py  # Uses ../recorder-content/dev/
```

### 3. `recorder-content/` — Content Repository

**Purpose:** Stores content files (themes, media, excel source).

**Structure:**
```
recorder-content/
├── dev/              # Development content
│   ├── excel/        # Source Excel files (input for tooling)
│   ├── themes/       # Generated theme JSON files
│   └── media/        # Images, audio, video files
├── json/             # Alternative output directory for generated JSON
├── media/            # Central media storage
└── excel/            # Central Excel storage
```

**Key Files:**
- Theme JSON: `dev/themes/<uuid>/<lang>.json`
- Media files: `dev/media/<filename>`
- Source Excel: `dev/excel/<filename>.xlsx`

## Workflow Example

### Creating New Content

1. **Create Excel source file** in `recorder-content/dev/excel/`
   - Use `recorder-tooling/example-theme.csv` as reference

2. **Convert Excel to JSON** from `recorder-tooling/`:
   ```bash
   cd recorder-tooling
   python convert_excel_to_json.py ../recorder-content/dev/my-theme.xlsx
   ```
   
3. **Output** is written to: `recorder-content/dev/themes/<uuid>/<lang>.json`

4. **Initialize storage** to Azurite or Azure:
   ```bash
   cd recorder-tooling
   python init-storage.py
   ```

### Running Backend with New Content

1. Ensure content is in `recorder-content/dev/` or `recorder-content/prod/`

2. Start storage (Azurite) or connect to Azure via env vars

3. Initialize blob storage:
   ```bash
   cd recorder-tooling
   python init-storage.py
   ```

4. Start backend:
   ```bash
   cd recorder-backend
   uvicorn app.main:app --reload --port 8000
   ```

## Dependencies & Package Management

Each directory is independently managed with `uv`:

- **recorder-backend**: FastAPI, Uvicorn, Pydantic, Azure Blob Storage SDK
- **recorder-tooling**: OpenPyXL, Azure Blob Storage SDK, PyYAML, Pydantic
- **recorder-content**: No dependencies (static content)

To update dependencies:
```bash
cd <directory>
uv sync                  # Install/update
uv lock --upgrade        # Upgrade versions
source .venv/bin/activate
```

## Future: Git LFS for Media

When `recorder-content/` is converted to a separate repository, configure git-lfs for binary files:

```bash
git lfs install
git lfs track "*.jpg" "*.png" "*.mp3" "*.mp4" "*.wav"
```

## Troubleshooting

### "Module not found" errors
- Ensure you're in the correct directory before running scripts
- Ensure `uv sync` was run in that directory

### "Content directory not found"
- Check that paths in tooling scripts are correct (should use `../recorder-content/`)
- Verify you're running scripts from `recorder-tooling/` directory

### Backend can't find content
- Verify `recorder-content/dev/` or `recorder-content/prod/` exists
- Check `init-storage.py` has uploaded content to Azurite/Azure
- Check blob storage connection settings (env vars)
