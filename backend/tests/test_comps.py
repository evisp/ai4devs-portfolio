"""
tests/test_comps.py — Tests for Phase 5: Comparable properties endpoint.

Tests cover:
  - Returning maximum `limit` number of items.
  - Ensuring the target listing itself is excluded from comps.
  - Handling of missing lat/lng (tests graceful penalty fallback).
  - Schema adherence.
  - 404 for unknown listing_id.

Run from backend/:
    pytest tests/test_comps.py -v
"""

import sys
import os
import pytest

# Make sure the backend package is importable when pytest is run from backend/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as flask_app          # noqa: E402
import comps_service             # noqa: E402


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
def target_listing_id():
    """Return the listing_id of the very first record in the dataset."""
    return flask_app.display_data[0]["listing_id"]


@pytest.fixture
def listing_without_coords():
    """Find a listing that doesn't have latitude/longitude."""
    for record in flask_app.display_data:
        if record.get("latitude") is None or record.get("longitude") is None:
            return record["listing_id"]
    pytest.skip("No listing without coordinates found in dataset.")


# ---------------------------------------------------------------------------
# Schema validation helper
# ---------------------------------------------------------------------------

COMP_REQUIRED_KEYS = {
    "listing_id",
    "price_in_euro",
    "address",
    "bedrooms",
    "bathrooms",
    "square_meters",
    "distance_meters",
    "similarity_reason",
}


def _assert_schema(comp: dict):
    """Assert that the comp dict has all ComparableListing keys."""
    assert COMP_REQUIRED_KEYS.issubset(comp.keys()), (
        f"Missing keys: {COMP_REQUIRED_KEYS - comp.keys()}"
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestCompsEndpointSchema:
    def test_schema_on_known_listing(self, client, target_listing_id):
        resp = client.get(f"/api/listings/{target_listing_id}/comps")
        assert resp.status_code == 200
        data = resp.get_json()
        
        assert "listing_id" in data
        assert data["listing_id"] == target_listing_id
        assert "comps" in data
        
        assert len(data["comps"]) > 0
        for comp in data["comps"]:
            _assert_schema(comp)


class TestCompsLogic:
    def test_limit_parameter_respected(self, client, target_listing_id):
        # Default limit is 5
        resp = client.get(f"/api/listings/{target_listing_id}/comps")
        data = resp.get_json()
        assert len(data["comps"]) == 5
        
        # Custom limit
        resp = client.get(f"/api/listings/{target_listing_id}/comps?limit=2")
        data = resp.get_json()
        assert len(data["comps"]) == 2

    def test_listing_does_not_return_itself(self, client, target_listing_id):
        resp = client.get(f"/api/listings/{target_listing_id}/comps?limit=10")
        data = resp.get_json()
        
        comp_ids = [c["listing_id"] for c in data["comps"]]
        assert target_listing_id not in comp_ids, "Listing should not be its own comp"

    def test_listing_without_coords_handled_gracefully(self, client, listing_without_coords):
        # Even without lat/lng, we still get comps based on size/rooms
        resp = client.get(f"/api/listings/{listing_without_coords}/comps")
        assert resp.status_code == 200
        data = resp.get_json()
        
        comps = data["comps"]
        assert len(comps) > 0
        
        # Distance should be null because target has no coordinates
        for comp in comps:
            assert comp["distance_meters"] is None
            
    def test_haversine_formula(self):
        # Tirana center vs Tirana east (approx 3km)
        lat1, lon1 = 41.3275, 19.8187
        lat2, lon2 = 41.3275, 19.8546
        
        dist_m = comps_service.haversine_distance_meters(lat1, lon1, lat2, lon2)
        assert dist_m is not None
        assert 2900 < dist_m < 3100  # roughly 3km


class TestCompsEndpoint404:
    def test_unknown_id_returns_404(self, client):
        resp = client.get("/api/listings/999999/comps")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "error" in data
        assert data["error"]["code"] == "NOT_FOUND"
