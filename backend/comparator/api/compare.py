print("compare.py loaded")
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv
from comparator.utils.business_utils import (
    get_places_cards,
)
from comparator.utils.ai_utils import generate_comparison_suggestions, compare_profiles

@csrf_exempt
def compare_view(request):
    # print("I got here")
    try:
        # print("compare_view called")
        if request.method != "POST":
            return JsonResponse({"error": "POST only"}, status=405)

        try:
            data = json.loads(request.body)
            num_places = int(data.get("num_places", 5))
            user_business_name = data.get("user_business_name")
            user_business_location = data.get("user_business_location")
            gl = data.get("gl", "us")
            query = data.get("query")
            location = data.get("location")

            nearby_restaurants = []
            search_results = []
            # print("First try:")
            user_card = None
            if user_business_name and user_business_location:
                user_cards = get_places_cards(user_business_name, user_business_location, gl=gl, num_places=1)
                # print("if userbusiness_name and user_business_location", user_cards) user_cards emtpy -> 404 error...
                if user_cards:
                    user_card = user_cards[0]
                    user_address = user_card.get("address", None)
                    # print("if usercards")
                    if user_address:
                        nearby_restaurants = get_places_cards("restaurant", user_address, gl=gl, num_places=num_places)
                        nearby_restaurants = [c for c in nearby_restaurants if not (
                            user_card.get("title", "").lower() == c.get("title", "").lower() and
                            user_card.get("address", "").lower() == c.get("address", "").lower()
                        )]
                        nearby_restaurants = [user_card] + nearby_restaurants
                    if query and location:
                        search_results = get_places_cards(query=query, location=location, gl=gl, num_places=num_places)
                        search_results = [c for c in search_results if not (
                            user_card.get("title", "").lower() == c.get("title", "").lower() and
                            user_card.get("address", "").lower() == c.get("address", "").lower()
                        )]
                        search_results = [user_card] + search_results
                    else:
                        search_results = [user_card]
                else:
                    return JsonResponse({"error": "User restaurant not found with the given name and location."}, status=404)
            else:
                return JsonResponse({"error": "User restaurant (name and location) must be specified."}, status=400)

        except Exception as e:
            print("Inner exception:", e)
            return JsonResponse({"error": f"Invalid JSON or logic error: {str(e)}"}, status=400)

        if not search_results:
            return JsonResponse({"error": "No results found"}, status=404)

        user_profile = search_results[0]
        competitor_profiles = search_results[1:]
        comparison = compare_profiles(user_profile, competitor_profiles)
        suggestions = generate_comparison_suggestions(comparison, competitor_profiles)

        return JsonResponse({
            "nearby_restaurants": nearby_restaurants,
            "search_results": search_results,
            "comparison": comparison,
            "suggestions": suggestions,
        })
    except Exception as e:
        print("Outer exception:", e)
        return JsonResponse({"error": f"Unhandled exception: {str(e)}"}, status=500)
