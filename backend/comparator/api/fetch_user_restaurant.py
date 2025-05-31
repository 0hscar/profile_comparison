from comparator.utils.cache_utils import safe_cache_key
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.cache import cache
from comparator.utils.business_utils import get_places_cards
from comparator.utils.ai_utils import sendToAI

@csrf_exempt
def fetch_user_restaurant(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
        user_business_name = data.get("user_business_name")
        user_business_location = data.get("user_business_location")
        gl = data.get("gl", "us")

        if not user_business_name or not user_business_location:
            return JsonResponse({"error": "user_business_name and user_business_location are required"}, status=400)

        cache_key = safe_cache_key(f"user_restaurant:{user_business_name.lower().strip()}|{user_business_location.lower().strip()}")
        cached = cache.get(cache_key)
        if cached:
            print("Returning cached user restaurant AI result (Django cache).")
            return JsonResponse(cached)

        user_cards = get_places_cards(user_business_name, user_business_location, gl=gl, num_places=1)
        if not user_cards:
            return JsonResponse({"error": "User restaurant not found with the given name and location."}, status=404)
        user_card = user_cards[0]

        prompt = f"""
You are an expert business analyst. Here is the data for a user's restaurant as found from Google/Serper:

User Restaurant:
{json.dumps(user_card, indent=2)}

Based on this data and your own knowledge, do the following:
- Clean up the data if needed and fill in details for said data if you can infer them.
- Return a structured JSON object with a single field: 'user_restaurant', which is a dictionary of the cleaned and filled-in restaurant profile.
Respond ONLY with valid JSON.
"""

        ai_response = sendToAI(prompt)
        # Only cache if successful
        if ai_response.status_code == 200:
            try:
                cached_data = json.loads(ai_response.content)
                cache.set(cache_key, cached_data, timeout=60*60)  # cache for 1 hour
            except Exception as e:
                print("Failed to cache AI response:", e)
        return ai_response

    except Exception as e:
        return JsonResponse({"error": f"Unhandled exception: {str(e)}"}, status=500)
