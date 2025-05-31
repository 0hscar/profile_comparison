from comparator.utils.cache_utils import safe_cache_key
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.cache import cache
from comparator.utils.business_utils import get_places_cards, filter_out_user_restaurant

def get_cached_and_uncached(restaurants):
    cached = []
    uncached = []
    for r in restaurants:
        cache_key = safe_cache_key(f"user_restaurant:{r.get('title','').lower().strip()}|{r.get('address','').lower().strip()}")
        cached_data = cache.get(cache_key)
        if cached_data:
            cached.append(cached_data['user_restaurant'])
        else:
            uncached.append(r)
    return cached, uncached

@csrf_exempt
def fetch_restaurant_groups(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
        user_business_name = data.get("user_business_name")
        user_business_location = data.get("user_business_location")
        gl = data.get("gl", "fi")
        num_places = int(data.get("num_places", 5))
        user_category = data.get("user_business_category") or "restaurant"

        if not user_business_name or not user_business_location:
            return JsonResponse({"error": "user_business_name and user_business_location are required"}, status=400)

        # Fetch nearby restaurants (generic "restaurant" query)
        # Fetch similar restaurants (using the user's category eg. "steak")
        nearby_cards = get_places_cards("restaurant", user_business_location, gl=gl, num_places=num_places, fullInfo=False)
        similar_cards = get_places_cards(user_category, user_business_location, gl=gl, num_places=num_places, fullInfo=False)

        # Filter out the user's own restaurant from both lists
        nearby_cards = filter_out_user_restaurant(nearby_cards, user_business_name, user_business_location)
        similar_cards = filter_out_user_restaurant(similar_cards, user_business_name, user_business_location)

        # Caching logic for each restaurant
        cached_nearby, uncached_nearby = get_cached_and_uncached(nearby_cards)
        cached_similar, uncached_similar = get_cached_and_uncached(similar_cards)

        # Cache new results individually
        for r in uncached_nearby:
            cache_key = safe_cache_key(f"user_restaurant:{r.get('title','').lower().strip()}|{r.get('address','').lower().strip()}")
            cache.set(cache_key, {"user_restaurant": r}, timeout=60*60)
        for r in uncached_similar:
            cache_key = safe_cache_key(f"user_restaurant:{r.get('title','').lower().strip()}|{r.get('address','').lower().strip()}")
            cache.set(cache_key, {"user_restaurant": r}, timeout=60*60)

        # Combine cached and newly fetched data
        all_nearby = cached_nearby + uncached_nearby
        all_similar = cached_similar + uncached_similar

        return JsonResponse({
            "nearby_restaurants": all_nearby,
            "similar_restaurants": all_similar,
        })

    except Exception as e:
        return JsonResponse({"error": f"Unhandled exception: {str(e)}"}, status=500)
