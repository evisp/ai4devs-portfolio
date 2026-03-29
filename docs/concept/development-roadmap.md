# Development Roadmap — Tirana Real Estate Companion

## Purpose

This document outlines the incremental steps to build the MVP.

Each phase is small, has clear success criteria, and builds on the previous one.

Use this as a checklist for manual development or when prompting AI coding agents.

**Tech stack:** Python Flask · HTML · CSS · Bootstrap 5 · Jinja2 · scikit-learn  
**Environment:** Windows with WSL. All commands must work in WSL.

---

## Phase 0 — Repo setup

**Status:** ⚠️ Partial

**Goal:** Make the repo agent-ready with complete documentation.

**Deliverables:**
- [x] `AGENTS.md` at root.
- [x] `docs/concept/01-project-brief.md`
- [x] `docs/concept/02-product-scope.md`
- [x] `docs/concept/03-dataset-overview.md`
- [x] `docs/concept/04-data-preprocessing.md`
- [x] `docs/ui/04-ui-style-guide.md`
- [x] `docs/ui/05-ui-screens-and-flow.md`
- [x] `docs/ui/06-ui-components.md`
- [x] `docs/api/07-api-requirements.md`
- [x] `docs/api/08-api-contract.yaml`
- [x] `data/tirana_house_prices.json`
- [ ] Simple `README.md` at root.

**Success criteria:**
- Root repo has clear guidance for humans and agents.
- All doc filenames match references in `AGENTS.md`.

---

## Phase 1 — Backend scaffold + data loading + preprocessing

**Status:** ✅ Complete

**Goal:** Create the Flask app, load and preprocess the dataset, and expose all 4 API endpoints with correct JSON shapes (stubs for ML endpoints).

**Estimated effort:** 2–3 hours.

**Docs to read:**
- `AGENTS.md`
- `docs/concept/03-dataset-overview.md`
- `docs/concept/04-data-preprocessing.md`
- `docs/api/07-api-requirements.md`
- `docs/api/08-api-contract.yaml`

**Instructions for agent:**
- Create `backend/` folder with this structure:
  ```
  backend/
  ├── app.py              # Flask app entry point
  ├── preprocessing.py    # Data loading and cleaning
  ├── requirements.txt    # Python dependencies
  └── README.md           # Local setup instructions
  ```
- In `preprocessing.py`:
  - Load `data/tirana_house_prices.json`.
  - Generate stable `listing_id` from row index.
  - Fix negative values: apply `abs()` to all composition fields (see `04-data-preprocessing.md`).
  - Handle nulls per field type (see `04-data-preprocessing.md`).
  - Rename long field names to short API names.
  - Log data quality summary (total rows, nulls per field).
- In `app.py`:
  - Create a Flask app with CORS enabled.
  - Load preprocessed data at startup.
  - Implement 4 endpoints (all under `/api/`):
    - `GET /api/listings` — return real listing summaries with pagination (`limit`, `offset`).
    - `GET /api/listings/<listing_id>` — return real listing details (stub is fine).
    - `GET /api/listings/<listing_id>/estimate` — return stub JSON.
    - `GET /api/listings/<listing_id>/comps` — return stub JSON.
  - Implement `ErrorResponse` JSON format for 400, 404, 500 errors.
- In `requirements.txt`: `flask`, `flask-cors`, `pandas`, `scikit-learn`, `joblib`.

**Success criteria:**
- `cd backend && pip install -r requirements.txt && python app.py` starts the server on port 5000.
- All 4 endpoints return correctly shaped JSON matching `08-api-contract.yaml`.
- `GET /api/listings` returns real listing summaries from the dataset.
- Error responses use the `ErrorResponse` schema.
- Preprocessing correctly converts `-1` values to positive.
- CORS headers present in responses.

---

## Phase 2 — Full backend data integration

**Status:** ✅ Complete

**Goal:** Replace stubs with real data for listings and details endpoints. Implement all filters.

**Estimated effort:** 1–2 hours.

**Instructions for agent:**
- Implement real filtering for `GET /api/listings`:
  - `min_price`, `max_price`
  - `min_bedrooms`, `max_bedrooms`
  - `min_bathrooms`, `max_bathrooms`
  - `min_sqm`, `max_sqm`
  - `furnishing_status`
  - `has_elevator`, `has_terrace`
- Implement pagination with `limit` (default 20) and `offset` (default 0).
- Return `total` count in the response alongside filtered `items`.
- Implement real details for `GET /api/listings/<listing_id>`:
  - Return all `ListingDetails` schema fields: core info, all amenities (`has_carport`, `has_garage`, `has_garden`, `has_parking_space`), `property_status`, `property_type`, `latitude`, `longitude`, `description`.
- Keep `/estimate` and `/comps` as stubs.

**Success criteria:**
- Each filter parameter correctly narrows results.
- Pagination returns correct subsets and accurate `total` count.
- `GET /api/listings/<listing_id>` returns all `ListingDetails` fields.
- Backend handles missing data gracefully (no crashes on null fields).

---

## Phase 3 — Baseline ML model

**Status:** ✅ Complete

**Goal:** Train and save a simple, working price prediction model.

**Estimated effort:** 2–3 hours.

**Instructions for agent:**
- Create `ml/` folder:
  ```
  ml/
  ├── train_model.py      # Training script
  └── README.md           # Model documentation
  ```
- In `train_model.py`:
  - Reuse preprocessing from `backend/preprocessing.py`.
  - Fix negative values with `abs()` (same rules as Phase 1).
  - Remove outliers: drop `price_in_euro` < 5,000 or > 2,000,000; drop `square_meters` < 10 or > 1,000.
  - Select features: `square_meters`, `bedrooms`, `bathrooms`, `floor`, `has_elevator`, `has_terrace`, `furnishing_status` (encoded).
  - Train a `RandomForestRegressor` (or `GradientBoostingRegressor`).
  - Evaluate: print MAE, RMSE, R² on a test split.
  - Save model to `models/price_estimator.pkl` using joblib.
- Define fair-range logic: prediction ± 15% (or use model confidence intervals).
- Document model choices in `ml/README.md`.

**Success criteria:**
- Running `python ml/train_model.py` trains and saves the model reproducibly.
- Model achieves reasonable R² (> 0.5 on test set).
- Sample predictions are plausible (no negative prices, no extreme outliers).
- Feature preprocessing explicitly handles `-1` and null values.

---

## Phase 4 — Backend ML integration

**Status:** ✅ Complete

**Goal:** Make `GET /api/listings/<listing_id>/estimate` return real ML predictions.

**Estimated effort:** 1 hour.

**Instructions for agent:**
- Load the saved model from `models/price_estimator.pkl` at Flask startup.
- Implement `GET /api/listings/<listing_id>/estimate`:
  - Extract features for the requested listing using the same preprocessing as training.
  - Run prediction.
  - Calculate fair range (prediction ± 15%).
  - Return `estimated_price`, `fair_range_low`, `fair_range_high`, `model_version` (e.g. `"baseline-v1"`), and `notes` (optional).
- Handle edge cases: listing not found (404), listing missing required features for prediction (return null estimate with a note).

**Success criteria:**
- `GET /api/listings/<listing_id>/estimate` returns real ML predictions.
- Response matches `EstimateResponse` schema in `08-api-contract.yaml`.
- Predictions are consistent for the same listing.

---

## Phase 5 — Comparable properties (comps)

**Status:** ✅ Complete

**Goal:** Implement comps logic and wire it to the API.

**Estimated effort:** 2 hours.

**Instructions for agent:**
- Define similarity scoring using:
  - Geographic distance (haversine on lat/lng).
  - Size similarity (absolute difference in sqm).
  - Room similarity (bedrooms, bathrooms).
- Implement `GET /api/listings/<listing_id>/comps`:
  - Score all other listings against the target listing.
  - Return the top `limit` (default 5) most similar listings.
  - Generate a human-readable `similarity_reason` for each comp (e.g. "Similar size and 2 bedrooms, 0.5 km away").
  - Include `distance_meters` if lat/lng is available for both listings.
- Handle edge case: if target listing has no lat/lng, use feature-only similarity.

**Success criteria:**
- `GET /api/listings/<listing_id>/comps` returns 5 similar listings with reasons.
- Comp selection is reasonable (not random, geographically and feature-close).
- Response matches the `ComparableListing` schema.

---

## Phase 6 — Frontend: Jinja2 templates + Bootstrap

**Status:** ⏳ Not started

**Goal:** Build the two main pages as server-rendered Jinja2 templates styled with Bootstrap 5.

**Estimated effort:** 3–4 hours.

**Docs to read:**
- `docs/ui/04-ui-style-guide.md` (colors, typography)
- `docs/ui/05-ui-screens-and-flow.md` (page layouts and flow)
- `docs/ui/06-ui-components.md` (Bootstrap component mapping)

**Instructions for agent:**
- Create template structure inside `backend/`:
  ```
  backend/
  ├── templates/
  │   ├── base.html               # PageLayout: Bootstrap CDN + navbar + content block
  │   ├── listings.html           # Screen 1: filters + listing cards + pagination
  │   ├── listing_detail.html     # Screen 2: details + estimate + comps
  │   └── partials/
  │       ├── _filter_group.html
  │       ├── _listing_card.html
  │       ├── _estimate_block.html
  │       └── _comparable_card.html
  └── static/
      └── style.css               # Custom overrides for project colors
  ```
- In `app.py`, add Flask routes that render these templates:
  - `GET /` → redirect to `/listings`
  - `GET /listings` → render `listings.html` with filter parameters and paginated data
  - `GET /listings/<listing_id>` → render `listing_detail.html` with details, estimate, and comps
- Implement all components from `06-ui-components.md`:
  - `FilterGroup` with price, bedrooms, bathrooms, sqm, furnishing, elevator, terrace
  - `ListingCard` with price, address, attribute badges, "View details" link
  - `EstimateBlock` with predicted price, fair range, optional note
  - `ComparableCard` with price, address, attributes, similarity reason
- Use `style.css` to set custom colors from the style guide (`#2563EB`, `#F9FAFB`, etc.).

**Success criteria:**
- Full user flow works: open app → browse listings → apply filters → open details → see estimate → see comps → go back.
- Templates use Bootstrap 5 grid and components.
- All component partials from `06-ui-components.md` are implemented.
- Pages look clean and readable on a 1280px+ screen.

---

## Phase 7 — UI polish

**Status:** ⏳ Not started

**Goal:** Apply style guide details, improve visual quality, and handle edge cases in the UI.

**Estimated effort:** 1–2 hours.

**Instructions for agent:**
- Verify all colors match `04-ui-style-guide.md`:
  - Primary blue `#2563EB`, hover `#1D4ED8`.
  - Background `#F9FAFB`, cards `#FFFFFF`, borders `#E5E7EB`.
  - Text primary `#111827`, text secondary `#6B7280`.
  - Accent green `#10B981`, warning orange `#F97316`.
- Apply typography: system font stack, correct font sizes per role.
- Handle missing data in the UI:
  - Show "N/A" for null numeric fields.
  - Show "Address not available" for missing addresses.
  - Show "No description available" for missing descriptions.
  - Show "Estimate unavailable" when ML can't predict.
- Add pagination controls (Bootstrap pagination component) on the listings page.
- Verify responsive behavior: filters stack on narrow screens.

**Success criteria:**
- UI matches the style guide colors and typography.
- No broken layouts or missing text for edge cases.
- Pagination controls work correctly.
- Page is usable at 1280px and degrades gracefully at smaller widths.

---

## Phase 8 — Testing and stabilization

**Status:** ⏳ Not started

**Goal:** Add basic tests, fix issues, and write clear setup instructions.

**Estimated effort:** 1–2 hours.

**Instructions for agent:**
- Backend tests (using `pytest`):
  - Test each API endpoint with valid parameters.
  - Test each API endpoint with invalid parameters (expect 400).
  - Test unknown `listing_id` (expect 404).
  - Test preprocessing: verify `-1` values become positive.
  - Test preprocessing: verify null handling.
- Frontend manual tests:
  - Verify the full user flow in a browser.
  - Verify pagination works end-to-end.
  - Verify filters clear correctly.
- Create or update root `README.md` with:
  - Prerequisites (Python 3.10+, pip).
  - WSL-compatible setup commands:
    ```bash
    cd backend
    pip install -r requirements.txt
    python ../ml/train_model.py      # train model (one-time)
    python app.py                    # start the app
    ```
  - How to open the app: `http://localhost:5000/listings`.
  - How to run tests: `cd backend && pytest`.

**Success criteria:**
- Project runs locally end-to-end from a fresh clone.
- All tests pass.
- `README.md` has clear, working WSL commands.
- All commands verified in WSL on Windows.

---

## Completion checklist

When all phases are ✅:

- [ ] Full user flow works locally.
- [ ] ML estimate is integrated and reasonable.
- [ ] Comps show similarity reasons.
- [ ] UI matches design docs.
- [ ] Backend API matches contract.
- [ ] Repo has clear setup instructions.
- [ ] Code is readable for students.
- [ ] Error responses follow contract schema.
- [ ] All commands verified in WSL.

## Notes for AI agents

- Work one phase at a time.
- Reference the relevant docs for each phase.
- Propose a plan before coding.
- Keep changes small and focused.
- Use Flask and Bootstrap — do not switch frameworks.

Total estimated time: 14–18 hours across phases.
