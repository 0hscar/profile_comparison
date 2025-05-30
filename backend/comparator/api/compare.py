print("compare.py loaded")
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv
from comparator.utils.business_utils import (
    get_places_cards,
)
from comparator.utils.ai_utils import sendToAI

@csrf_exempt
def compare_view(request):
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

        # Gather user and competitor data as before
        user_card = None
        user_cards = []
        if user_business_name and user_business_location:
            user_cards = get_places_cards(user_business_name, user_business_location, gl=gl, num_places=1)
        if not user_cards:
            return JsonResponse({"error": "User restaurant not found with the given name and location."}, status=404)
        user_card = user_cards[0]

        # Get competitors (excluding the user)
        competitor_cards = []
        if query and location:
            competitor_cards = get_places_cards(query=query, location=location, gl=gl, num_places=num_places)
            competitor_cards = [c for c in competitor_cards if not (
                user_card.get("title", "").lower() == c.get("title", "").lower() and
                user_card.get("address", "").lower() == c.get("address", "").lower()
            )]

        # Prepare prompt for OpenAI
        prompt = f"""
You are an expert business analyst. Here is the data for a user's restaurant and its competitors, as found from Google/Serper:

User Restaurant:
{json.dumps(user_card, indent=2)}

Competitors:
{json.dumps(competitor_cards, indent=2)}

Based on this data and your own knowledge, do the following:
- Fill in any missing details for the user restaurant if you can infer them.
- Create a detailed, structured profile for the user restaurant.
- Compare the user restaurant to its competitors.
- Suggest specific improvements for the user restaurant to stand out.
- If you know more about these businesses, add relevant details.
Return your answer as a structured JSON object with fields: 'user_profile', 'competitor_profiles', 'comparison', 'suggestions', and 'extra_insights'.
Respond ONLY with valid JSON.
"""

        # Use the new sendToAI function
        return sendToAI(prompt)

    except Exception as e:
        return JsonResponse({"error": f"Unhandled exception: {str(e)}"}, status=500)
