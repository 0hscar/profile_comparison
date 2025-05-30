from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.cache import cache
from comparator.utils.business_utils import get_places_cards, filter_out_user_restaurant
from comparator.utils.ai_utils import sendToAI, extract_json_from_response

def get_cached_and_uncached(restaurants):
    cached = []
    uncached = []
    for r in restaurants:
        cache_key = f"user_restaurant:{r.get('title','').lower().strip()}|{r.get('address','').lower().strip()}"
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


        # Mock cordinates for the user restaurant.
        # In a real application, you would fetch these from a reliable source or use geocoding.
        user_latlong = "60.1699,24.9444"

        if not user_business_name or not user_business_location:
            return JsonResponse({"error": "user_business_name and user_business_location are required"}, status=400)

        # Fetch nearby restaurants (generic "restaurant" query)
        nearby_cards = get_places_cards("restaurant", user_latlong, gl=gl, num_places=num_places)
        # Remove the user restaurant if present

        nearby_cards = filter_out_user_restaurant(nearby_cards, user_business_name, user_business_location)


        # Fetch similar restaurants (using the user's category)
        similar_cards = get_places_cards(user_category, user_business_location, gl=gl, num_places=num_places)

        similar_cards = filter_out_user_restaurant(similar_cards, user_business_name, user_business_location)
        # Caching logic for each restaurant
        cached_nearby, uncached_nearby = get_cached_and_uncached(nearby_cards)
        cached_similar, uncached_similar = get_cached_and_uncached(similar_cards)

        if (cached_nearby or cached_similar) and (uncached_nearby or uncached_similar):
            print("Using some cached restaurant profiles for fetch_restaurant_groups.")
        elif (cached_nearby or cached_similar):
            print("All restaurants are cached for fetch_restaurant_groups.")
        else:
            print("No cached restaurant profiles used for fetch_restaurant_groups.")

        # If all are cached, return immediately
        if len(cached_nearby) == len(nearby_cards) and len(cached_similar) == len(similar_cards):
            return JsonResponse({
                "nearby_restaurants": cached_nearby,
                "similar_restaurants": cached_similar,
            })

        # Otherwise, build prompt for AI
        prompt = f"""
You are an expert business analyst. Here is the data for a user's restaurant group.

For these restaurants, use the already processed data as-is:
Nearby Restaurants (cached):
{json.dumps(cached_nearby, indent=2)}

Similar Restaurants (cached):
{json.dumps(cached_similar, indent=2)}

For these restaurants, process and clean up the data:
- Fill in any missing details for the user restaurant if you can infer them.
Nearby Restaurants (uncached):
{json.dumps(uncached_nearby, indent=2)}

Similar Restaurants (uncached):
{json.dumps(uncached_similar, indent=2)}

Return a JSON object with 'nearby_restaurants' and 'similar_restaurants', using the provided data for cached ones and your own processing for the uncached ones.
Respond ONLY with valid JSON.
"""

        ai_response = sendToAI(prompt)
        if ai_response.status_code == 200:
            try:
                ai_data = extract_json_from_response(ai_response.content.decode())
                # Cache new results individually
                for r in ai_data.get("nearby_restaurants", []):
                    cache_key = f"user_restaurant:{r.get('title','').lower().strip()}|{r.get('address','').lower().strip()}"
                    cache.set(cache_key, {"user_restaurant": r}, timeout=60*60)
                for r in ai_data.get("similar_restaurants", []):
                    cache_key = f"user_restaurant:{r.get('title','').lower().strip()}|{r.get('address','').lower().strip()}"
                    cache.set(cache_key, {"user_restaurant": r}, timeout=60*60)
                return JsonResponse(ai_data)
            except Exception as e:
                print("Failed to cache AI response:", e)
                return ai_response
        return ai_response

    except Exception as e:
        return JsonResponse({"error": f"Unhandled exception: {str(e)}"}, status=500)
