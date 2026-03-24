# Data Preprocessing — Tirana Real Estate Companion

## Purpose of this document

This document defines the complete preprocessing pipeline for the dataset.

It ensures that all data cleaning rules are centralized, consistent, and easy to follow for students, developers, and AI coding agents.

## Input

Source file: `data/tirana_house_prices.json`

This is a JSON array of listing objects. See `docs/concept/03-dataset-overview.md` for the full field reference.

## Preprocessing pipeline

Apply these steps in order when loading the dataset.

### Step 1 — Load and parse

- Load the JSON file into a list of dictionaries or a pandas DataFrame.
- Verify the file is a valid JSON array.

### Step 2 — Create stable listing identifier

- The source data does not include a reliable unique ID.
- Generate a `listing_id` from the row index (0-based or 1-based, be consistent).
- This identifier is used for API endpoints, URL routing, and linking between listings.

### Step 3 — Fix negative values

Some numeric fields contain `-1` as a data-entry error. These are **not** missing values; they are mistakes where the sign was entered incorrectly.

**Rule:** Convert any negative value to its positive equivalent using `abs()`.

Fields where this is known to occur:
- `main_property_property_composition_balconies`
- `main_property_property_composition_kitchens`
- `main_property_property_composition_living_rooms`
- `main_property_property_composition_bathrooms`
- `main_property_property_composition_bedrooms`

Apply `abs()` to all composition fields. If a negative value appears in other numeric fields (e.g., `main_property_floor`, `main_property_property_square`), apply the same rule.

### Step 4 — Handle null values

Null values (`null` in JSON, `None` in Python, `NaN` in pandas) indicate truly missing data. Handle by field type:

**Numeric fields (for display):**
- Keep as `None`/`null` in the API response.
- The frontend should display "N/A" or hide the field.

**Numeric fields (for ML):**
- `price_in_euro`: Drop the record if null — this is the prediction target.
- `main_property_property_square`: Drop the record if null — essential for prediction.
- `bedrooms`, `bathrooms`, `floor`: Impute with the median of the column, or drop if too many are missing.

**Categorical fields:**
- `furnishing_status`: Replace null with `"unknown"`.
- `property_status`, `property_type`: Replace null with `"unknown"`.

**Boolean fields:**
- `has_elevator`, `has_terrace`, `has_carport`, `has_garage`, `has_garden`, `has_parking_space`: Replace null with `false` (conservative default).

**Text fields:**
- `description`: Keep null as-is. Display "No description available" in the UI.

**Location fields:**
- `latitude`, `longitude`: Keep null. Exclude from distance-based comp calculations.
- `formatted_address`: Keep null. Display "Address not available" in the UI.

### Step 5 — Remove outliers

Before ML training, remove records that are clearly invalid or extreme:

- `price_in_euro` < 5,000 or > 2,000,000 EUR.
- `main_property_property_square` < 10 or > 1,000 m².

These thresholds are based on the Tirana residential market. Keep outlier-removed data for ML only; the full cleaned dataset (step 4 output) is used for display.

### Step 6 — Rename fields for API

Map the long source field names to short API-friendly names:

| Source field | API name |
|---|---|
| `price_in_euro` | `price_in_euro` |
| `main_property_property_square` | `square_meters` |
| `main_property_property_composition_bedrooms` | `bedrooms` |
| `main_property_property_composition_bathrooms` | `bathrooms` |
| `main_property_floor` | `floor` |
| `main_property_furnishing_status` | `furnishing_status` |
| `main_property_has_elevator` | `has_elevator` |
| `main_property_has_terrace` | `has_terrace` |
| `main_property_has_carport` | `has_carport` |
| `main_property_has_garage` | `has_garage` |
| `main_property_has_garden` | `has_garden` |
| `main_property_has_parking_space` | `has_parking_space` |
| `main_property_location_city_zone_formatted_address` | `address` |
| `main_property_location_lat` | `latitude` |
| `main_property_location_lng` | `longitude` |
| `main_property_property_status` | `property_status` |
| `main_property_property_type` | `property_type` |
| `main_property_description_text_content_original_text` | `description` |

### Step 7 — Prepare two datasets

After preprocessing, maintain two views of the data:

1. **Display dataset:** All cleaned records (steps 1–4 + step 6). Used by the API for listings and details.
2. **ML dataset:** Display dataset minus outliers (step 5). Used for model training and predictions.

## Summary of value handling

| Condition | Action |
|---|---|
| Value is `-1` (or any negative) | Convert to positive: `abs(value)` |
| Value is `null` (numeric, display) | Keep as null, UI shows "N/A" |
| Value is `null` (numeric, ML) | Impute with median or drop record |
| Value is `null` (boolean) | Default to `false` |
| Value is `null` (categorical) | Replace with `"unknown"` |
| Value is extreme outlier | Exclude from ML dataset only |

## Notes for AI coding agents

- Apply preprocessing once at application startup, not per-request.
- Keep the preprocessing code in a single module (e.g., `backend/preprocessing.py`).
- Log how many records were modified, dropped, or imputed.
- Make thresholds (outlier bounds) easy to change via constants.
- The same preprocessing logic must be used during model training and during prediction.
