# Phase 0 — MVP DataToolkit

## Goal
Launch a functional MVP to validate real demand for a JSON ↔ CSV ↔ Excel conversion tool.

---

## MVP Features

### Supported Conversions

| Input | Output | Priority |
|-------|--------|----------|
| JSON | CSV | P0 |
| JSON | Excel (.xlsx) | P0 |
| CSV | JSON | P0 |
| Excel (.xlsx, .xls) | JSON | P1 |

### Characteristics

- [ ] **File upload**: drag & drop or file selector button
- [ ] **Data preview**: show first 10 rows in HTML table
- [ ] **Direct download**: converted file ready to download
- [ ] **No registration**: completely anonymous usage
- [ ] **No initial limits**: any (reasonable) size for now

---

## Technical Specifications

### JSON → CSV
- Input: Valid JSON (array of objects or object with array)
- Flatten first level of nesting
- First row = column names (JSON keys)
- Default delimiter: comma

### JSON → Excel
- Same process as CSV but generating .xlsx
- Single sheet named "Data"

### CSV → JSON
- First row = JSON keys
- Each following row = one object
- Output: array of objects
- Auto-detect delimiter (comma, semicolon, tab)

### Excel → JSON
- Read first sheet of file
- First row = keys
- Same output as CSV → JSON

---

## MVP UI/UX

### Main Screen
```
┌─────────────────────────────────────────────┐
│  🔄 DataToolkit                             │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │                                     │   │
│  │   Drop your file here              │   │
│  │   JSON, CSV or Excel               │   │
│  │                                     │   │
│  │   [Select file]                    │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### After File Upload
```
┌─────────────────────────────────────────────┐
│  📄 file.json (2.3 KB)                      │
│                                             │
│  Preview:                                   │
│  ┌─────────────────────────────────────┐   │
│  │ col1  │ col2   │ col3              │   │
│  │ val1  │ val2   │ val3              │   │
│  │ ...   │ ...    │ ...               │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Convert to:                                │
│  [CSV]  [Excel]                             │
│                                             │
│  [Upload another file]                      │
└─────────────────────────────────────────────┘
```

---

## File Structure

```
datatoolkit/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── converters/
│   │   ├── __init__.py
│   │   ├── json_to_csv.py
│   │   ├── json_to_excel.py
│   │   ├── csv_to_json.py
│   │   └── excel_to_json.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file_detection.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── tests/
│   ├── test_converters.py
│   └── sample_files/
│       ├── sample.json
│       ├── sample.csv
│       └── sample.xlsx
├── README.md
├── ROADMAP.md
├── PHASE0.md
└── STACK.md
```

---

## API Endpoints

### POST /convert
Single endpoint for all conversions.

**Request:**
- `file`: file to convert (multipart/form-data)
- `output_format`: desired format (`csv`, `xlsx`, `json`)

**Response:**
- Converted file for download
- Appropriate Content-Type

### POST /preview
Get file preview without converting.

**Request:**
- `file`: file to preview

**Response:**
```json
{
  "columns": ["col1", "col2", "col3"],
  "rows": [
    ["val1", "val2", "val3"],
    ["val4", "val5", "val6"]
  ],
  "total_rows": 150,
  "detected_type": "json"
}
```

---

## Development Tasks

### Backend (3-5 days)
- [ ] Setup FastAPI project
- [ ] Implement json_to_csv.py
- [ ] Implement json_to_excel.py
- [ ] Implement csv_to_json.py
- [ ] Implement excel_to_json.py
- [ ] Implement automatic file type detection
- [ ] Implement /convert endpoint
- [ ] Implement /preview endpoint
- [ ] Basic tests for each converter
- [ ] Error handling (invalid file, malformed JSON, etc.)

### Frontend (2-3 days)
- [ ] Basic HTML structure
- [ ] Clean and minimalist CSS styles
- [ ] JS: file drag & drop
- [ ] JS: call /preview and display table
- [ ] JS: call /convert and trigger download
- [ ] Loading states (spinner)
- [ ] User-friendly error messages

### DevOps (1 day)
- [ ] Setup Git repository
- [ ] Configure deploy on Railway/Render/Fly.io
- [ ] Domain (can be free subdomain initially)
- [ ] HTTPS

---

## "Done" Criteria for Phase 0

- [ ] I can upload a JSON and download CSV
- [ ] I can upload a JSON and download Excel
- [ ] I can upload a CSV and download JSON
- [ ] I can upload an Excel and download JSON
- [ ] I see a preview of my data before converting
- [ ] The web is deployed and publicly accessible
- [ ] Works on mobile (basic responsive)
- [ ] No obvious errors in console

---

## Out of Scope (Phase 0)

- User registration
- Size limits
- Multiple files at once
- Complex nested JSON
- Delimiter selection
- Advanced analytics
- Documented public API
