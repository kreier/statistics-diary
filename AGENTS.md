# AGENTS.md — Statistics Diary

## Project purpose

`statistics-diary` is a personal data-ingestion, analysis, and visualization project. It collects material from multiple sources, extracts and normalizes content and metadata, calculates statistics, and produces machine-readable and human-readable outputs.

The project is intentionally **Python-first for data processing**. A modern Vite frontend is being introduced for interactive exploration and editing, while Python remains responsible for file processing, parsing, analysis, and persistence.

The repository should evolve incrementally. Do not rewrite working Python processing code merely to move functionality to JavaScript.

## Architecture

The target architecture is:

```text
                    ┌─────────────────────────────┐
                    │ Vite + React + TypeScript   │
                    │                             │
                    │ Interactive tables          │
                    │ Filters and search           │
                    │ Charts and statistics        │
                    │ Source/category editing      │
                    └──────────────┬──────────────┘
                                   │ HTTP/JSON
                                   │ /api/*
                    ┌──────────────▼──────────────┐
                    │ Python API                  │
                    │ Flask initially; FastAPI    │
                    │ may be adopted incrementally│
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Python processing layer     │
                    │                             │
                    │ Parsers / metadata          │
                    │ pandas / analysis           │
                    │ File and image processing   │
                    │ Export generation            │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Persistent/intermediate data│
                    │ JSON / CSV / source files   │
                    │ SQLite when justified       │
                    └─────────────────────────────┘
```

### Responsibilities

**Vite/React/TypeScript**
- Presentation and interaction.
- Tables, filtering, sorting, forms, charts, and navigation.
- API calls through `/api/...`.
- No direct filesystem access.
- No data-processing logic that belongs in Python/pandas.

**Python**
- Reading and writing files.
- Image and metadata processing.
- Parsing external sources.
- pandas transformations and analytical calculations.
- Validation and normalization.
- Import/export.
- API endpoints used by the frontend.

**Batch pipeline**
- Expensive corpus-wide operations remain runnable independently of the web UI.
- GitHub Actions and command-line scripts should continue to be able to regenerate derived data without requiring the frontend.

## Source of truth

Keep the distinction between:
- original/source material;
- canonical configuration and metadata;
- intermediate processing results;
- derived analytical output;
- presentation assets.

Do not silently treat a generated CSV/JSON artifact as authoritative when it is actually derived from another source.

When changing the data model, identify the canonical source first and update the pipeline rather than patching generated output.

## Existing processing pipeline

The repository currently uses a staged data workflow. Preserve the conceptual separation:

```text
sources
  ↓
Step 1 — link/source discovery
  ↓
Step 2 — content retrieval and parsing
  ↓
Step 3 — analysis/statistics
  ↓
derived output
  ↓
web/static presentation
```

Existing scripts and directories may use different names; do not rename them solely for aesthetic reasons.

## Web application rules

### Development

The preferred developer experience is eventually:

```bash
npm run dev
```

which starts both:
1. the Vite development server; and
2. the Python API server.

Use an npm process runner such as `concurrently` rather than making browser-side JavaScript launch Python.

Vite should proxy `/api` to the Python server so frontend code can use:

```ts
fetch("/api/sources")
```

instead of hard-coding a Python port.

### Production

`npm run build` produces the static frontend.

The production deployment may:
- serve the Vite `dist/` directory directly and proxy `/api` to Python; or
- serve the Vite build through the Python application.

Do not make the production architecture depend on Vite's development server.

## API design

Use resource-oriented, predictable endpoints.

Examples:

```text
GET    /api/sources
GET    /api/sources/:id
PUT    /api/sources/:id

GET    /api/statistics
GET    /api/statistics/days
GET    /api/statistics/categories

POST   /api/sources/:id/refresh
POST   /api/sources/:id/reparse
```

API responses should be JSON and should have stable field names.

Do not expose arbitrary filesystem paths or shell commands through the API.

Long-running operations must not block an HTTP request indefinitely. Initially they may remain command-line/batch operations; if asynchronous jobs are later introduced, expose job status explicitly.

## Data and database policy

JSON and CSV remain valid intermediate and export formats.

Do not introduce a database merely because a web frontend exists.

SQLite becomes appropriate when interactive editing, querying, relationships, or concurrent access make filesystem-based JSON/CSV cumbersome. If SQLite is introduced:
- define a clear schema;
- identify which tables are canonical;
- keep CSV/JSON export available where useful;
- do not duplicate the same authoritative data in multiple stores without a synchronization strategy.

## Frontend conventions

Use TypeScript rather than JavaScript for new frontend code.

Prefer small components with clear responsibilities.

Keep API access in a dedicated client/service layer rather than scattering raw `fetch()` calls throughout UI components.

Do not put pandas-like analytical logic into React components.

Keep presentation state separate from persistent domain data.

## Python conventions

Reuse existing Python modules before creating parallel implementations.

Prefer functions/classes with explicit inputs and outputs over scripts that rely on implicit global state.

Do not make the API layer contain the actual parsing/analysis implementation. API handlers should call reusable Python services/modules.

When practical, make processing functions usable both:
- from the command line/batch pipeline; and
- from the API.

## Generated files

Before editing a generated artifact, determine how it is generated.

Generated statistics, HTML, charts, JSON, or CSV files should normally be regenerated by the appropriate pipeline rather than manually edited.

If a generated artifact is intentionally committed, document its generation command.

## Testing

At minimum, changes should be checked at the appropriate layer:

### Python
- Run the affected script/module.
- Verify representative input and output.
- Test edge cases involving missing metadata, malformed files, empty datasets, and duplicate records.

### API
- Start the backend.
- Exercise affected endpoints.
- Verify JSON structure and error responses.

### Frontend
- Run the development server.
- Check affected screens manually.
- Run the production build with `npm run build`.

### Integration
For changes crossing frontend/API boundaries:
1. start both servers;
2. exercise the API from the browser;
3. verify that changes persist correctly;
4. verify that batch processing still works.

## Git and change discipline

Keep changes focused.

Do not combine a frontend migration with unrelated cleanup unless required.

When replacing the Flask UI:
- retain working batch-processing behavior;
- migrate one screen/workflow at a time;
- remove old Flask presentation code only after the replacement works;
- record architectural changes in `CHANGELOG.md`.

## Documentation

- `README.md` explains the project to humans and gives setup/usage information.
- `AGENTS.md` contains durable instructions for coding agents.
- `TODO.md` is the active implementation backlog.
- `CHANGELOG.md` records completed, user-visible, and architectural changes.
- `structure.md` describes the data pipeline and should remain consistent with the actual implementation.

Do not turn `AGENTS.md` into a chronological development diary. Put temporary session details in issues, commits, or `TODO.md` as appropriate.

## Definition of done for the Vite migration

A migration step is complete only when:
- the new frontend works against the Python API;
- the corresponding existing workflow still works;
- the Python processing pipeline remains usable independently;
- no unnecessary duplicate processing logic has been introduced in TypeScript;
- development startup is documented;
- production build succeeds;
- the README and changelog reflect the new architecture where relevant.

## Non-goals

Do not:
- rewrite Python processing in Node without a concrete performance or maintenance reason;
- make Vite responsible for filesystem or data processing;
- make browser code execute arbitrary local Python;
- introduce a large framework or database without a demonstrated need;
- remove the existing staged pipeline merely to simplify the web application.
