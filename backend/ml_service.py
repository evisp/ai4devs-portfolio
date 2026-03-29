"""
ml_service.py — ML price estimation service for Tirana Real Estate Companion.

Phase 4 of the development roadmap.

Responsibilities:
  - Load the saved model bundle from models/price_estimator.pkl at startup.
  - Expose a single public function: estimate_price(listing) → dict.
  - Use the same feature set as train_model.py (square_meters, bedrooms,
    bathrooms, floor, has_elevator, has_terrace, furnishing_status).
  - Calculate fair range as prediction ± fair_range_pct (stored in bundle).
"""

import os
import logging
import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(REPO_ROOT, "models", "price_estimator.pkl")

# ---------------------------------------------------------------------------
# Feature list — must match train_model.py exactly
# ---------------------------------------------------------------------------

NUMERIC_FEATURES    = ["square_meters", "bedrooms", "bathrooms", "floor"]
BOOLEAN_FEATURES    = ["has_elevator", "has_terrace"]
CATEGORICAL_FEATURE = "furnishing_status"

ALL_FEATURES = NUMERIC_FEATURES + BOOLEAN_FEATURES + [CATEGORICAL_FEATURE]

# ---------------------------------------------------------------------------
# Load model bundle at import time
# ---------------------------------------------------------------------------

_bundle = None  # populated by load_model()


def load_model() -> bool:
    """
    Load the model bundle from disk.  Call this once at Flask startup.

    Returns True on success, False if the model file is missing or corrupt.
    """
    global _bundle
    try:
        import joblib
        _bundle = joblib.load(MODEL_PATH)
        version = _bundle.get("model_version", "unknown")
        metrics = _bundle.get("metrics", {})
        mae_formatted = f"€{metrics.get('mae', 0):,.0f}" if metrics.get("mae") else "n/a"
        logger.info(
            "ML model loaded — version=%s  R²=%.4f  MAE=%s",
            version,
            metrics.get("r2", float("nan")),
            mae_formatted,
        )
        return True
    except FileNotFoundError:
        logger.warning("Model file not found at %s — estimate endpoint will return nulls.", MODEL_PATH)
        return False
    except Exception as exc:
        logger.error("Failed to load model: %s", exc)
        return False


def _model_ready() -> bool:
    """Return True if the model bundle was successfully loaded."""
    return _bundle is not None and "model" in _bundle


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def _extract_features(listing: dict):
    """
    Build the feature vector for a single listing dict.

    Returns (feature_row, missing_fields) where:
      - feature_row is a 1-D numpy array of floats, or None if required
        features are missing.
      - missing_fields is a list of field names that were None/missing.
    """
    missing = []

    # Numeric features — required (None → prediction is not possible)
    row = []
    for f in NUMERIC_FEATURES:
        val = listing.get(f)
        if val is None:
            missing.append(f)
            row.append(0.0)   # placeholder; will be flagged by missing list
        else:
            row.append(float(val))

    # Boolean features — default to False if missing (not a blocker)
    for f in BOOLEAN_FEATURES:
        row.append(float(bool(listing.get(f, False))))

    # Categorical feature — default to "unknown" if missing
    cat_val = listing.get(CATEGORICAL_FEATURE) or "unknown"
    row.append(cat_val)   # will be encoded below

    return row, missing


def _encode_row(row: list):
    """
    Encode the raw feature row (list with one string at the end) into a
    numpy float array using the encoder stored in the model bundle.

    Returns a (1, n_features) numpy array.
    """
    encoder = _bundle["encoder"]
    cat_val = row[-1]
    numeric_part = np.array(row[:-1], dtype=float)

    if cat_val in encoder.classes_:
        encoded_cat = float(encoder.transform([cat_val])[0])
    else:
        # Unseen label — use -1 (same as encode_furnishing in train_model.py)
        encoded_cat = -1.0

    return np.concatenate([numeric_part, [encoded_cat]]).reshape(1, -1)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def estimate_price(listing: dict) -> dict:
    """
    Generate an ML price estimate for a listing.

    Parameters
    ----------
    listing : dict
        A preprocessed listing record (API-friendly field names).

    Returns
    -------
    dict with keys:
        estimated_price  — float or None
        fair_range_low   — float or None
        fair_range_high  — float or None
        model_version    — str or None
        notes            — str or None
    """
    # Model not available
    if not _model_ready():
        return {
            "estimated_price":  None,
            "fair_range_low":   None,
            "fair_range_high":  None,
            "model_version":    None,
            "notes": (
                "ML model is not loaded. "
                "Run `python ml/train_model.py` from the repo root to train it."
            ),
        }

    # Extract features
    raw_row, missing_fields = _extract_features(listing)

    if missing_fields:
        # One or more required numeric features are missing — cannot predict
        return {
            "estimated_price":  None,
            "fair_range_low":   None,
            "fair_range_high":  None,
            "model_version":    _bundle.get("model_version"),
            "notes": (
                f"Cannot generate estimate — missing required features: "
                f"{', '.join(missing_fields)}."
            ),
        }

    # Encode and predict
    X = _encode_row(raw_row)
    predicted = float(_bundle["model"].predict(X)[0])

    # Fair range (± percentage stored in bundle, default 15 %)
    pct = _bundle.get("fair_range_pct", 0.15)
    low  = round(predicted * (1 - pct), 2)
    high = round(predicted * (1 + pct), 2)
    predicted = round(predicted, 2)

    return {
        "estimated_price":  predicted,
        "fair_range_low":   low,
        "fair_range_high":  high,
        "model_version":    _bundle.get("model_version"),
        "notes":            None,
    }
