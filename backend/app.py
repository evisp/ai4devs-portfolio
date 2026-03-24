"""
app.py — Flask application for Tirana Real Estate Companion.

Exposes the API defined in docs/api/08-api-contract.yaml:
  GET /api/listings              — browse with filters + pagination
  GET /api/listings/<id>         — listing details
  GET /api/listings/<id>/estimate — ML price estimate (stub)
  GET /api/listings/<id>/comps   — comparable properties (stub)
"""

import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from preprocessing import load_and_preprocess

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)  # Allow all origins for local development

# ---------------------------------------------------------------------------
# Load data at startup
# ---------------------------------------------------------------------------

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tirana_house_prices.json")

logger.info("Loading and preprocessing dataset …")
display_data, ml_data = load_and_preprocess(DATA_PATH)
# Build a lookup dict for O(1) access by listing_id
listings_by_id = {r["listing_id"]: r for r in display_data}
logger.info("Ready — %d listings available, %d in ML dataset", len(display_data), len(ml_data))

# ---------------------------------------------------------------------------
# Summary fields (ListingSummary schema)
# ---------------------------------------------------------------------------

SUMMARY_FIELDS = [
    "listing_id",
    "price_in_euro",
    "address",
    "bedrooms",
    "bathrooms",
    "square_meters",
    "floor",
    "has_elevator",
    "has_terrace",
    "furnishing_status",
]


def _summary(record: dict) -> dict:
    """Return only the ListingSummary fields."""
    return {k: record.get(k) for k in SUMMARY_FIELDS}


# ---------------------------------------------------------------------------
# Error helpers
# ---------------------------------------------------------------------------

def _error_response(code: str, message: str, status: int, details=None):
    """Return a JSON error response matching the ErrorResponse schema."""
    return jsonify({
        "error": {
            "code": code,
            "message": message,
            "details": details,
        }
    }), status


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/listings", methods=["GET"])
def get_listings():
    """Browse listings with optional filters and pagination."""
    try:
        filtered = list(display_data)  # start with all

        # --- Filters ---
        min_price = request.args.get("min_price", type=float)
        max_price = request.args.get("max_price", type=float)
        min_bedrooms = request.args.get("min_bedrooms", type=int)
        max_bedrooms = request.args.get("max_bedrooms", type=int)
        min_bathrooms = request.args.get("min_bathrooms", type=int)
        max_bathrooms = request.args.get("max_bathrooms", type=int)
        min_sqm = request.args.get("min_sqm", type=float)
        max_sqm = request.args.get("max_sqm", type=float)
        furnishing = request.args.get("furnishing_status", type=str)
        elevator = request.args.get("has_elevator", type=str)
        terrace = request.args.get("has_terrace", type=str)

        if min_price is not None:
            filtered = [r for r in filtered if r.get("price_in_euro") is not None and r["price_in_euro"] >= min_price]
        if max_price is not None:
            filtered = [r for r in filtered if r.get("price_in_euro") is not None and r["price_in_euro"] <= max_price]
        if min_bedrooms is not None:
            filtered = [r for r in filtered if r.get("bedrooms") is not None and r["bedrooms"] >= min_bedrooms]
        if max_bedrooms is not None:
            filtered = [r for r in filtered if r.get("bedrooms") is not None and r["bedrooms"] <= max_bedrooms]
        if min_bathrooms is not None:
            filtered = [r for r in filtered if r.get("bathrooms") is not None and r["bathrooms"] >= min_bathrooms]
        if max_bathrooms is not None:
            filtered = [r for r in filtered if r.get("bathrooms") is not None and r["bathrooms"] <= max_bathrooms]
        if min_sqm is not None:
            filtered = [r for r in filtered if r.get("square_meters") is not None and r["square_meters"] >= min_sqm]
        if max_sqm is not None:
            filtered = [r for r in filtered if r.get("square_meters") is not None and r["square_meters"] <= max_sqm]
        if furnishing is not None:
            filtered = [r for r in filtered if r.get("furnishing_status") == furnishing]
        if elevator is not None:
            val = elevator.lower() in ("true", "1", "yes")
            filtered = [r for r in filtered if r.get("has_elevator") == val]
        if terrace is not None:
            val = terrace.lower() in ("true", "1", "yes")
            filtered = [r for r in filtered if r.get("has_terrace") == val]

        # --- Pagination ---
        total = len(filtered)
        limit = request.args.get("limit", default=20, type=int)
        offset = request.args.get("offset", default=0, type=int)

        if limit < 0 or offset < 0:
            return _error_response("BAD_REQUEST", "limit and offset must be non-negative", 400)

        page = filtered[offset: offset + limit]

        return jsonify({
            "items": [_summary(r) for r in page],
            "total": total,
        })

    except Exception as e:
        logger.exception("Error in GET /api/listings")
        return _error_response("INTERNAL_ERROR", str(e), 500)


@app.route("/api/listings/<int:listing_id>", methods=["GET"])
def get_listing_detail(listing_id: int):
    """Return full details for one listing."""
    listing = listings_by_id.get(listing_id)
    if listing is None:
        return _error_response("NOT_FOUND", f"Listing {listing_id} not found", 404)

    # Return all fields (ListingDetails schema)
    return jsonify(listing)


@app.route("/api/listings/<int:listing_id>/estimate", methods=["GET"])
def get_listing_estimate(listing_id: int):
    """Return ML price estimate (stub until Phase 4)."""
    listing = listings_by_id.get(listing_id)
    if listing is None:
        return _error_response("NOT_FOUND", f"Listing {listing_id} not found", 404)

    # Stub response — will be replaced in Phase 4
    return jsonify({
        "listing_id": listing_id,
        "estimated_price": None,
        "fair_range_low": None,
        "fair_range_high": None,
        "model_version": None,
        "notes": "ML model not yet integrated. Coming in Phase 4.",
    })


@app.route("/api/listings/<int:listing_id>/comps", methods=["GET"])
def get_listing_comps(listing_id: int):
    """Return comparable properties (stub until Phase 5)."""
    listing = listings_by_id.get(listing_id)
    if listing is None:
        return _error_response("NOT_FOUND", f"Listing {listing_id} not found", 404)

    # Stub response — will be replaced in Phase 5
    return jsonify({
        "listing_id": listing_id,
        "comps": [],
    })


# ---------------------------------------------------------------------------
# Global error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return _error_response("NOT_FOUND", "The requested resource was not found", 404)


@app.errorhandler(500)
def internal_error(e):
    return _error_response("INTERNAL_ERROR", "An unexpected error occurred", 500)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
