"""Quick smoke test — run from backend/ to verify comparable property generation."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app, comps_service

target_id = 9
listing = next((r for r in app.display_data if r["listing_id"] == target_id), None)

if listing is None:
    print("ERROR: target listing not found"); sys.exit(1)

print(f"--- TARGET LISTING (ID: {target_id}) ---")
print(f"Price: €{listing.get('price_in_euro', 0):,.0f}")
print(f"Size : {listing.get('square_meters')} sqm")
print(f"Rooms: {listing.get('bedrooms')} bed, {listing.get('bathrooms')} bath")
print(f"Address: {listing.get('address')}")
print(f"Coords: {listing.get('latitude')}, {listing.get('longitude')}")

print("\n--- COMPARABLE LISTINGS ---")
comps = comps_service.get_similar_listings(target_id, app.display_data, limit=3)

for idx, comp in enumerate(comps, start=1):
    print(f"\nComp {idx} (ID: {comp['listing_id']}):")
    print(f"Reason  : {comp['similarity_reason']}")
    print(f"Price   : €{comp.get('price_in_euro', 0):,.0f}")
    if comp['distance_meters'] is not None:
        print(f"Distance: {comp['distance_meters']}m")
    print(f"Size    : {comp.get('square_meters')} sqm")
    print(f"Rooms   : {comp.get('bedrooms')} bed, {comp.get('bathrooms')} bath")
