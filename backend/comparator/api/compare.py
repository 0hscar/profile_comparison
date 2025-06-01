from comparator.utils.cache_utils import check_for_cached_data, get_or_cache_places_cards, safe_cache_key
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache
import json
from comparator.utils.business_utils import get_places_cards
from comparator.utils.ai_utils import sendToAI, extract_json_from_response

@csrf_exempt
def compare_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        num_places = int(data.get("num_places", 5))
        user_business_name = data.get("user_business_name")
        user_business_location = data.get("user_business_location")
        gl = data.get("gl", "fi")
        query = data.get("query")
        location = data.get("location")

        # Try to use cached user restaurant, if none found, fetch it from Google/Serper
        cache_key_user = safe_cache_key(f"user_restaurant:{user_business_name.lower().strip()}|{user_business_location.lower().strip()}")
        cached_user = cache.get(cache_key_user)
        user_query = ""
        if (cached_response := check_for_cached_data(cache_key_user)) is not False:
            user_card = cached_response["user_restaurant"]
            user_title = user_card.get("title", "Unknown Title")
            user_address = user_card.get("address", "Unknown Address")
            user_query = f"User Restaurant:\n  Title: {user_title}\n  Address: {user_address}"
            print(user_query)

        # if cached_user and "user_restaurant" in cached_user:
        #     print("Using cached user restaurant profile in compare_view.")
        #     user_card = cached_user["user_restaurant"]
        #     print(user_card)
        else:
            user_cards = []
            if user_business_name and user_business_location:
                user_cards = get_or_cache_places_cards(user_business_name, user_business_location, gl=gl, num_places=1)
            if not user_cards:
                return JsonResponse({"error": "User restaurant not found with the given name and location."}, status=404)
            user_card = user_cards[0]



        # Get competitors (excluding the user)
        competitor_query = ""
        competitor_cards = [] # Might not be used
        if query and location:
            competitor_cards = get_or_cache_places_cards(query=query, location=location, gl=gl, num_places=num_places, fullInfo=False)
            # Build competitor_query string
            competitor_query = "Competitors:\n"
            for idx, c in enumerate(competitor_cards, 1):
                c_title = c.get("title", "Unknown Title")
                c_address = c.get("address", "Unknown Address")
                competitor_query += f"  {idx}. Title: {c_title}\n     Address: {c_address}\n"
            print(competitor_query)

        # Prepare prompt for OpenAI
        prompt = f"""
You are an expert business analyst. Here is the data for a user's restaurant and its competitors, as found from Google/Serper:

User Restaurant:
{user_query}
Competitors:
{competitor_query}

Based on these names and addresses and your own knowledge, (use the web if you can) do the following:
- Fill in any missing details for the user restaurant if you can infer them.
- Create a detailed, structured profile for the user restaurant, in regards to price, try to keep it as a price range in euros.
- Compare the user restaurant to its competitors, important fields:
    1 Point out Review counts and ratings, including averages for the competitors.
    2 Number of photos, if available.
    3 Presence of critical fiels like menu, hours, description (If there are menu links, point them out)
    4 Extra fields you deem important.
- Suggest specific improvements for the user restaurant to stand out.
- If you know more about these businesses, add relevant details.
Return your answer as a structured JSON object with fields: 'user_profile', 'competitor_profiles', 'comparison', 'suggestions', and 'extra_insights'.
Respond ONLY with valid JSON.
"""

        # Cache key for the AI response (include num_places for uniqueness)
        cache_key_ai = safe_cache_key(f"compare:{user_card.get('title','').lower().strip()}|{query.lower().strip() if query else ''}|{num_places}")

        cached_ai = cache.get(cache_key_ai)
        if cached_ai:
            print(f"Returning cached AI comparison for key: {cache_key_ai}")
            return JsonResponse(cached_ai)

        ai_response = sendToAI(prompt)
        if ai_response.status_code == 200:
            try:
                ai_data = extract_json_from_response(ai_response.content.decode())
                cache.set(cache_key_ai, ai_data, timeout=60*60)
                return JsonResponse(ai_data)
            except Exception as e:
                print("Failed to cache or parse AI response:", e)
                return ai_response
        return ai_response

    except Exception as e:
        return JsonResponse({"error": f"Unhandled exception: {str(e)}"}, status=500)
