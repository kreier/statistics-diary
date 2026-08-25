# TODO — Statistics Diary

This backlog tracks the planned transition from the current Flask-oriented web interface to a Vite frontend backed by the existing Python processing pipeline.

## Phase 0 — Baseline and inventory

- [ ] Inventory the existing Flask application and identify every route/view.
- [ ] Identify which Flask routes are presentation-only and which contain real business/data-processing logic.
- [ ] Identify the existing Python modules that should become reusable services.
- [ ] Document the current data flow and source-of-truth files.
- [ ] Identify all generated files and their generating scripts.
- [ ] Record the current commands needed to regenerate the corpus and statistics.
- [ ] Establish a reproducible baseline: run the existing pipeline and verify that the current outputs are generated successfully.

## Phase 1 — Vite frontend foundation

- [ ] Create a `web/` Vite project.
- [ ] Use React and TypeScript unless there is a concrete reason to choose another Vite framework.
- [ ] Add a minimal application shell and navigation.
- [ ] Add linting/formatting appropriate for the frontend.
- [ ] Add `npm run dev`.
- [ ] Add `npm run build`.
- [ ] Add a Vite development proxy for `/api` → Python backend.
- [ ] Add an npm process runner so `npm run dev` starts Vite and Python together.
- [ ] Document frontend setup and development commands.

## Phase 2 — Python API

- [ ] Extract reusable business/data-processing functions from the Flask presentation layer.
- [ ] Add a small JSON API while preserving the existing Flask interface.
- [ ] Decide whether to retain Flask or incrementally move the API to FastAPI.
- [ ] Implement `GET /api/sources`.
- [ ] Implement `GET /api/sources/:id`.
- [ ] Implement source/category/color editing.
- [ ] Implement `PUT /api/sources/:id`.
- [ ] Implement statistics endpoints.
- [ ] Add consistent JSON error responses.
- [ ] Validate API inputs.
- [ ] Add API tests for the most important endpoints.
- [ ] Ensure API handlers do not contain the actual parsing/analysis implementation.

## Phase 3 — Replace the existing Flask UI

- [ ] Recreate the source list in React.
- [ ] Recreate source details.
- [ ] Recreate category selection.
- [ ] Recreate color selection.
- [ ] Recreate source editing/saving.
- [ ] Recreate links/open-source actions.
- [ ] Recreate any existing source-management workflow currently provided by `manage_sources_webview.py` or related Flask code.
- [ ] Compare the old and new interfaces feature-by-feature.
- [ ] Remove obsolete Flask templates only after parity is confirmed.

## Phase 4 — Interactive statistics

- [ ] Build a reusable statistics API response model.
- [ ] Add the main statistics dashboard.
- [ ] Add time-series views.
- [ ] Add category/source filtering.
- [ ] Add day/month/year drill-down.
- [ ] Make charts interactive where useful.
- [ ] Allow selecting a chart element to inspect the underlying source records.
- [ ] Avoid duplicating pandas calculations in the frontend.
- [ ] Add loading, empty, and error states.

## Phase 5 — Data model and persistence

- [ ] Evaluate whether JSON/CSV remain sufficient for interactive editing.
- [ ] If querying/editing becomes cumbersome, design an SQLite schema.
- [ ] Define canonical tables and relationships before introducing SQLite.
- [ ] Provide migration/import tooling if SQLite is adopted.
- [ ] Keep CSV/JSON export functionality.
- [ ] Add data validation before committing changes to canonical data.

## Phase 6 — Batch processing and integration

- [ ] Ensure all existing batch scripts remain independently runnable.
- [ ] Ensure GitHub Actions can still regenerate derived data without starting the web application.
- [ ] Add integration tests covering representative source → parse → analysis → output workflows.
- [ ] Document the difference between batch processing and interactive editing.
- [ ] Decide which generated artifacts should be committed and which should remain generated-only.

## Phase 7 — Production deployment

- [ ] Build the frontend with `npm run build`.
- [ ] Decide whether production static assets are served by Python, a reverse proxy, or a dedicated static server.
- [ ] Configure `/api` routing for production.
- [ ] Verify the application behind the existing deployment infrastructure.
- [ ] Add a production smoke test.
- [ ] Update deployment documentation.

## Cleanup

- [ ] Remove obsolete Flask HTML templates after migration.
- [ ] Remove duplicate presentation logic.
- [ ] Remove obsolete JavaScript/CSS from the previous UI.
- [ ] Update `structure.md`.
- [ ] Update `README.md`.
- [ ] Update `CHANGELOG.md`.
- [ ] Review `AGENTS.md` against the final architecture.
- [ ] Review the repository for dead scripts and obsolete generated files.

## Decisions still to make

- [ ] Flask API vs. FastAPI API.
- [ ] React vs. another Vite-supported frontend framework.
- [ ] JSON/CSV persistence vs. SQLite for interactive state.
- [ ] Production serving model for `dist/` and the Python API.
- [ ] Whether long-running processing should eventually become an asynchronous job system.

## Guiding principle

Do not rewrite working data-processing code simply because the UI is changing.

The target is:

```text
Vite/React/TypeScript
        ↓
     JSON API
        ↓
Python processing + pandas
        ↓
JSON/CSV/files
```

The migration should be incremental, testable, and reversible.
