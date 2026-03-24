# Dataset Overview — Tirana House Prices

## Purpose of this document

This document explains the dataset used in the project.

## Dataset file

The main dataset file is:

`data/tirana_house_prices.json`

This file contains residential property listing records for Tirana.

## File structure

- The file is a JSON array.
- Each item in the array represents one property listing.
- Each listing contains structured property fields and may also include free-text description content.

## Project usage

This dataset is used for three main purposes:

1. Display listings in the web application.
2. Show listing details for an individual property.
3. Train a machine learning model to estimate property price and retrieve comparable properties.

## Prediction target

The recommended target variable for price prediction is:

`price_in_euro`

This field should be treated as the main label for the ML model whenever it is available and valid.

## Main field groups

For implementation purposes, the dataset can be understood in the following groups.

### 1. Identification and display fields
These fields are useful for showing listings in the UI:
- `main_property_location_city_zone_formatted_address`
- `main_property_price`
- `main_property_price_currency`
- `price_in_euro`

If the source data does not include a stable unique identifier, the preprocessing step should create one.

### 2. Core structured property features
These fields are likely to be the most useful for filtering, display, and baseline prediction:
- `main_property_property_square`
- `main_property_property_composition_bedrooms`
- `main_property_property_composition_bathrooms`
- `main_property_floor`
- `main_property_furnishing_status`
- `main_property_has_elevator`
- `main_property_has_terrace`

### 3. Additional structured features
These fields may improve filtering, comparables, or modeling depending on data quality:
- `main_property_property_composition_balconies`
- `main_property_property_composition_kitchens`
- `main_property_property_composition_living_rooms`
- `main_property_has_carport`
- `main_property_has_garage`
- `main_property_has_garden`
- `main_property_has_parking_space`

### 4. Location fields
These fields are especially important for comparable-property selection:
- `main_property_location_city_zone_city_city_name`
- `main_property_location_city_zone_formatted_address`
- `main_property_location_lat`
- `main_property_location_lng`

Latitude and longitude can be used to estimate distance between listings.

### 5. Listing metadata fields
These fields describe listing context and may be useful for filtering or validation:
- `main_property_property_status`
- `main_property_property_type`

### 6. Free-text field
This field contains the original listing description:
- `main_property_description_text_content_original_text`

This field is optional for the first version of the project. It can be displayed in the UI even if it is not used in the initial ML model.

## Field reference

| Field | Type | Meaning | Implementation note |
|---|---|---|---|
| `main_property_description_text_content_original_text` | string | Original property description text | Useful for display; optional for baseline ML. |
| `main_property_floor` | number or null | Floor number | Can be used in display and modeling. |
| `main_property_furnishing_status` | string or null | Furnishing status | Good candidate for filtering and features. |
| `main_property_has_carport` | boolean or null | Carport availability | Optional feature. |
| `main_property_has_elevator` | boolean or null | Elevator availability | Useful for filtering, details, and ML. |
| `main_property_has_garage` | boolean or null | Garage availability | Optional feature. |
| `main_property_has_garden` | boolean or null | Garden availability | Optional feature. |
| `main_property_has_parking_space` | boolean or null | Parking space availability | Optional feature. |
| `main_property_has_terrace` | boolean or null | Terrace availability | Useful for filtering, details, and ML. |
| `main_property_location_city_zone_city_city_name` | string or null | City name | Useful for validation and grouping. |
| `main_property_location_city_zone_formatted_address` | string or null | Human-readable address | Useful for display. |
| `main_property_location_lat` | number or null | Latitude | Useful for location-based comps. |
| `main_property_location_lng` | number or null | Longitude | Useful for location-based comps. |
| `main_property_price` | number or null | Raw listing price | Secondary price field; prefer `price_in_euro` as target. |
| `main_property_price_currency` | string or null | Price currency | Useful for validation. |
| `main_property_property_composition_balconies` | number or null | Number of balconies | Optional structured feature. |
| `main_property_property_composition_bathrooms` | number or null | Number of bathrooms | Core filtering and ML feature. |
| `main_property_property_composition_bedrooms` | number or null | Number of bedrooms | Core filtering and ML feature. |
| `main_property_property_composition_kitchens` | number or null | Number of kitchens | Optional structured feature. |
| `main_property_property_composition_living_rooms` | number or null | Number of living rooms | Optional structured feature. |
| `main_property_property_status` | string or null | Listing status | Useful for validation or filtering. |
| `main_property_property_type` | string or null | Property type | Useful for filtering or restricting scope. |
| `price_in_euro` | number or null | Listing price in EUR | Recommended prediction target. |
| `main_property_property_square` | number or null | Property area in square meters | Core filtering and ML feature. |

## Minimum fields needed for the MVP

The first version of the application should prioritize the following fields:

- `price_in_euro`
- `main_property_property_square`
- `main_property_property_composition_bedrooms`
- `main_property_property_composition_bathrooms`
- `main_property_floor`
- `main_property_furnishing_status`
- `main_property_has_elevator`
- `main_property_has_terrace`
- `main_property_location_city_zone_formatted_address`
- `main_property_location_lat`
- `main_property_location_lng`
- `main_property_description_text_content_original_text`

These fields are enough to support listing display, filtering, property details, price prediction, and comparable-property selection.

## Data quality assumptions

The implementation should assume the following:

- Some fields may be missing and stored as `null`.
- Some records may contain abnormal values.
- Some fields may be more complete than others.
- Some listings may not include enough information for all UI or ML tasks.
- The dataset may not contain a stable unique listing identifier.

These assumptions should be handled explicitly during preprocessing.

## Negative values

Some numeric fields in this dataset contain `-1` as a value. These are **data-entry errors**, not valid data.

The correct handling is:
- Convert any `-1` value to its positive equivalent using `abs()`. For example, `balconies: -1` becomes `balconies: 1`.
- This rule applies to all composition fields (`balconies`, `kitchens`, `living_rooms`, `bathrooms`, `bedrooms`) and any other numeric field where `-1` appears.
- Do **not** treat `-1` as null or missing. After conversion, the value is a real positive number.

This rule is separate from handling `null` values, which are described below.

## Missing values

Missing values are stored as `null` in this dataset. They are distinct from `-1` (which is a data-entry error, see above).

A preprocessing plan should define how to handle them, for example:
- Drop records only when required target or essential fields are missing.
- Fill numeric values carefully when appropriate.
- Keep missing categorical values as `unknown` when useful.
- Preserve nulls in fields that are optional for display only.

The handling strategy should be simple, documented, and consistent.

## Outliers and abnormal values

The dataset may contain unusual prices, extreme square-meter values, or inconsistent records.

Before training the model, the project should define rules for identifying and handling outliers. These rules may include:
- Removing clearly invalid rows.
- Capping extreme values.
- Keeping rare but plausible values if they reflect the market.

The chosen strategy should be documented clearly and applied consistently.

## Identifier requirement

If the source data does not provide a stable listing identifier, preprocessing must create one.

A simple approach is to generate an internal `listing_id` from the row index after loading the dataset. This identifier should be used by the application to:
- Render listing links.
- Open details pages.
- Retrieve comparable properties.
- Connect UI interactions to backend logic.

## Recommended first-use strategy

For the first implementation, use the dataset in a simple and safe way:

1. Load the JSON file into a tabular structure.
2. Create a stable internal identifier.
3. Keep only fields needed for the MVP.
4. Validate the prediction target.
5. Inspect missing values and outliers.
6. Prepare a cleaned dataset for the app and for model training.

This approach keeps the first version understandable and reduces unnecessary complexity.

## Notes for AI coding agents

When using this dataset in code, follow these rules:

- Do not assume every field is present in every record.
- Treat `price_in_euro` as the main prediction target.
- Negative values (`-1`) are data-entry errors — convert them to positive with `abs()`.
- Distinguish `null` (truly missing) from `-1` (erroneous negative → convert to positive).
- Prefer structured features before using text features.
- Create a stable internal identifier if none exists.
- Use latitude and longitude when available for comparable-property selection.
- Keep preprocessing decisions explicit and reproducible.
- Avoid hidden assumptions about null values or field formats.
- See `docs/concept/04-data-preprocessing.md` for the complete preprocessing pipeline.

