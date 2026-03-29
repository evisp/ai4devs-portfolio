"""
train_model.py — Baseline ML model for Tirana Real Estate price prediction.

Phase 3 of the development roadmap.

Usage (from the repo root, in WSL):
    python ml/train_model.py

Output:
    models/price_estimator.pkl   — trained model artifact

Model:
    RandomForestRegressor with default hyper-parameters.
    Features: square_meters, bedrooms, bathrooms, floor,
              has_elevator, has_terrace, furnishing_status (label-encoded).
    Target:   price_in_euro
"""

import os
import sys
import joblib
import logging
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths  (repo-root-relative, so script works from any CWD via python ml/...)
# ---------------------------------------------------------------------------
REPO_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH   = os.path.join(REPO_ROOT, "data", "tirana_house_prices.json")
MODELS_DIR  = os.path.join(REPO_ROOT, "models")
MODEL_PATH  = os.path.join(MODELS_DIR, "price_estimator.pkl")

# Add backend/ to the path so we can import preprocessing.py
sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))
from preprocessing import load_and_preprocess  # noqa: E402

# ---------------------------------------------------------------------------
# Feature configuration
# ---------------------------------------------------------------------------
NUMERIC_FEATURES    = ["square_meters", "bedrooms", "bathrooms", "floor"]
BOOLEAN_FEATURES    = ["has_elevator", "has_terrace"]
CATEGORICAL_FEATURE = "furnishing_status"
TARGET              = "price_in_euro"
MODEL_VERSION       = "baseline-v1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def encode_furnishing(series: list, encoder: LabelEncoder = None):
    """Label-encode furnishing_status. Fit if no encoder is provided."""
    import numpy as np
    arr = np.array([v if v else "unknown" for v in series])
    if encoder is None:
        encoder = LabelEncoder()
        encoded = encoder.fit_transform(arr)
    else:
        # Handle unseen labels gracefully
        encoded = np.array([
            encoder.transform([v])[0] if v in encoder.classes_ else -1
            for v in arr
        ])
    return encoded.tolist(), encoder


def build_feature_matrix(records: list, encoder: LabelEncoder = None):
    """
    Convert a list of preprocessed record dicts into a (X, y) tuple.

    Rows with any missing numeric feature or missing target are dropped.
    Returns: X (np.ndarray), y (np.ndarray), encoder, valid_indices
    """
    all_features = NUMERIC_FEATURES + BOOLEAN_FEATURES + [CATEGORICAL_FEATURE]

    rows   = []
    prices = []

    for r in records:
        # Skip rows with missing target
        if r.get(TARGET) is None:
            continue

        # Skip rows with missing numeric features
        if any(r.get(f) is None for f in NUMERIC_FEATURES):
            continue

        row = [float(r.get(f) or 0) for f in NUMERIC_FEATURES]
        row += [float(bool(r.get(f))) for f in BOOLEAN_FEATURES]
        row.append(r.get(CATEGORICAL_FEATURE) or "unknown")   # placeholder
        rows.append(row)
        prices.append(float(r[TARGET]))

    if not rows:
        raise ValueError("No usable rows after filtering.")

    # Encode furnishing_status (last column)
    furnishing_values = [row[-1] for row in rows]
    encoded_furn, encoder = encode_furnishing(furnishing_values, encoder)
    X = np.array([[*row[:-1], encoded_furn[i]] for i, row in enumerate(rows)],
                 dtype=float)
    y = np.array(prices, dtype=float)

    logger.info("Feature matrix: %d rows × %d features", X.shape[0], X.shape[1])
    logger.info("Features: %s", all_features)
    return X, y, encoder


# ---------------------------------------------------------------------------
# Main training routine
# ---------------------------------------------------------------------------

def train():
    logger.info("=== Phase 3: Training baseline ML model ===")
    logger.info("Data: %s", DATA_PATH)

    # 1. Load and preprocess data (ml_data already has outliers removed)
    _, ml_data = load_and_preprocess(DATA_PATH)
    logger.info("ML dataset size after outlier removal: %d records", len(ml_data))

    # 2. Build feature matrix
    X, y, encoder = build_feature_matrix(ml_data)

    # 3. Train / test split (80 / 20, fixed seed for reproducibility)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    logger.info("Train size: %d  |  Test size: %d", len(X_train), len(X_test))

    # 4. Train model
    logger.info("Training RandomForestRegressor …")
    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = model.predict(X_test)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2   = r2_score(y_test, y_pred)

    logger.info("--- Evaluation Results ---")
    logger.info("  MAE  : €{:,.0f}".format(mae))
    logger.info("  RMSE : €{:,.0f}".format(rmse))
    logger.info("  R²   : {:.4f}".format(r2))

    if r2 < 0.5:
        logger.warning("R² below 0.5 — consider tuning hyper-parameters or adding features.")

    # 6. Fair-range helper (stored alongside model)
    FAIR_RANGE_PCT = 0.15   # ± 15 %

    # 7. Save model bundle
    os.makedirs(MODELS_DIR, exist_ok=True)
    bundle = {
        "model":         model,
        "encoder":       encoder,
        "features":      NUMERIC_FEATURES + BOOLEAN_FEATURES + [CATEGORICAL_FEATURE],
        "model_version": MODEL_VERSION,
        "fair_range_pct": FAIR_RANGE_PCT,
        "metrics": {
            "mae":  round(mae, 2),
            "rmse": round(rmse, 2),
            "r2":   round(r2, 4),
        },
    }
    joblib.dump(bundle, MODEL_PATH)
    logger.info("Model saved → %s", MODEL_PATH)

    # 8. Quick sanity check — sample predictions
    logger.info("--- Sample predictions vs actuals (first 5 test rows) ---")
    for actual, pred in zip(y_test[:5], y_pred[:5]):
        low  = pred * (1 - FAIR_RANGE_PCT)
        high = pred * (1 + FAIR_RANGE_PCT)
        logger.info(
            "  Actual €{:>10,.0f}  |  Predicted €{:>10,.0f}  |  Range €{:,.0f}–€{:,.0f}".format(
                actual, pred, low, high
            )
        )

    return bundle


if __name__ == "__main__":
    train()
