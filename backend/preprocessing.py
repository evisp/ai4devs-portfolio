"""
preprocessing.py — Data loading and cleaning for Tirana Real Estate Companion.

Implements the 7-step pipeline defined in docs/concept/04-data-preprocessing.md.
"""

import json
import os
import logging
import math

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Fields where -1 is a known data-entry error (Step 3)
COMPOSITION_FIELDS = [
    "main_property_property_composition_balconies",
    "main_property_property_composition_kitchens",
    "main_property_property_composition_living_rooms",
    "main_property_property_composition_bathrooms",
    "main_property_property_composition_bedrooms",
]

# Additional numeric fields to abs-fix if negative
NUMERIC_ABS_FIELDS = [
    "main_property_floor",
    "main_property_property_square",
]

# Boolean fields — null → False (Step 4)
BOOLEAN_FIELDS = [
    "main_property_has_elevator",
    "main_property_has_terrace",
    "main_property_has_carport",
    "main_property_has_garage",
    "main_property_has_garden",
    "main_property_has_parking_space",
]

# Categorical fields — null → "unknown" (Step 4)
CATEGORICAL_FIELDS = [
    "main_property_furnishing_status",
    "main_property_property_status",
    "main_property_property_type",
]

# Field rename mapping (Step 6)
FIELD_MAP = {
    "price_in_euro":                                          "price_in_euro",
    "main_property_property_square":                          "square_meters",
    "main_property_property_composition_bedrooms":            "bedrooms",
    "main_property_property_composition_bathrooms":           "bathrooms",
    "main_property_floor":                                    "floor",
    "main_property_furnishing_status":                        "furnishing_status",
    "main_property_has_elevator":                             "has_elevator",
    "main_property_has_terrace":                              "has_terrace",
    "main_property_has_carport":                              "has_carport",
    "main_property_has_garage":                               "has_garage",
    "main_property_has_garden":                               "has_garden",
    "main_property_has_parking_space":                        "has_parking_space",
    "main_property_location_city_zone_formatted_address":     "address",
    "main_property_location_lat":                             "latitude",
    "main_property_location_lng":                             "longitude",
    "main_property_property_status":                          "property_status",
    "main_property_property_type":                            "property_type",
    "main_property_description_text_content_original_text":   "description",
}

# Outlier thresholds (Step 5)
PRICE_MIN = 5_000
PRICE_MAX = 2_000_000
SQM_MIN = 10
SQM_MAX = 1_000


# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------

def _fix_negative(value):
    """Return abs(value) if value is a negative number, else return as-is."""
    if isinstance(value, (int, float)) and not math.isnan(value) and value < 0:
        return abs(value)
    return value


def _safe_int(value):
    """Convert a float like 2.0 to int 2 for display. Keep None as None."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _safe_float(value):
    """Return float or None."""
    if value is None:
        return None
    try:
        f = float(value)
        return None if math.isnan(f) else f
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def load_and_preprocess(data_path: str):
    """
    Run the full preprocessing pipeline and return (display_data, ml_data).

    display_data: list of dicts with API-friendly field names (all clean records).
    ml_data:      list of dicts excluding outliers (for model training).
    """

    # Step 1 — Load and parse
    logger.info("Step 1: Loading data from %s", data_path)
    with open(data_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    logger.info("  Loaded %d raw records", len(raw))

    neg_fixes = 0
    null_bool_fixes = 0
    null_cat_fixes = 0

    cleaned = []
    for idx, record in enumerate(raw):

        # Step 2 — Create stable listing_id (0-based)
        record["listing_id"] = idx

        # Step 3 — Fix negative values
        for field in COMPOSITION_FIELDS + NUMERIC_ABS_FIELDS:
            original = record.get(field)
            fixed = _fix_negative(original)
            if fixed != original:
                neg_fixes += 1
            record[field] = fixed

        # Step 4 — Handle null values
        # Boolean fields: null → False
        for field in BOOLEAN_FIELDS:
            if record.get(field) is None:
                record[field] = False
                null_bool_fixes += 1

        # Categorical fields: null → "unknown"
        for field in CATEGORICAL_FIELDS:
            if record.get(field) is None:
                record[field] = "unknown"
                null_cat_fixes += 1

        # Numeric and text fields: keep None as-is (handled in rename step)

        # Step 6 — Rename fields for API
        renamed = {"listing_id": record["listing_id"]}
        for src, dst in FIELD_MAP.items():
            renamed[dst] = record.get(src)

        # Convert integer-like floats for display (bedrooms, bathrooms, floor)
        renamed["bedrooms"]  = _safe_int(renamed.get("bedrooms"))
        renamed["bathrooms"] = _safe_int(renamed.get("bathrooms"))
        renamed["floor"]     = _safe_int(renamed.get("floor"))

        # Ensure numeric types
        renamed["price_in_euro"]  = _safe_float(renamed.get("price_in_euro"))
        renamed["square_meters"]  = _safe_float(renamed.get("square_meters"))
        renamed["latitude"]       = _safe_float(renamed.get("latitude"))
        renamed["longitude"]      = _safe_float(renamed.get("longitude"))

        cleaned.append(renamed)

    logger.info("Step 3: Fixed %d negative values", neg_fixes)
    logger.info("Step 4: Set %d null booleans to False", null_bool_fixes)
    logger.info("Step 4: Set %d null categoricals to 'unknown'", null_cat_fixes)

    # Log data quality summary
    total = len(cleaned)
    null_counts = {}
    for key in cleaned[0]:
        count = sum(1 for r in cleaned if r.get(key) is None)
        if count > 0:
            null_counts[key] = count
    logger.info("Data quality: %d total records", total)
    for field, count in sorted(null_counts.items()):
        logger.info("  %s: %d nulls (%.1f%%)", field, count, 100 * count / total)

    display_data = cleaned

    # Step 5 — Remove outliers (ML dataset only)
    ml_data = [
        r for r in cleaned
        if r.get("price_in_euro") is not None
        and PRICE_MIN <= r["price_in_euro"] <= PRICE_MAX
        and r.get("square_meters") is not None
        and SQM_MIN <= r["square_meters"] <= SQM_MAX
    ]
    removed = total - len(ml_data)
    logger.info("Step 5: Removed %d outliers, ML dataset has %d records", removed, len(ml_data))

    return display_data, ml_data
