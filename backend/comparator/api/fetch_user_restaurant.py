from comparator.utils.cache_utils import safe_cache_key, check_for_cached_data, set_cached_data
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.cache import cache
from comparator.utils.business_utils import get_places_cards

@csrf_exempt
def fetch_user_restaurant(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
        user_business_name = data.get("user_business_name")
        user_business_location = data.get("user_business_location")
        gl = data.get("gl", "fi")

        if not user_business_name or not user_business_location:
            return JsonResponse({"error": "user_business_name and user_business_location are required"}, status=400)

        # Check for cached user restaurant
        cache_key = safe_cache_key(f"user_restaurant:{user_business_name.lower().strip()}|{user_business_location.lower().strip()}")
        if (cached_response := check_for_cached_data(cache_key)) is not False: return JsonResponse(cached_response)

        user_cards = get_places_cards(user_business_name, user_business_location, gl=gl, num_places=1)
        if not user_cards:
            return JsonResponse({"error": "User restaurant not found with the given name and location."}, status=404)
        user_card = user_cards[0]
        # get_places_cards returns a list, Need the first one

        # Optionally, you can do some cleaning/formatting here if needed

        result = {"user_restaurant": user_card}
        set_cached_data(cache_key, result, timeout=60*60)  # cache for 1 hour
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": f"Unhandled exception: {str(e)}"}, status=500)
