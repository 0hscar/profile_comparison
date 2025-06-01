from comparator.utils.cache_utils import safe_cache_key, get_cached_and_uncached, cache_given_list, get_or_cache_places_cards
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.cache import cache
from comparator.utils.business_utils import get_places_cards, filter_out_user_restaurant

@csrf_exempt
def fetch_restaurant_groups(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
        user_business_name = data.get("user_business_name")
        user_business_location = data.get("user_business_location")
        gl = data.get("gl")
        num_places = int(data.get("num_places"))
        user_category = data.get("user_business_category")

        if not user_business_name or not user_business_location:
            return JsonResponse({"error": "user_business_name and user_business_location are required"}, status=400)

        # Check for cached user restaurant, if none found, fetch it from Google/Serper
        nearby_cards = get_or_cache_places_cards("restaurant", user_business_location, gl=gl, num_places=num_places, fullInfo=False)
        similar_cards = get_or_cache_places_cards(user_category, user_business_location, gl=gl, num_places=num_places, fullInfo=False)

        # Filter out the user's own restaurant from both lists, has been slipping through in some cases
        nearby_cards = filter_out_user_restaurant(nearby_cards, user_business_name, user_business_location)
        similar_cards = filter_out_user_restaurant(similar_cards, user_business_name, user_business_location)

        key_func = lambda r: safe_cache_key(
            f"user_restaurant:{r.get('title','').lower().strip()}|{r.get('address','').lower().strip()}"
        )
        # Caching logic for each restaurant
        cached_nearby, uncached_nearby = get_cached_and_uncached(nearby_cards, key_func)
        cached_similar, uncached_similar = get_cached_and_uncached(similar_cards, key_func)

        # Cache new results individually
        cache_given_list(uncached_nearby, key_func, timeout=60*60)
        cache_given_list(uncached_similar, key_func, timeout=60*60)


        # Combine cached and newly fetched data
        all_nearby = cached_nearby + uncached_nearby
        all_similar = cached_similar + uncached_similar

        return JsonResponse({
            "nearby_restaurants": all_nearby,
            "similar_restaurants": all_similar,
        })

    except Exception as e:
        return JsonResponse({"error": "Unhandled exception"}, status=500)
