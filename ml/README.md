# ML — Tirana Real Estate Price Estimator

## Overview

This directory contains the **Phase 3** baseline ML model for the Tirana Real Estate Companion.

- **Model:** `RandomForestRegressor` (200 trees, `random_state=42`)
- **Target:** `price_in_euro`
- **Features:** `square_meters`, `bedrooms`, `bathrooms`, `floor`, `has_elevator`, `has_terrace`, `furnishing_status` (label-encoded)
- **Outlier removal:** price outside €5,000–€2,000,000 or sqm outside 10–1,000 m² are excluded from training
- **Fair range:** predicted price ± 15%

The trained model is saved to `models/price_estimator.pkl` as a `joblib` bundle containing:
- `model` — the fitted `RandomForestRegressor`
- `encoder` — the fitted `LabelEncoder` for `furnishing_status`
- `features` — ordered list of feature names
- `model_version` — `"baseline-v1"`
- `fair_range_pct` — `0.15`
- `metrics` — MAE, RMSE, R² from the training run

---

## Setup

All commands run from the **repo root** in WSL:

```bash
cd backend
pip install -r requirements.txt
```

---

## Train the Model

```bash
# From the repo root
python ml/train_model.py
```

This will:
1. Load and preprocess `data/tirana_house_prices.json`
2. Remove outliers (uses the `ml_data` output from `preprocessing.py`)
3. Train a `RandomForestRegressor`
4. Print MAE, RMSE, and R² on a held-out test set (80/20 split)
5. Save the model bundle to `models/price_estimator.pkl`

Expected output (values are approximate):
```
MAE  : €XX,XXX
RMSE : €XX,XXX
R²   : 0.XX
Model saved → models/price_estimator.pkl
```

---

## Generate Visualizations

Run **after** `train_model.py` (the last two plots require the saved model):

```bash
# From the repo root
python ml/visualize.py
```

Figures are saved to `ml/figures/`:

| File | Description |
|------|-------------|
| `01_price_distribution.png` | Histogram of listing prices |
| `02_sqm_vs_price.png` | Scatter: square meters vs. price |
| `03_bedrooms_distribution.png` | Bar chart of bedroom counts |
| `04_bathrooms_distribution.png` | Bar chart of bathroom counts |
| `05_furnishing_status.png` | Furnishing status breakdown |
| `06_correlation_heatmap.png` | Correlation heatmap of numeric features |
| `07_feature_importance.png` | Random Forest feature importances |
| `08_predicted_vs_actual.png` | Predicted vs. actual price scatter |

---

## Model Choices

| Decision | Rationale |
|----------|-----------|
| `RandomForestRegressor` | Robust baseline; handles mixed feature types well; no scaling needed |
| 200 trees | Balances variance reduction with training speed |
| ± 15% fair range | Simple, interpretable bound for a real-estate audience |
| `LabelEncoder` for furnishing | Low cardinality categorical; ordinal encoding is sufficient for RF |

---

## Next Steps

- **Phase 4** — Wire `models/price_estimator.pkl` into `backend/app.py` to serve real predictions from `GET /api/listings/<id>/estimate`.
- Future: Tune hyper-parameters (max depth, min samples split), add more features (location zone, property type).
