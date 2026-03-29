"""
tests/test_estimate.py — Tests for Phase 4: ML price estimate endpoint.

Tests cover:
  - Real ML predictions returned (not nulls).
  - Response shape matches EstimateResponse schema.
  - 404 for unknown listing_id.
  - Graceful handling when required features are missing (notes, nulls).
  - Consistency: same listing always returns the same estimate.

Run from backend/:
    pytest tests/test_estimate.py -v
"""

import sys
import os
import pytest

# Make sure the backend package is importable when pytest is run from backend/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as flask_app          # noqa: E402  (imports the Flask app)
import ml_service                # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Return a Flask test client with testing mode enabled."""
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as c:
        yield c


@pytest.fixture
def first_listing_id():
    """Return the listing_id of the very first record in the dataset."""
    return flask_app.display_data[0]["listing_id"]


@pytest.fixture
def listing_with_all_features():
    """
    Return the first listing_id that has *all* required numeric features
    (square_meters, bedrooms, bathrooms, floor) present and non-null.
    """
    required = ["square_meters", "bedrooms", "bathrooms", "floor"]
    for record in flask_app.display_data:
        if all(record.get(f) is not None for f in required):
            return record["listing_id"]
    pytest.skip("No listing with all required features found in dataset.")


# ---------------------------------------------------------------------------
# Schema validation helper
# ---------------------------------------------------------------------------

ESTIMATE_REQUIRED_KEYS = {
    "listing_id",
    "estimated_price",
    "fair_range_low",
    "fair_range_high",
    "model_version",
    "notes",
}


def _assert_schema(data: dict):
    """Assert that the response dict has all EstimateResponse keys."""
    assert ESTIMATE_REQUIRED_KEYS.issubset(data.keys()), (
        f"Missing keys: {ESTIMATE_REQUIRED_KEYS - data.keys()}"
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestEstimateEndpointSchema:
    """Response always has the correct shape regardless of outcome."""

    def test_schema_on_known_listing(self, client, first_listing_id):
        resp = client.get(f"/api/listings/{first_listing_id}/estimate")
        assert resp.status_code == 200
        data = resp.get_json()
        _assert_schema(data)
        assert data["listing_id"] == first_listing_id

    def test_listing_id_matches_request(self, client, listing_with_all_features):
        lid = listing_with_all_features
        resp = client.get(f"/api/listings/{lid}/estimate")
        data = resp.get_json()
        assert data["listing_id"] == lid


class TestEstimateEndpoint404:
    """404 is returned for unknown listing_id values."""

    def test_unknown_id_returns_404(self, client):
        resp = client.get("/api/listings/999999/estimate")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "error" in data
        assert data["error"]["code"] == "NOT_FOUND"

    def test_negative_id_returns_404(self, client):
        # Negative ids cannot match any listing (listing_id is 0-based index)
        resp = client.get("/api/listings/-1/estimate")
        # Flask routes don't match negative int path params by default → 404
        assert resp.status_code == 404


class TestRealPredictions:
    """When the model is loaded and features are present, we get real numbers."""

    def test_estimate_returns_non_null_price(self, client, listing_with_all_features):
        resp = client.get(f"/api/listings/{listing_with_all_features}/estimate")
        assert resp.status_code == 200
        data = resp.get_json()

        # Only test real prediction if model is loaded
        if not ml_service._model_ready():
            pytest.skip("ML model not loaded — skipping real-prediction test.")

        assert data["estimated_price"] is not None, "Expected a real price estimate"
        assert data["fair_range_low"] is not None
        assert data["fair_range_high"] is not None
        assert data["model_version"] is not None

    def test_fair_range_bounds(self, client, listing_with_all_features):
        resp = client.get(f"/api/listings/{listing_with_all_features}/estimate")
        data = resp.get_json()

        if not ml_service._model_ready() or data["estimated_price"] is None:
            pytest.skip("ML model not loaded or estimate is null.")

        low  = data["fair_range_low"]
        est  = data["estimated_price"]
        high = data["fair_range_high"]

        assert low < est < high, (
            f"Expected low < estimated < high, got {low} / {est} / {high}"
        )

    def test_price_is_positive(self, client, listing_with_all_features):
        resp = client.get(f"/api/listings/{listing_with_all_features}/estimate")
        data = resp.get_json()

        if not ml_service._model_ready() or data["estimated_price"] is None:
            pytest.skip("ML model not loaded or estimate is null.")

        assert data["estimated_price"] > 0, "Estimated price must be positive"
        assert data["fair_range_low"]  > 0, "Fair range low must be positive"
        assert data["fair_range_high"] > 0, "Fair range high must be positive"

    def test_prediction_is_consistent(self, client, listing_with_all_features):
        """Same listing should always return the same estimate."""
        resp1 = client.get(f"/api/listings/{listing_with_all_features}/estimate")
        resp2 = client.get(f"/api/listings/{listing_with_all_features}/estimate")
        assert resp1.get_json()["estimated_price"] == resp2.get_json()["estimated_price"]

    def test_model_version_is_baseline(self, client, listing_with_all_features):
        resp = client.get(f"/api/listings/{listing_with_all_features}/estimate")
        data = resp.get_json()

        if not ml_service._model_ready() or data["model_version"] is None:
            pytest.skip("ML model not loaded.")

        assert data["model_version"] == "baseline-v1"


class TestMissingFeatureHandling:
    """When a listing lacks required features, a note is returned."""

    def test_missing_features_returns_null_estimate_with_note(self):
        """Unit-test ml_service directly with a bare listing dict."""
        if not ml_service._model_ready():
            pytest.skip("ML model not loaded.")

        # A listing with missing numeric features
        sparse_listing = {
            "listing_id": 9999,
            "square_meters": None,
            "bedrooms": None,
            "bathrooms": None,
            "floor": None,
            "has_elevator": False,
            "has_terrace": False,
            "furnishing_status": "unknown",
        }
        result = ml_service.estimate_price(sparse_listing)
        assert result["estimated_price"] is None
        assert result["fair_range_low"] is None
        assert result["fair_range_high"] is None
        assert result["notes"] is not None
        assert "missing" in result["notes"].lower()

    def test_partial_features_returns_null_with_note(self):
        """A listing missing only one required field still can't be predicted."""
        if not ml_service._model_ready():
            pytest.skip("ML model not loaded.")

        partial_listing = {
            "listing_id": 9998,
            "square_meters": 80.0,
            "bedrooms": 2,
            "bathrooms": None,   # missing
            "floor": 3,
            "has_elevator": True,
            "has_terrace": False,
            "furnishing_status": "furnished",
        }
        result = ml_service.estimate_price(partial_listing)
        assert result["estimated_price"] is None
        assert "bathrooms" in result["notes"]

    def test_all_features_present_gives_prediction(self):
        """Full feature vector → real prediction (unit test)."""
        if not ml_service._model_ready():
            pytest.skip("ML model not loaded.")

        full_listing = {
            "listing_id": 1,
            "square_meters": 90.0,
            "bedrooms": 3,
            "bathrooms": 1,
            "floor": 2,
            "has_elevator": True,
            "has_terrace": False,
            "furnishing_status": "furnished",
        }
        result = ml_service.estimate_price(full_listing)
        assert result["estimated_price"] is not None
        assert result["estimated_price"] > 0
