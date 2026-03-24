# API Requirements — Tirana Real Estate Companion

## Purpose

Define the minimal backend API needed to support the web app:

- Browse listings with filters.
- View a listing’s details.
- Get an ML price estimate and fair range.
- Get comparable properties (comps).

This document is high level and will be complemented by a separate, detailed API contract file.

## General

- Framework: **Python Flask**.
- Style: JSON over HTTP.
- Base URL (local): `http://localhost:5000/api`.
- Methods: read-only (`GET`) for the first version.
- Auth: none (local, educational project).
- CORS: enabled for local development (allow `*` or specific localhost origins).
- All responses use a consistent JSON error format when failing (see Error handling below).

## Required endpoints

### 1. GET /listings

Returns a list of listing summaries, optionally filtered.

- Purpose:
  - Power the “Listings” page with filters.
- Key query parameters (all optional):
  - `min_price`, `max_price`
  - `min_bedrooms`, `max_bedrooms`
  - `min_bathrooms`, `max_bathrooms`
  - `min_sqm`, `max_sqm`
  - `furnishing_status`
  - `has_elevator`
  - `has_terrace`
  - `limit`, `offset`
- Response (per item, summary fields only):
  - `listing_id`
  - `price_in_euro`
  - `address`
  - `bedrooms`
  - `bathrooms`
  - `square_meters`
  - `floor`
  - `has_elevator`
  - `has_terrace`
  - `furnishing_status`

### 2. GET /listings/{listing_id}

Returns full details for one listing.

- Purpose:
  - Power the “Listing details” page.
- Path:
  - `listing_id` (internal stable id).
- Response (full details):
  - All fields needed for the details page, including:
    - Core info (price, size, rooms, floor).
    - Amenities.
    - Address and location.
    - Description text.

### 3. GET /listings/{listing_id}/estimate

Returns ML price estimate and fair range for one listing.

- Purpose:
  - Power the “Price estimate” block on the details page.
- Path:
  - `listing_id`.
- Response:
  - `listing_id`
  - `estimated_price`
  - `fair_range_low`
  - `fair_range_high`
  - Optional: `model_version`, `notes`.

### 4. GET /listings/{listing_id}/comps

Returns comparable listings for one listing.

- Purpose:
  - Power the “Comparable properties” section.
- Path:
  - `listing_id`.
- Query parameter (optional):
  - `limit` (default 5).
- Response:
  - `listing_id` (target listing).
  - `comps` (array of comparables), each with:
    - `listing_id`
    - `price_in_euro`
    - `address`
    - `bedrooms`
    - `bathrooms`
    - `square_meters`
    - `distance_meters` (if available)
    - `similarity_reason` (short text).

## Error handling

- All error responses are JSON using this structure:
  ```json
  {
    "error": {
      "code": "NOT_FOUND",
      "message": "Listing not found",
      "details": null
    }
  }
  ```
- Common cases:
  - 400 — invalid parameters.
  - 404 — listing not found.
  - 500 — unexpected server error.

## Non-goals for v1

The first version does **not** need:

- Create/update/delete endpoints.
- Authentication or user accounts.
- Real-time features.
- External API integrations.

