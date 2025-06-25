from typing import List, Dict, Any, Generator
import os
import requests
import hashlib
import json
from core.cache_utils import cache_generator_response, safe_cache_key
from profiles.models.business_profile import BusinessProfile

def serper_cache_key(profile, mode="nearby", max_results=5):
    base = json.dumps({
        "profile": profile.json(),
        "mode": mode,
        "max_results": max_results
    }, sort_keys=True)
    return safe_cache_key("serper_competitors:" + hashlib.sha256(base.encode()).hexdigest())

@cache_generator_response(serper_cache_key)
def get_competitors_from_serper(
    profile: BusinessProfile,
    mode: str = "nearby",
    max_results: int = 5
) -> Generator[Dict, None, None]:
    """
    Uses the Serper API to search for business competitors.
    mode: "nearby" (default) or "similar"
    Returns a generator of competitor dicts (serializable for caching).
    """

    # Build the search query
    if mode == "nearby":
        query = f"{profile.category} near {profile.address}"
    elif mode == "similar":
        query = f"{profile.category} similar to {profile.name} in {profile.address}"
    else:
        raise ValueError("mode must be 'nearby' or 'similar'")

    serper_api_key = os.environ.get("SERPER_API_KEY")
    if not serper_api_key:
        raise RuntimeError("SERPER_API_KEY environment variable is not set.")

    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "gl": "fi",
        "hl": "en"
    }
    try:
        response = requests.post(
            "https://google.serper.dev/places",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        # Log error and return no competitors
        print(f"Error fetching competitors from Serper API: {e}")
        return

    try:
        data = response.json()
    except Exception as e:
        print(f"Error parsing Serper API response as JSON: {e}")
        return

    places = data.get("places", [])[:max_results]

    for place in places:
        try:
            competitor = {
                "name": place.get("title", ""),
                "address": place.get("address", ""),
                "rating": float(place.get("rating", 0.0)) if place.get("rating") is not None else 0.0,
                "review_count": int(place.get("ratingCount", 0)) if place.get("ratingCount") is not None else 0,
                "price_level": place.get("priceLevel", ""),
                "category": place.get("category", ""),
                "description": place.get("description", ""),
                "hours": place.get("hours", []) if isinstance(place.get("hours", []), list) else [],
                "menu_url": place.get("menu", ""),
                "website": place.get("website", ""),
                "phone": place.get("phoneNumber", ""),
                "photos": place.get("photos", []) if isinstance(place.get("photos", []), list) else [],
            }
            # Filter out competitors with missing name or address
            if not competitor["name"] or not competitor["address"]:
                continue
            yield competitor
        except Exception as e:
            print(f"Error mapping competitor data: {e}")
            continue
