# Content identifiers

## Schedules

| `scheduleId` | Schedule name |
| ------------- | ------------- |
| 3a73d87a-8856-4ca0-9af2-da66c99a95f9 | Eläimet |
| 8aaf82be-de16-4449-9fd2-677291a0e804 | Urheilu |
| 0598bf14-ab48-4ccb-a50c-0bd779f77933 | Lähelläni juuri nyt |
| 664bc028-a92f-435f-8e33-9ab4921476c1 | Kesä |
| f5c5fd20-34f9-4ff8-bdba-666bbf1740ce | Kerro korona-ajasta |
| 92d22fe6-ae1d-448a-b17d-d8ac9f274f56 | Mediataidot lukio |
| e6433174-6e3c-470c-8e63-b2ef2335e26a | Mediataidot 8-9 |
| f5c74c5e-e19c-47f6-beff-9631d9c7b6d6 | Mediataidot 4-6 |
| 6975c4b9-b40e-42e7-9572-05eeab25452b | K-18 |
| cbb91217-b323-46d7-b3af-16c41206c60d | Luonto |

## Metadata items

| `itemId` | Item purpose | Item type | Remarks |
| -------- | ------------ | --------- | ------- |
| 88acf16d-9180-47ef-a003-e1571048c701 | Occupation | `prompt` / `text` | Ammatti (v2) |
| 5103c614-1df4-4ffd-a670-30ef78e0a613 | Education | `prompt` / `choice` | Koulutus (v2) |
| 6ef34957-41e7-487e-aa0c-a40c93ed9251 | Dialect | `prompt` / `choice` | Murretausta |
| e3264046-a642-46de-a9e7-c55933ee3739 | Age | `prompt` / `choice` | Ikä |
| 8bbb8e5d-56a2-4082-9429-233ff2a5e53f | Gender | `prompt` / `choice` | Sukupuoli |
| fa3ecb10-1128-4c8c-a838-600a0faadc2e | Native language | `prompt` / `multi-choice` | Äidinkieli |
| a9a3d87b-49cf-4015-8953-7a5c96abefb9 | Health issues | `prompt` / `text` | Terveydelliset tekijät |
| 626d3fb5-6b82-4d5d-bdde-1637e571ca28 | Place of residence | `prompt` / `super-choice` | Asuinpaikka (v2) |
| dad311ea-3e7f-4d16-b76b-0c94aaf9fc73 | Place of birth | `prompt` / `super-choice` | Syntymäpaikka (v2) |
| 365c78ae-0ff3-4331-99df-9a8c18ba6e7f | Company challenge | `prompt` / `text` | Firmahaaste (v2) |

For the `choice`, `multi-choice` and `super-choice` item types, the choices and other related content
are included in the schedule description JSON file.

## Miscellaneous

To create a new identifier, make a UUID v4 with a time-based component.
Please use only all lower case identifiers.

For example, in the macOS Terminal, issue the command:

    uuidgen | tr '[:upper:]' '[:lower:]'

This generates a new UUID v4 and converts it from upper case to lower case.
