# Statistics Diary

![GitHub Release](https://img.shields.io/github/v/release/kreier/statistics-diary)
![GitHub License](https://img.shields.io/github/license/kreier/statistics-diary)
[![Update Version](https://github.com/kreier/statistics-diary/actions/workflows/update.yml/badge.svg)](https://github.com/kreier/statistics-diary/actions/workflows/update.yml)

<!-- START:version -->
Version: v2026.09.01.65
<!-- END:version -->

`statistics-diary` is a personal data collection and analysis project for bringing together material from multiple sources, extracting content and metadata, and generating statistics and other analytical views.

The project is designed around a staged Python processing pipeline, with an interactive web interface for exploring, categorizing, and editing the resulting data. The vite TypeScript interface is new since 2026-08, prior we used Flask - see [documentation 2026-08](docs/2026-04/README.md)

## Architecture

The project is moving toward a two-part web architecture:

```text
┌─────────────────────────────────────┐
│ Vite + React + TypeScript           │
│                                     │
│ Interactive UI                      │
│ Tables / filters / charts           │
│ Source and category management      │
└──────────────────┬──────────────────┘
                   │ HTTP / JSON
                   │ /api/*
┌──────────────────▼──────────────────┐
│ Python API                          │
│ Flask initially / FastAPI possible  │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ Python processing                   │
│                                     │
│ Source retrieval                    │
│ Parsing                             │
│ Image and metadata processing       │
│ pandas analysis                    │
│ CSV / JSON / file generation        │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ Source and derived data             │
└─────────────────────────────────────┘
```

### Why Python remains the processing layer

The project already contains Python code for reading files and images, extracting metadata, processing source material, using pandas for analysis, and producing CSV/JSON and other outputs.

That code is valuable and does not need to be rewritten merely because the web interface is changing.

The frontend is therefore responsible for **interaction and presentation**, while Python remains responsible for **data and analysis**.

## Data pipeline

The repository uses a staged processing model:

```text
Source configuration
        │
        ▼
Step 1 — source/link discovery
        │
        ▼
Step 2 — content retrieval and parsing
        │
        ▼
Step 3 — analysis and statistics
        │
        ▼
Derived JSON / CSV / other outputs
        │
        ├──────────────► static/generated views
        │
        └──────────────► Python API
                              │
                              ▼
                       Vite web interface
```

The stages are deliberately kept separate. Expensive corpus-wide processing should not be performed simply because a user opens a web page.

See `structure.md` for the detailed repository/data structure.

## Web interface

The current web tooling is being evolved from the existing Flask interface to a Vite frontend.

The target development experience is:

```bash
npm run dev
```

This should eventually start:

- the Vite development server; and
- the Python API server.

The frontend communicates with Python through `/api/...` endpoints. Vite proxies these requests during development.

For example:

```text
Browser
  │
  ├── /              → Vite
  │
  └── /api/sources   → Python API
```

The browser never directly accesses the local filesystem and does not launch Python.

## Interactive goals

The new interface is intended to make the existing analytical workflow easier to use interactively.

Planned capabilities include:

- browsing sources;
- searching and filtering;
- inspecting source metadata;
- changing categories;
- changing colors;
- editing source metadata;
- viewing statistics;
- filtering statistics by source/category/time;
- drilling down from statistics to the underlying records;
- triggering appropriate source refresh/reprocessing operations;
- exporting analytical data.

The exact feature set is tracked in `TODO.md`.

## Existing Python processing

Python remains the preferred language for:

- reading source files;
- downloading/retrieving source material;
- parsing HTML and other formats;
- image processing;
- metadata extraction;
- normalization;
- pandas transformations;
- statistical calculations;
- generating CSV/JSON;
- batch regeneration of derived data.

New API endpoints should call reusable Python processing modules rather than embedding processing logic directly inside route handlers.

## Development

### Python

Use the existing Python environment and dependencies required by the repository.

The existing batch-processing commands remain important. The web application should not replace them.

When modifying Python processing code, test the affected pipeline with representative input before committing.

### Frontend

The planned frontend lives under:

```text
web/
```

A typical development workflow will be:

```bash
npm install
npm run dev
```

The production frontend is built with:

```bash
npm run build
```

The generated Vite files are placed in the normal Vite `dist/` directory.

> These commands become authoritative once the Vite frontend has been added to the repository.

## API

The target API is resource-oriented and JSON-based.

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

The API is an interface to the Python processing/data layer. It is not intended to become a second implementation of the analysis pipeline.

## Batch processing vs. web application

These are deliberately different workflows.

### Batch processing

Used for expensive operations such as:

- retrieving source material;
- processing a large corpus;
- recalculating statistics;
- generating derived files.

Batch processing should remain usable from the command line and in GitHub Actions.

### Web application

Used for:

- exploring existing results;
- filtering and visualizing data;
- editing metadata;
- categorizing sources;
- performing small interactive operations.

Long-running corpus-wide processing should not block an HTTP request.

## Project documentation

| File | Purpose |
|---|---|
| `README.md` | Project overview, architecture, setup, and usage |
| `AGENTS.md` | Durable instructions for coding agents |
| `TODO.md` | Active implementation roadmap |
| `CHANGELOG.md` | History of architectural and user-visible changes |
| `structure.md` | Data and repository structure |

## Migration strategy

The web migration is intentionally incremental:

1. Keep the existing Python processing pipeline.
2. Inventory the existing Flask interface and extract reusable Python functionality.
3. Add a small Python JSON API.
4. Create the Vite/React/TypeScript frontend.
5. Recreate the existing source-management workflow.
6. Add interactive statistics and drill-down.
7. Remove obsolete Flask presentation code only after feature parity.
8. Evaluate SQLite only if the interactive data model requires it.
9. Keep batch processing and GitHub Actions independent from the frontend.

The goal is not to replace Python with Node.js. The goal is to use the best tool for each layer:

```text
TypeScript / React → user interface
Python             → data processing and analysis
pandas             → analytical transformations
JSON / CSV         → exchange and export
SQLite             → optional interactive persistence
```

## Status

The repository is in an incremental migration phase. See `TODO.md` for the current implementation plan and `CHANGELOG.md` for architectural changes.

## License

See the repository's license file for licensing information.
