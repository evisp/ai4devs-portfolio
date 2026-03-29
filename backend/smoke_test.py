"""Quick smoke test — run from backend/ to verify a real ML estimate."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app, ml_service

required = ["square_meters", "bedrooms", "bathrooms", "floor"]
listing = next(
    (r for r in app.display_data if all(r.get(f) is not None for f in required)),
    None,
)
if listing is None:
    print("ERROR: no listing with all required features found"); sys.exit(1)

print(f"Listing ID : {listing['listing_id']}")
for f in required + ["has_elevator", "has_terrace", "furnishing_status"]:
    print(f"  {f}: {listing.get(f)}")

result = ml_service.estimate_price(listing)
print("\nEstimate response:")
print(json.dumps(result, indent=2))
print(f"\nActual price : €{listing.get('price_in_euro'):,.0f}")
