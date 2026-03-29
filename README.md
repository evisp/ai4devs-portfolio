# Tirana Real Estate Companion

A property-browsing web app for the Tirana market with ML-based price estimates.
Built with **Python Flask · Bootstrap 5 · scikit-learn** — designed to run locally on WSL/Windows.

---

## Prerequisites

- Python 3.10+
- pip
- WSL (Windows Subsystem for Linux) recommended

---

## Quick Start

### 1. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train the ML model *(one-time, required before starting the app)*

```bash
# From the repo root
python ml/train_model.py
```

Saves the trained model to `models/price_estimator.pkl`.

### 3. Start the Flask server

```bash
# From the backend/ directory
python app.py
```

Open the app in your browser: **http://localhost:5000/listings**

---

## Generate Data Visualizations

Produces 8 charts saved to `ml/figures/` (run after training the model):

```bash
# From the repo root
python ml/visualize.py
```

Output charts:

| File | Description |
|------|-------------|
| `01_price_distribution.png` | Histogram of listing prices |
| `02_sqm_vs_price.png` | Scatter: square meters vs. price |
| `03_bedrooms_distribution.png` | Bar chart: bedroom counts |
| `04_bathrooms_distribution.png` | Bar chart: bathroom counts |
| `05_furnishing_status.png` | Furnishing status breakdown |
| `06_correlation_heatmap.png` | Feature correlation heatmap |
| `07_feature_importance.png` | Random Forest feature importances |
| `08_predicted_vs_actual.png` | Predicted vs. actual price |

---

## Run Tests

```bash
cd backend
pytest
```

---

## API Endpoints

All endpoints under `http://localhost:5000/api/`:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/listings` | Browse listings with filters + pagination |
| GET | `/api/listings/<id>` | Full details for one listing |
| GET | `/api/listings/<id>/estimate` | ML price estimate (Phase 4: real predictions) |
| GET | `/api/listings/<id>/comps` | Comparable properties (Phase 5: real similarities) |

See `docs/api/08-api-contract.yaml` for the full OpenAPI spec.

---

## Project Structure

```
ai4devs-portfolio/
├── backend/
│   ├── app.py              # Flask app and API routes
│   ├── preprocessing.py    # Data loading and cleaning pipeline
│   ├── requirements.txt    # All Python dependencies
│   └── README.md           # Backend-specific setup notes
├── data/
│   └── tirana_house_prices.json
├── docs/
│   ├── concept/            # Project brief, scope, dataset, preprocessing, roadmap
│   ├── ui/                 # Style guide, screen designs, component specs
│   └── api/                # API requirements and OpenAPI contract
├── ml/
│   ├── train_model.py      # Training script (Phase 3)
│   ├── visualize.py        # Data visualization script (Phase 3)
│   ├── figures/            # Generated charts (created by visualize.py)
│   └── README.md           # Model documentation
├── models/
│   └── price_estimator.pkl # Trained model (created by train_model.py)
└── AGENTS.md               # Agent guidance for AI coding tools
```

---

## Development Roadmap

See [`docs/concept/development-roadmap.md`](docs/concept/development-roadmap.md) for the full phase-by-phase plan.

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Repo setup & documentation | ⚠️ Partial |
| 1 | Backend scaffold + data loading + preprocessing | ✅ Complete |
| 2 | Full backend data integration | ✅ Complete |
| 3 | Baseline ML model | ✅ Complete |
| 4 | Backend ML integration | ✅ Complete |
| 5 | Comparable properties (comps) | ⏳ Not started |
| 6 | Frontend: Jinja2 templates + Bootstrap | ⏳ Not started |
| 7 | UI polish | ⏳ Not started |
| 8 | Testing and stabilization | ⏳ Not started |
