# AGENTS.md — Tirana Real Estate Companion

## Project goal

Build a small Tirana real-estate web app that:

- Browses and filters property listings.
- Shows a listing details page.
- Shows an ML-based price estimate with a fair low–high range.
- Shows comparable properties ("comps") to support the estimate.

This repo is also a teaching asset for the AI4Devs program, with step-by-step docs in `docs/`.

## Tech stack

- **Backend:** Python + Flask.
- **Frontend:** HTML + CSS + Bootstrap 5 (Jinja2 templates served by Flask).
- **ML:** scikit-learn (baseline regression model).
- **Data:** JSON dataset loaded at startup.

## Key directories

- `docs/` — project documentation.
  - `concept/` — project overview, scope, dataset, data preprocessing, and roadmap.
  - `ui/` — style guide, screens, and UI components.
  - `api/` — API requirements and OpenAPI contract.
- `data/` — raw data.
  - `tirana_house_prices.json` — main dataset of listings.

More code directories (for example `backend/`, `ml/`, `models/`) may be added later.

## How to use the docs

Before generating code, read (or assume) these documents:

- Concept:
  - `docs/concept/01-project-brief.md`
  - `docs/concept/02-product-scope.md`
  - `docs/concept/03-dataset-overview.md`
  - `docs/concept/04-data-preprocessing.md`
- UI:
  - `docs/ui/04-ui-style-guide.md`
  - `docs/ui/05-ui-screens-and-flow.md`
  - `docs/ui/06-ui-components.md`
- API:
  - `docs/api/07-api-requirements.md`
  - `docs/api/08-api-contract.yaml`

These documents describe what to build, how the UI should look, and how the API should behave.

## High-level architecture (intended)

- Backend (Flask):
  - Loads and preprocesses `data/tirana_house_prices.json`.
  - Exposes the API described in `docs/api/07-api-requirements.md` and `docs/api/08-api-contract.yaml`.
  - Provides ML price estimates and comparable properties.
  - Serves frontend templates via Jinja2.
- Frontend (HTML + Bootstrap):
  - Implements the screens described in `docs/ui/05-ui-screens-and-flow.md`.
  - Uses the visual language and components from `docs/ui/04-ui-style-guide.md` and `docs/ui/06-ui-components.md`.
  - Calls the backend API for data, estimates, and comps.
  - Uses Bootstrap 5 for layout, grid, and base components.

If no code exists yet, propose a minimal structure (e.g. `backend/`) aligned with this.

## Agent guidelines

When generating or modifying code:

1. Follow the API contract.
   - Do not change endpoint shapes without updating `docs/api/08-api-contract.yaml` and mentioning it.

2. Follow the UI docs.
   - Use the components and styles defined in `docs/ui/` as a guide.
   - Use Bootstrap 5 classes for layout, buttons, cards, inputs, and modals.

3. Respect the dataset and preprocessing docs.
   - Use `price_in_euro` as the main prediction target.
   - Negative values (e.g. `-1`) are data-entry errors — convert them to their positive equivalent (e.g. `abs(-1)` → `1`).
   - Handle `null` values as described in `docs/concept/04-data-preprocessing.md`.
   - Remove outliers as documented before ML training.

4. Prefer small, incremental changes.
   - Add focused files or functions instead of large rewrites.
   - Keep code readable for students.

5. Keep everything runnable locally.
   - No external paid APIs.
   - Use simple tooling and clear setup instructions.
   - All commands must work in WSL on Windows.

## Typical tasks for agents

Examples of tasks that are in scope for this project:

- Implement backend endpoints that follow the API contract.
- Implement a baseline ML model for price prediction using `price_in_euro`.
- Implement the listings page and details page UI using Jinja2 + Bootstrap.
- Wire the frontend to call the backend API.
- Add tests or small utilities that support the main flow.

Tasks outside scope for now:

- Building complex auth systems.
- Cloud production deployment.
- Large UI redesign that ignores `docs/ui/`.

## Output expectations

When creating or modifying code:

- Keep file names and locations consistent with the docs.
- Add short, focused comments where needed.
- Avoid introducing hidden dependencies or heavy frameworks without justification.
- Use Flask and Bootstrap — do not switch to FastAPI, React, Vue, or other frameworks.
