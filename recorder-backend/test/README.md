# Test Data Files

This directory contains test JSON files for local development.

## Files

- **0b5cf885-5049-4e7a-83e0-05a63be53639.json**: Sample schedule with various
  item types (audio, video, prompts)
- **8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9.json**: Sample theme definition

**Note:** Files are named with UUIDs to match production naming conventions.
The UUID becomes the resource ID when uploaded to blob storage.

## Format

These files use the **new format** (without `kind` field). The old format from
the `fromsam` branch has been converted using `convert_schedule.py`.

### Conversion from Old Format

The old format (with `kind` and `itemType` fields) has been converted to the new
simplified format:

**Old Format:**
```json
{
  "itemId": "...",
  "kind": "media",
  "itemType": "audio",
  "typeId": "audio/m4a",
  "url": "...",
  "options": [],
  ...
}
```

**New Format:**
```json
{
  "itemId": "...",
  "itemType": "audio",
  "typeId": "audio/m4a",
  "url": "...",
  ...
}
```

### Item Type Changes

- Media `text` → `text-content` (to avoid conflict with prompt text-input)
- Prompt `text` → `text-input`
- Removed `kind` field from all items
- Removed `options` field from all media items
- Removed `typeId` from YLE media items (always None)
- Removed `typeId` and `url` from prompt items (always None/unused)

## Usage

These files are automatically uploaded to the Azurite blob storage when running
`setup-local.sh`:

- `test/0b5cf885-5049-4e7a-83e0-05a63be53639.json` →
  `schedule/0b5cf885-5049-4e7a-83e0-05a63be53639.json` (Schedule ID:
  `0b5cf885-5049-4e7a-83e0-05a63be53639`)
- `test/8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9.json` →
  `theme/8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9.json` (Theme ID:
  `8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9`)

Access via API:
```bash
curl http://localhost:8000/v1/schedule/0b5cf885-5049-4e7a-83e0-05a63be53639
curl http://localhost:8000/v1/theme/8d147f2c-9a3b-4e5d-b2c1-45a8f7e3c6d9
```

## Converting Additional Files

To convert old-format JSON files to the new format:

```bash
./convert_schedule.py <old-file.json> <new-file.json>
```
