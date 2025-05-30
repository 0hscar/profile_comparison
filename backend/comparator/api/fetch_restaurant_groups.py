print("fetch_restaurant_groups.py loaded")
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv
from comparator.utils.business_utils import (
    fetch_business_profiles_from_serper,
    fetch_business_search_from_serper,
    combine_all_info_for_place,
    get_places_cards,
)


@csrf_exempt
def fetch_restaurant_groups(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
        user_business_name = data.get("user_business_name")
        user_business_location = data.get("user_business_location")
        gl = data.get("gl", "us")
        num_places = int(data.get("num_places", 5))
        similar_query = data.get("similar_query", "restaurant")
        similar_location = data.get("similar_location", user_business_location)

        if not user_business_name or not user_business_location:
            return JsonResponse({"error": "user_business_name and user_business_location are required"}, status=400)

        # Fetch user business card
        user_cards = get_places_cards(user_business_name, user_business_location, gl=gl, num_places=1)
        if not user_cards:
            return JsonResponse({"error": "User restaurant not found with the given name and location."}, status=404)
        user_card = user_cards[0]
        user_address = user_card.get("address", user_business_location)

        # Fetch nearby restaurants (generic "restaurant" query)
        nearby_cards = get_places_cards("restaurant", user_address, gl=gl, num_places=num_places)
        # Remove user_card if present, then prepend user_card
        nearby_cards = [c for c in nearby_cards if not (
            user_card.get("title", "").lower() == c.get("title", "").lower() and
            user_card.get("address", "").lower() == c.get("address", "").lower()
        )]
        nearby_cards = [user_card] + nearby_cards

        # Fetch similar restaurants using the user's category as the query
        user_category = user_card.get("category") or "restaurant"
        similar_cards = get_places_cards(user_category, user_address, gl=gl, num_places=num_places)
        # Remove user_card if present, then prepend user_card
        similar_cards = [c for c in similar_cards if not (
            user_card.get("title", "").lower() == c.get("title", "").lower() and
            user_card.get("address", "").lower() == c.get("address", "").lower()
        )]
        similar_cards = [user_card] + similar_cards

        return JsonResponse({
            "user_business": user_card,
            "nearby_restaurants": nearby_cards,
            "similar_restaurants": similar_cards,
        })
    except Exception as e:
        return JsonResponse({"error": f"Invalid request: {str(e)}"}, status=400)
