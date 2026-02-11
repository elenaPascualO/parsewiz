# ParseWiz — General Roadmap

## Vision
Web tool for conversion, cleaning, and manipulation of tabular data (JSON, CSV, Excel). Start simple, grow with features that deliver real value.

---

## Phase 0 — MVP (Complete)

**Goal:** Launch a functional MVP to validate real demand for a JSON / CSV / Excel conversion tool.
**Status:** Complete (January 2026) - 91 tests passing. Deployed pending.

### Supported Conversions

| Input | Output | Priority |
|-------|--------|----------|
| JSON | CSV | P0 |
| JSON | Excel (.xlsx) | P0 |
| CSV | JSON | P0 |
| CSV | Excel (.xlsx) | P0 |
| Excel (.xlsx, .xls) | JSON | P1 |
| Excel (.xlsx, .xls) | CSV | P1 |

### Features
- [x] Data preview with pagination
- [x] Nested JSON array expansion (Cartesian product)
- [x] Smart JSON handling (multi-table export, single-row export)
- [x] Raw editor for malformed files
- [x] Basic and functional UI
- [x] Privacy disclaimer
- [x] Feedback form (Discord webhook)
- [x] PWA support (installable on mobile)

### Security (P0)
- [x] Filename sanitization
- [x] Security headers middleware
- [x] Production CORS configuration

### Technical Specifications

#### JSON -> CSV
- Input: Valid JSON (array of objects or object with array)
- Flatten first level of nesting
- First row = column names (JSON keys)
- Default delimiter: comma

#### JSON -> Excel
- Same process as CSV but generating .xlsx
- Single sheet named "Data"

#### CSV -> JSON
- First row = JSON keys
- Each following row = one object
- Output: array of objects
- Auto-detect delimiter (comma, semicolon, tab)

#### Excel -> JSON
- Read first sheet of file
- First row = keys
- Same output as CSV -> JSON

### API Endpoints (Phase 0)

#### POST /convert
Single endpoint for all conversions.

**Request:**
- `file`: file to convert (multipart/form-data)
- `output_format`: desired format (`csv`, `xlsx`, `json`)

**Response:**
- Converted file for download
- Appropriate Content-Type

#### POST /preview
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

### Improvements Completed

#### Frontend / Preview
- [x] Pagination for large files (10 per page by default, max 100)
- [x] Preserve data exactly as in file (leading zeroes preserved)
- [x] Hover hint above preview tables
- [x] Start Over button (renamed from "Upload another file")

#### New Conversions
- [x] CSV -> Excel
- [x] Excel -> CSV

#### Error Handling
- [x] Detailed errors for malformed files (JSON: line/column, CSV: row context, Excel: corruption info)

#### Nested JSON Support (January 2026)
- [x] Nested array expansion via Cartesian product
- [x] Single object support with multiple nested arrays
- [x] Safety limit: MAX_EXPANDED_ROWS=10000

#### Raw Editor for Malformed Files (January 2026)
- [x] Raw text editor when JSON/CSV fails to parse
- [x] Inline error display with line/column info
- [x] Line numbers for easy error location
- [x] Retry functionality without re-uploading
- [x] Seamless flow to normal table preview

#### Smart JSON Handling (January 2026)
- [x] Automatic complexity detection (>100 estimated rows)
- [x] Simplified UX: info screen with "Next" button
- [x] `_record_id` explanation tip
- [x] Tabbed preview (Multi-file vs Single-file)
- [x] Multi-sheet Excel export
- [x] Multi-CSV ZIP export
- [x] New /api/analyze endpoint
- [x] Updated convert/preview with `export_mode` parameter

### "Done" Criteria (Phase 0)
- [x] Upload JSON and download CSV
- [x] Upload JSON and download Excel
- [x] Upload CSV and download JSON
- [x] Upload Excel and download JSON
- [x] Data preview before converting
- [ ] Web deployed and publicly accessible *(moved to Phase 1 backlog)*
- [x] Works on mobile (basic responsive)
- [x] No obvious errors in console

### Out of Scope (Phase 0)
- User registration
- Size limits
- Multiple files at once
- Delimiter selection
- Advanced analytics
- Documented public API

---

## Phase 1 — Consolidate Conversions (Current)

**Goal:** Expand conversion capabilities, improve data transformation options, and add security hardening. Focus on features that solve real user problems like round-tripping data between formats.
**Status:** In Progress (January 2026)

### 1. JSON Structure Transformations (Priority: P0)

#### 1.1 Flatten JSON
Convert nested JSON structures to flat key-value pairs suitable for CSV/tabular formats.

**Input:**
```json
{
  "id": 1,
  "user": {
    "name": "John",
    "address": {
      "city": "NYC"
    }
  },
  "tags": ["a", "b"]
}
```

**Output:**
```json
{
  "id": 1,
  "user.name": "John",
  "user.address.city": "NYC",
  "tags": "[\"a\", \"b\"]"
}
```

**Rules:**
- Nested objects -> dot notation keys (`user.address.city`)
- Arrays -> JSON string representation
- Primitive values remain unchanged

**Use case:** Prepare complex JSON for CSV export with predictable structure.

#### 1.2 Unflatten JSON
Restore nested JSON structures from flattened data (CSV -> original JSON).

**Input:**
```json
{
  "id": 1,
  "user.name": "John",
  "user.address.city": "NYC",
  "tags": "[\"a\", \"b\"]"
}
```

**Output:**
```json
{
  "id": 1,
  "user": {
    "name": "John",
    "address": {
      "city": "NYC"
    }
  },
  "tags": ["a", "b"]
}
```

**Rules:**
- Split keys on `.` to rebuild nested structure
- Detect and parse JSON strings (starts with `[` or `{`)
- Handle edge cases: escaped dots, array indices

**Use case:** Restore original JSON structure after CSV round-trip.

#### 1.3 Implementation Notes

**Backend:**
- New utility: `backend/utils/json_transform.py`
  - `flatten_json(data: dict, separator: str = ".") -> dict`
  - `unflatten_json(data: dict, separator: str = ".") -> dict`
- New converter: `backend/converters/json_transform.py`
- New API endpoint: `POST /api/transform`
  - Parameters: `file`, `operation` (flatten/unflatten)

**Frontend:**
- Add transformation options when JSON is uploaded
- Preview shows before/after comparison
- Download transformed JSON

**Edge cases to handle:**
1. Keys containing dots (e.g., `"user.name"` as literal key)
   - Solution: Optional escape character or alternate separator
2. Array indices in paths (e.g., `tags.0`, `tags.1`)
   - Solution: Support `[0]` notation or keep arrays as JSON strings
3. Empty objects/arrays
4. Mixed types at same path level

### 2. New File Formats (Priority: P1)

#### 2.1 JSON Lines (.jsonl)
- One JSON object per line
- Common for streaming data, logs, ML datasets

**Read:** Parse each line as separate JSON object
**Write:** Output one object per line, no array wrapper

#### 2.2 TSV (Tab-Separated Values)
- Same as CSV but with tab delimiter
- Common for spreadsheet copy-paste

### 3. Delimiter Options (Priority: P1)

Add delimiter selector for CSV operations:
- Comma (default)
- Semicolon (European standard)
- Tab
- Pipe (`|`)

**UI:** Dropdown in conversion options when CSV is involved.

### 4. Security Hardening (Priority: P1)

Carry over from Phase 0 backlog:

#### 4.1 Rate Limiting
- 30 req/min for /api/preview
- 20 req/min for /api/convert
- 60 req/min for /api/health
- Use slowapi library

#### 4.2 Request Timeouts
- File upload: 30 seconds
- File processing: 60 seconds
- Total request: 120 seconds

#### 4.3 ZIP Bomb Protection (XLSX)
- Max compression ratio: 100:1
- Max entries: 1000 files
- Max individual entry: 100MB
- Max total uncompressed: 500MB

### API Changes (Phase 1)

#### New Endpoint: POST /api/transform

Transform JSON structure without format conversion.

**Request:**
```
POST /api/transform
Content-Type: multipart/form-data

Parameters:
- file: File (required) - JSON file to transform
- operation: string (required) - "flatten" or "unflatten"
- separator: string (optional, default: ".") - Key separator
```

**Response:**
```json
{
  "success": true,
  "data": { /* transformed JSON */ },
  "original_keys": 15,
  "transformed_keys": 42
}
```

Or direct file download if `?download=true` query param.

### Development Tasks (Phase 1)

#### Backend
- [ ] Implement `flatten_json()` utility function
- [ ] Implement `unflatten_json()` utility function
- [ ] Create `/api/transform` endpoint
- [ ] Add JSONL read support
- [ ] Add JSONL write support
- [ ] Add TSV support (read/write)
- [ ] Add delimiter selection to CSV converters
- [ ] Implement rate limiting with slowapi
- [ ] Implement request timeouts
- [ ] Implement ZIP bomb protection
- [ ] Tests for all new features

#### Frontend
- [ ] Add "Transform JSON" option for JSON files
- [ ] Before/after preview for transformations
- [ ] Delimiter selector dropdown
- [ ] JSONL format support in UI
- [ ] Rate limit error handling (429 responses)

#### Documentation
- [ ] Update SPEC.md with new endpoints
- [ ] Update CLAUDE.md with new features
- [ ] Add transformation examples to user guide

### "Done" Criteria (Phase 1)
- [ ] Flatten a nested JSON to dot-notation keys
- [ ] Unflatten a CSV-exported JSON back to nested structure
- [ ] Upload/download JSONL files
- [ ] Choose CSV delimiter (comma, semicolon, tab, pipe)
- [ ] Rate limiting is active in production
- [ ] ZIP bomb protection is active for XLSX files
- [ ] All features have tests

### Technical Decisions (Phase 1)

#### Flatten/Unflatten Separator
Default: `.` (dot)

Rationale: Most common convention, matches pandas `json_normalize()` behavior.

Alternative considered: `__` (double underscore) - less ambiguous but less readable.

#### JSON String Detection for Unflatten
Heuristic approach:
1. Check if string starts with `[` or `{`
2. Attempt `json.loads()`
3. If parse succeeds -> use parsed value
4. If parse fails -> keep as string

This handles 99% of cases from our own flatten output.

#### Array Handling in Flatten
Keep arrays as JSON strings rather than indexed keys.

Rationale:
- Simpler round-trip (flatten -> unflatten)
- Matches Phase 0 behavior
- Avoids sparse columns for variable-length arrays

### Dependencies (Phase 1)

No new dependencies required. Existing stack sufficient:
- `json` (stdlib) - JSON parsing
- `pandas` - CSV/Excel handling
- `fastapi` - API framework

For rate limiting (when implemented):
- `slowapi` - Rate limiting middleware

### Out of Scope (Phase 1)
- SQL generation (Phase 2)
- Data cleaning operations (Phase 3)
- Multiple file operations (Phase 4)
- User registration/authentication
- API keys

---

## Phase 2 — SQL Generator

**Goal:** Add SQL generation capabilities to attract technical users (developers, DBAs, data analysts). Convert tabular data (CSV/Excel) into ready-to-use SQL statements for database imports.
**Status:** Not Started (Target: Q1 2026)

### 1. SQL INSERT Generation (Priority: P0)

Generate INSERT statements from tabular data.

**Input (CSV/Excel):**
| id | name | email | age |
|----|------|-------|-----|
| 1 | John | john@example.com | 28 |
| 2 | Jane | jane@example.com | 32 |

**Output:**
```sql
INSERT INTO users (id, name, email, age) VALUES (1, 'John', 'john@example.com', 28);
INSERT INTO users (id, name, email, age) VALUES (2, 'Jane', 'jane@example.com', 32);
```

**Options:**
- Table name (required, user input)
- Include column names (default: true)
- Batch size for multi-row INSERT (default: 1 row per statement)

### 2. CREATE TABLE Generation (Priority: P0)

Generate CREATE TABLE statement with automatic type inference.

**Output:**
```sql
CREATE TABLE users (
    id INTEGER,
    name VARCHAR(255),
    email VARCHAR(255),
    age INTEGER
);
```

**Type Inference Rules:**
| Data Pattern | SQL Type |
|--------------|----------|
| Integer numbers only | INTEGER |
| Decimal numbers | DECIMAL(10,2) |
| Boolean (true/false, 1/0) | BOOLEAN |
| ISO date (YYYY-MM-DD) | DATE |
| ISO datetime (YYYY-MM-DDTHH:MM:SS) | TIMESTAMP |
| Text (default) | VARCHAR(255) |
| Text > 255 chars | TEXT |
| NULL/empty values | nullable column |

### 3. SQL Dialect Support (Priority: P0)

| Dialect | String Quote | Identifier Quote | Type Differences |
|---------|--------------|------------------|------------------|
| MySQL | `'single'` | `` `backtick` `` | INT, VARCHAR, DATETIME |
| PostgreSQL | `'single'` | `"double"` | INTEGER, VARCHAR, TIMESTAMP |
| SQLite | `'single'` | `"double"` | INTEGER, TEXT, REAL |
| SQL Server | `'single'` | `[brackets]` | INT, NVARCHAR, DATETIME2 |

**UI:** Dropdown selector, default MySQL.

### 4. Output Options (Priority: P1)

#### 4.1 Output Mode
- **INSERT only** - Just INSERT statements
- **CREATE + INSERT** - CREATE TABLE followed by INSERT statements
- **CREATE only** - Just the table definition

#### 4.2 Batch INSERT (Multi-row)
```sql
INSERT INTO users (id, name, email, age) VALUES
    (1, 'John', 'john@example.com', 28),
    (2, 'Jane', 'jane@example.com', 32),
    (3, 'Bob', 'bob@example.com', 45);
```

**Batch sizes:** 1 (default), 10, 50, 100, 500, 1000

#### 4.3 NULL Handling
- Empty cells -> `NULL`
- String "NULL" -> `NULL`
- Option to treat empty as empty string `''` instead

### 5. Copy to Clipboard (Priority: P1)
- "Copy SQL" button next to download
- Visual feedback (button text changes to "Copied!")
- Works for preview and full output

### API Changes (Phase 2)

#### New Endpoint: POST /api/generate-sql

**Request:**
```
POST /api/generate-sql
Content-Type: multipart/form-data

Parameters:
- file: File (required) - CSV or Excel file
- table_name: string (required) - Target table name
- dialect: string (optional, default: "mysql") - mysql, postgresql, sqlite, sqlserver
- mode: string (optional, default: "insert") - insert, create, create_insert
- batch_size: int (optional, default: 1) - Rows per INSERT statement
- include_columns: bool (optional, default: true) - Include column names in INSERT
- null_empty: bool (optional, default: true) - Treat empty cells as NULL
```

**Response:**
```json
{
  "success": true,
  "sql": "INSERT INTO users ...",
  "dialect": "mysql",
  "row_count": 150,
  "column_count": 4,
  "columns": [
    {"name": "id", "inferred_type": "INTEGER"},
    {"name": "name", "inferred_type": "VARCHAR(255)"},
    {"name": "email", "inferred_type": "VARCHAR(255)"},
    {"name": "age", "inferred_type": "INTEGER"}
  ]
}
```

#### New Endpoint: POST /api/sql-preview

**Request:**
```
POST /api/sql-preview
Content-Type: multipart/form-data

Parameters:
- file: File (required)
- table_name: string (required)
- dialect: string (optional, default: "mysql")
- mode: string (optional, default: "insert")
- preview_rows: int (optional, default: 5, max: 20)
```

**Response:**
```json
{
  "success": true,
  "preview_sql": "CREATE TABLE users (...); INSERT INTO users ...",
  "total_rows": 1500,
  "columns": [...],
  "warnings": ["Column 'date' has mixed formats, using VARCHAR"]
}
```

### Backend Implementation (Phase 2)

#### New Files
```
backend/
├── generators/
│   ├── __init__.py
│   ├── base.py               # Base SQL generator class
│   ├── sql_generator.py      # Main generator logic
│   └── dialects/
│       ├── __init__.py
│       ├── mysql.py
│       ├── postgresql.py
│       ├── sqlite.py
│       └── sqlserver.py
└── utils/
    └── type_inference.py     # Column type detection
```

#### Core Classes

```python
# backend/generators/base.py
class SQLDialect:
    """Base class for SQL dialects."""
    name: str
    string_quote: str = "'"
    identifier_quote: str = '"'

    def quote_identifier(self, name: str) -> str: ...
    def quote_string(self, value: str) -> str: ...
    def get_type(self, inferred_type: str) -> str: ...

# backend/generators/sql_generator.py
class SQLGenerator:
    """Generate SQL from tabular data."""

    def __init__(self, dialect: SQLDialect): ...
    def infer_types(self, df: pd.DataFrame) -> list[ColumnInfo]: ...
    def generate_create(self, table_name: str, columns: list) -> str: ...
    def generate_inserts(self, table_name: str, df: pd.DataFrame, batch_size: int) -> str: ...
```

#### Type Inference Logic

```python
# backend/utils/type_inference.py
def infer_column_type(series: pd.Series) -> str:
    """
    Infer SQL type from pandas Series.

    Priority:
    1. Check for all nulls -> VARCHAR(255) nullable
    2. Check for integers (no decimals)
    3. Check for floats/decimals
    4. Check for booleans
    5. Check for dates (ISO format)
    6. Check for datetimes
    7. Default to VARCHAR with max length detection
    """
```

### Frontend Implementation (Phase 2)

#### UI Flow
1. User uploads CSV/Excel file
2. Standard table preview shown
3. User clicks "Generate SQL" (new button alongside CSV/Excel options)
4. SQL Options panel appears:
   - Table name input (required)
   - Dialect dropdown
   - Output mode radio buttons
   - Advanced options (collapsible)
5. Click "Generate" shows SQL preview
6. User can: Copy to clipboard, Download as .sql, Adjust and regenerate

#### UI Mockup

```
┌─────────────────────────────────────────────────────────────┐
│  data.csv (2.3 KB)                                          │
│                                                             │
│  Preview:                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ id  │ name  │ email              │ age             │   │
│  │ 1   │ John  │ john@example.com   │ 28              │   │
│  │ 2   │ Jane  │ jane@example.com   │ 32              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Convert to:  [CSV]  [Excel]  [JSON]  [SQL]                │
│                                                             │
│  ┌─ SQL Options ────────────────────────────────────────┐  │
│  │  Table name: [users____________]                      │  │
│  │  Dialect:    [MySQL]                                  │  │
│  │  Output:     INSERT only / CREATE+INSERT / CREATE     │  │
│  │  > Advanced options                                   │  │
│  │  [Generate SQL]                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  [Copy SQL]  [Download .sql]                                │
│  [Start Over]                                               │
└─────────────────────────────────────────────────────────────┘
```

### Development Tasks (Phase 2)

#### Backend
- [ ] Create `backend/generators/` module structure
- [ ] Implement base `SQLDialect` class
- [ ] Implement MySQL dialect
- [ ] Implement PostgreSQL dialect
- [ ] Implement SQLite dialect
- [ ] Implement SQL Server dialect
- [ ] Implement `type_inference.py` utility
- [ ] Implement `SQLGenerator` class
- [ ] Create `/api/generate-sql` endpoint
- [ ] Create `/api/sql-preview` endpoint
- [ ] Add SQL escaping for special characters
- [ ] Add reserved word handling
- [ ] Tests for type inference (edge cases)
- [ ] Tests for each dialect
- [ ] Tests for API endpoints
- [ ] Tests for SQL injection prevention

#### Frontend
- [ ] Add "SQL" button to conversion options
- [ ] Create SQL options panel component
- [ ] Table name input with validation
- [ ] Dialect selector dropdown
- [ ] Output mode radio buttons
- [ ] Advanced options collapsible section
- [ ] SQL preview display with syntax highlighting
- [ ] Copy to clipboard functionality
- [ ] Download as .sql file
- [ ] Loading states during generation
- [ ] Error handling for invalid table names

#### Documentation
- [ ] Update SPEC.md with SQL endpoints
- [ ] Update CLAUDE.md with new commands
- [ ] Add SQL generation examples to user guide

### "Done" Criteria (Phase 2)
- [ ] Upload CSV and generate INSERT statements
- [ ] Upload Excel and generate INSERT statements
- [ ] Generate CREATE TABLE with inferred types
- [ ] Select between MySQL, PostgreSQL, SQLite, SQL Server
- [ ] Generated SQL is valid and executable
- [ ] Copy generated SQL to clipboard
- [ ] Download SQL as .sql file
- [ ] Type inference handles: integers, decimals, dates, booleans, text
- [ ] Reserved SQL words are properly quoted
- [ ] All features have tests (target: 95%+ coverage for generators)

### Technical Decisions (Phase 2)

#### Type Inference Strategy
**Approach:** Sample-based inference with fallback to VARCHAR.

1. Sample up to 1000 rows for type detection
2. If >90% of non-null values match a type -> use that type
3. If mixed types -> fallback to VARCHAR/TEXT
4. Always allow NULL unless explicitly told otherwise

**Rationale:** Conservative approach prevents data loss.

#### Identifier Quoting
**Approach:** Quote all identifiers by default.

Prevents issues with reserved words, spaces, special characters, case sensitivity.

#### Batch INSERT Limits
**Max batch size:** 1000 rows

Rationale: MySQL max_allowed_packet (16MB), PostgreSQL (no hard limit), SQLite SQLITE_MAX_COMPOUND_SELECT (500).

#### SQL Injection Prevention
Even though we generate SQL (not execute), we escape values:
- Single quotes -> doubled (`'` -> `''`)
- Backslashes escaped for MySQL
- Null bytes removed

### Edge Cases (Phase 2)
1. **Empty File** - Error: "File contains no data rows"
2. **Special characters in column names** - Quote identifiers, replace invalid chars
3. **Very long text values** - Infer as TEXT, warn if > 65535 chars
4. **Mixed numeric formats** - "1,234" vs "1.234" -> default to VARCHAR, add warning
5. **Date format ambiguity** - Only recognize ISO format (YYYY-MM-DD), else VARCHAR
6. **Boolean detection** - Recognize: true/false, TRUE/FALSE, 1/0, yes/no, Y/N
7. **Reserved words as column names** - Always quote per dialect

### Security Considerations (Phase 2)
- Table name: alphanumeric + underscore only, max 64 chars
- Batch size: validated range 1-1000
- Dialect: whitelist validation
- All string values properly escaped
- No direct database execution (output only)

### Performance Considerations (Phase 2)
- Preview limited to first 20 rows
- Full generation streams output for files > 10MB
- Process in chunks of 10,000 rows

### SEO Integration (Phase 2)
After completion:
- Create `/csv-to-sql` landing page
- Create `/excel-to-sql` landing page
- Target keywords: "csv to sql insert", "excel to sql generator online"
- Blog post: "How to Generate SQL INSERT Statements from Excel"

### Out of Scope (Phase 2)
- UPDATE/DELETE/ALTER TABLE statements
- Foreign key relationships / index generation
- Stored procedures
- Database connection/execution
- Schema import from existing database

---

## Phase 3 — Data Cleaning
**Goal:** Solve real problems, increase retention.

- [ ] Remove completely empty rows
- [ ] Remove duplicate rows
- [ ] Trim whitespace (leading, trailing, multiple)
- [ ] Standardize dates (detect source format -> target format)
- [ ] Standardize text (UPPER, lower, Capitalize)
- [ ] Before/after preview for each operation
- [ ] Undo last operation

---

## Phase 4 — Advanced Operations
**Goal:** Differentiation, features that Excel doesn't do easily.

- [ ] Merge multiple files into one
- [ ] Compare two files (visual diff: added, deleted, modified rows)
- [ ] Split column (e.g., "full name" -> "first name" + "last name")
- [ ] Merge columns
- [ ] Filter rows by simple condition
- [ ] Bulk rename columns
- [ ] Reorder columns with drag & drop

---

## Phase 5 — Public API
**Goal:** B2B monetization, automation.

- [ ] Documented REST API (OpenAPI/Swagger)
- [ ] Endpoints for all conversions
- [ ] API key authentication
- [ ] Rate limiting by plan
- [ ] Usage dashboard for users
- [ ] Plans: Free (100 req/day), Pro (10k req/day), Enterprise

---

## Phase 6 — Integrations (Future)
**Goal:** Expand ecosystem.

- [ ] Google Sheets integration (import/export)
- [ ] Webhooks (receive data -> process -> return)
- [ ] Zapier / Make integration
- [ ] CLI tool (npm/pip)
- [ ] VS Code extension
- [ ] Background processing for large files

---

## Monetization Model

| Phase | Strategy |
|-------|----------|
| 0-2 | 100% free. Priority: traction and SEO |
| 3+ | Size limit: 5MB free, more requires account |
| 4+ | Advanced features only for registered users |
| 5+ | Paid API: volume-based plans |
| 6+ | Enterprise plans with SLA |

---

## Key Metrics to Track

- Conversions performed per day
- Most used conversion types
- Average file size
- Return rate (users who come back)
- Traffic sources (SEO, direct, referral)
- Most frequent errors

---

## Development Principles

1. **Simplicity first** — Every feature must work without explanation
2. **Speed** — Conversions must be instant for small files
3. **Privacy** — Don't store user data longer than necessary
4. **Fast iteration** — Launch, measure, adjust
