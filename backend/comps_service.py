"""
comps_service.py — Comparable properties service for Tirana Real Estate Companion.

Phase 5 of the development roadmap.

Responsibilities:
  - Provide a function to find comparable properties given a target listing.
  - Compute similarity using Haversine geographic distance and feature differences.
  - Return formatted ComparableListing objects.
"""

import math
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants / Weights
# ---------------------------------------------------------------------------

# Penalty weights (Cost multiplier). Lower cost means more similar.
WEIGHT_DISTANCE_KM = 1.0   # 1 km = 1.0 penalty
WEIGHT_SQM         = 0.1   # 10 sqm = 1.0 penalty
WEIGHT_ROOMS       = 1.5   # 1 room (bed/bath) difference = 1.5 penalty

# If coordinates are completely missing for either the target or the comp,
# we apply a flat geographical penalty to favor properties that do have known
# proximity. 5.0 penalty is equivalent to being 5km away.
MISSING_COORD_PENALTY = 5.0


# ---------------------------------------------------------------------------
# Distance computation
# ---------------------------------------------------------------------------

def haversine_distance_meters(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) in meters.
    """
    # Convert decimal degrees to radians
    try:
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    except TypeError:
        # None passed in
        return None

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth radius in meters
    r = 6371000
    
    return c * r


# ---------------------------------------------------------------------------
# Scoring / Comparison
# ---------------------------------------------------------------------------

def _calculate_cost_and_reason(target: dict, comp: dict):
    """
    Compare two listings and return the total penalty cost and a human 
    readable string explaining their similarity.
    """
    cost = 0.0
    reasons = []

    # 1. Geographic distance
    dist_m = None
    if target.get("latitude") and target.get("longitude") and \
       comp.get("latitude") and comp.get("longitude"):
        dist_m = haversine_distance_meters(
            target["latitude"], target["longitude"],
            comp["latitude"], comp["longitude"]
        )
        if dist_m is not None:
            dist_km = dist_m / 1000.0
            cost += dist_km * WEIGHT_DISTANCE_KM
            
            if dist_km < 1.0:
                reasons.append(f"{dist_km*1000:.0f}m away")
            else:
                reasons.append(f"{dist_km:.1f}km away")
    else:
        # Penalize lack of geographical data
        cost += MISSING_COORD_PENALTY

    # 2. Size similarity
    sqm_t = target.get("square_meters")
    sqm_c = comp.get("square_meters")
    
    if sqm_t is not None and sqm_c is not None:
        sqm_diff = abs(sqm_t - sqm_c)
        cost += (sqm_diff * WEIGHT_SQM)
        if sqm_diff <= 10:
            reasons.append("similar size")
    else:
        # Penalize missing size slightly
        cost += 2.0

    # 3. Room similarity
    bed_t = target.get("bedrooms")
    bed_c = comp.get("bedrooms")
    bath_t = target.get("bathrooms")
    bath_c = comp.get("bathrooms")
    
    room_diff = 0
    room_matched = False
    
    if bed_t is not None and bed_c is not None:
        room_diff += abs(bed_t - bed_c)
        if bed_t == bed_c:
            room_matched = True
            reasons.append(f"same bedrooms ({bed_t})")
            
    if bath_t is not None and bath_c is not None:
        room_diff += abs(bath_t - bath_c)
        if bath_t == bath_c and not room_matched: 
            # only mention bath match if bed wasn't exactly same, to prevent long reasons
            reasons.append(f"same bathrooms ({bath_t})")
            
    cost += (room_diff * WEIGHT_ROOMS)
    
    # Ensure reason string isn't empty if nothing perfectly matched
    if not reasons:
        reasons.append("comparable features")
        
    reason_str = ", ".join(reasons).capitalize()

    return cost, reason_str, dist_m


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_similar_listings(target_id: int, all_listings: list, limit: int = 5):
    """
    Find the most comparable listings for the given target_id.
    
    Returns a list of dicts matching the `ComparableListing` schema.
    """
    # 1. Find the target listing
    target = None
    for r in all_listings:
        if r["listing_id"] == target_id:
            target = r
            break
            
    if not target:
        return []

    # 2. Score all other listings
    scored_comps = []
    for comp in all_listings:
        if comp["listing_id"] == target_id:
            continue
            
        cost, reason, dist_m = _calculate_cost_and_reason(target, comp)
        
        scored_comps.append({
            "listing_id": comp.get("listing_id"),
            "price_in_euro": comp.get("price_in_euro"),
            "address": comp.get("address"),
            "bedrooms": comp.get("bedrooms"),
            "bathrooms": comp.get("bathrooms"),
            "square_meters": comp.get("square_meters"),
            "distance_meters": round(dist_m) if dist_m is not None else None,
            "similarity_reason": reason,
            "_cost": cost # Temporary sorting key
        })
        
    # 3. Sort by cost (ascending) and take top N
    scored_comps.sort(key=lambda x: x["_cost"])
    top_comps = scored_comps[:limit]
    
    # 4. Remove internal cost key
    for comp in top_comps:
        del comp["_cost"]
        
    return top_comps
