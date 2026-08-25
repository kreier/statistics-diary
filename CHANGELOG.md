# Changelog

All notable changes to `statistics-diary` are documented here.

The project is currently transitioning from a Flask-rendered interactive interface toward a Vite/React/TypeScript frontend backed by a Python API. During the transition, the existing Python data-processing pipeline remains the authoritative processing layer.

## [Unreleased]

### Architecture

- Planned migration of the interactive web interface from Flask-rendered pages to a Vite frontend.
- Python remains responsible for file ingestion, parsing, image/metadata processing, pandas analysis, and exports.
- The frontend/backend boundary is being defined around a JSON HTTP API.
- The existing staged processing pipeline remains in place:
  source discovery → content retrieval/parsing → analysis → derived output.
- The migration is explicitly incremental; existing batch-processing functionality should continue to work throughout.

### Frontend

- Planned Vite + React + TypeScript frontend.
- Planned Vite development proxy for `/api`.
- Planned single development command that starts both the Vite server and Python API.

### Backend

- Planned extraction of reusable processing services from the existing Flask presentation layer.
- Planned JSON API for sources, source metadata, categories, colors, and statistics.
- Flask may initially remain the API framework; FastAPI is an architectural option for a later incremental migration.

### Data

- JSON and CSV remain supported intermediate/export formats.
- SQLite is considered only if interactive querying and editing demonstrate a need for a database.

### Documentation

- Added project-agent guidance in `AGENTS.md`.
- Added the implementation roadmap in `TODO.md`.
- README documentation is being updated to describe the target frontend/backend architecture.

## Migration notes

The following principles apply during the transition:

1. Do not duplicate pandas/data-processing logic in TypeScript.
2. Do not make browser code responsible for launching Python or accessing the filesystem.
3. Keep expensive corpus-wide processing outside synchronous HTTP requests.
4. Preserve the existing command-line and GitHub Actions workflows.
5. Remove old Flask presentation code only after equivalent functionality is available in the new frontend.
