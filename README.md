# ParseWiz

Free online tool for converting, previewing, and cleaning tabular data between JSON, CSV, and Excel formats. No registration required.

**[www.parsewiz.app](https://www.parsewiz.app)**

## What it does

Upload a file, preview the data, and convert it to another format. ParseWiz handles edge cases like complex nested JSON, malformed files (with an inline editor to fix errors), and legacy Excel formats.

## Features

- **All conversions**: JSON ↔ CSV, JSON ↔ Excel, CSV ↔ Excel (including legacy .xls)
- **Data preview**: paginated HTML table before converting
- **Complex JSON handling**: automatic detection of nested arrays with three export modes:
  - Normal (cartesian product expansion)
  - Multi-table (separate sheets with record ID linking)
  - Single-row (arrays kept as JSON strings)
- **Inline error editor**: fix malformed JSON/CSV directly in the browser with line numbers and error location
- **Drag & drop** file upload
- **PWA**: installable and works offline
- **Privacy-first**: no authentication, no data stored server-side

## Tech stack

| Component | Technology |
|---|---|
| Backend | Python + FastAPI |
| Frontend | Vanilla JS + HTML + CSS |
| Data processing | pandas + openpyxl + xlrd |
| Package manager | uv |
| Tests | pytest (91 tests) |
| Deployment | Railway |

## Quick start

### Install

```bash
uv sync
```

### Run

```bash
uv run uvicorn backend.main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser.

### Tests

```bash
uv run pytest tests/ -v
```

### Code quality

```bash
uv run ruff format backend/
uv run ruff check backend/ --fix
```

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/convert` | Convert a file to the target format |
| POST | `/api/preview` | Preview file contents as paginated table |
| POST | `/api/analyze` | Analyze JSON complexity (nested arrays) |
| POST | `/api/preview-all-tables` | Preview all tables from complex JSON |
| POST | `/api/feedback` | Send user feedback |
| GET | `/api/health` | Health check |

## Environment variables

| Variable | Description |
|---|---|
| `ENVIRONMENT` | `production` or `development` (default) |
| `ALLOWED_ORIGINS` | CORS origins (default: `*`) |
| `MAX_FILE_SIZE_MB` | Max upload size (default: 10) |
| `DISCORD_WEBHOOK_URL` | Feedback webhook |

## License

All rights reserved.
