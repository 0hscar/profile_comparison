from pydantic import Json
from comparator.utils.cache_utils import check_for_cached_data, get_or_cache_places_cards, safe_cache_key
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache
import json
from comparator.utils.business_utils import filter_out_user_restaurant, get_places_cards
from comparator.utils.ai_utils import build_query_for_prompt, sendToAI

@csrf_exempt
def compare_view(request: Json) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        query = data.get("query")
        location = data.get("location")
        if not query and location:
            return JsonResponse({"error": "'query' or 'location' must be provided."}, status=400)

        num_places = int(data.get("num_places"))
        user_business_name = data.get("user_business_name")
        user_business_location = data.get("user_business_location")
        gl = data.get("gl")

        # Try to use cached user restaurant, if none found, fetch it from Google/Serper
        cache_key_user = safe_cache_key(f"user_restaurant:{user_business_name.lower().strip()}|{user_business_location.lower().strip()}")
        cached_user = cache.get(cache_key_user)
        user_query = ""
        if (cached_response := check_for_cached_data(cache_key_user)) is not False:
            user_card = cached_response["user_restaurant"]
            user_query = build_query_for_prompt("User Restaurant", [user_card])

        else:
            user_cards = []
            if user_business_name and user_business_location:
                user_cards = get_or_cache_places_cards(user_business_name, user_business_location, num_places ,gl=gl )
            if not user_cards:
                return JsonResponse({"error": "User restaurant not found with the given name and location."}, status=404)
            user_card = user_cards[0]

        # Get competitors (excluding the user)
        competitor_cards = get_or_cache_places_cards(query=query, location=location, gl=gl, num_places=num_places, fullInfo=False)
        # Build competitor_query string
        competitor_query = build_query_for_prompt("Competitor Restaurants", competitor_cards)
        # Cache key for the AI response (include num_places for uniqueness)
        cache_key_ai = safe_cache_key(f"compare:{user_card.get('title','').lower().strip()}|{query.lower().strip() if query else ''}|{num_places}")

        cached_ai = cache.get(cache_key_ai)
        if cached_ai:
            print(f"Returning cached AI comparison for key: {cache_key_ai}")
            return JsonResponse(cached_ai)

        ai_response = sendToAI(user_query, competitor_query)
        if ai_response:
            ai_response_dict = ai_response.model_dump()
            cache.set(cache_key_ai, ai_response_dict, timeout=60*60)
            return JsonResponse(ai_response_dict)
        else:
            return JsonResponse({"error": "AI response is empty or invalid."}, status=500)

    except Exception as e:
        print("compare endpoint failed with: ", e)
        return JsonResponse({"error": "Unhandled exception:"}, status=500)
