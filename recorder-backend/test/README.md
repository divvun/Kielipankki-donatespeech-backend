# Test Data Files

This directory contains test JSON files for local development.

## Files

- **playlist.json**: Sample schedule with various item types (audio, video, YLE media, prompts)
- **theme.json**: Sample theme definition

## Format

These files use the **new format** (without `kind` field). The old format from the `fromsam` branch has been converted using `convert_schedule.py`.

### Conversion from Old Format

The old format (with `kind` and `itemType` fields) has been converted to the new simplified format:

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

These files are automatically uploaded to the Azurite blob storage when running `setup-local.sh`:

- `test/playlist.json` → `schedule/test-playlist.json`
- `test/theme.json` → `theme/test-theme.json`

## Converting Additional Files

To convert old-format JSON files to the new format:

```bash
./convert_schedule.py <old-file.json> <new-file.json>
```
