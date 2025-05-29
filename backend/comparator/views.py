from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json
import os
import http.client
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
# For AI integration, we'll import a utility (to be implemented)
from .ai_utils import generate_comparison_suggestions as mock_ai
import openai


# Function to fetch business profiles from Serper.dev API
def fetch_business_profiles_from_serper(query, location, gl="us"):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "location": location,
        "gl": gl
    })
    headers = {
        'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/places", payload, headers)
    res = conn.getresponse()
    data = res.read()
    try:
        results = json.loads(data.decode("utf-8"))
        return results
    except Exception:
        return {}

def fetch_business_search_from_serper(query, location, gl="us"):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "location": location,
        "gl": gl,
        "type": "search"
    })
    headers = {
        'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    try:
        results = json.loads(data.decode("utf-8"))
        return results
    except Exception:
        return {}

def extract_profile_from_serper_result(place):
    # Return all fields from the place result as-is (dynamic extraction)
    return dict(place)

def extract_menu_from_search(search_data, business_title):
    # Look for menu in organic sitelinks, matching business title
    for organic in search_data.get("organic", []):
        if business_title.lower() in organic.get("title", "").lower():
            for sitelink in organic.get("sitelinks", []):
                title_lower = sitelink["title"].lower()
                link_lower = sitelink.get("link", "").lower()
                if "menu" in title_lower or "ruokalista" in title_lower:
                    return sitelink["link"]
                if "menu" in link_lower:
                    return f"Possibly this link: {sitelink['link']}"
    # Fallback: search all sitelinks if not matched by title
    for organic in search_data.get("organic", []):
        for sitelink in organic.get("sitelinks", []):
            title_lower = sitelink["title"].lower()
            link_lower = sitelink.get("link", "").lower()
            if "menu" in title_lower or "ruokalista" in title_lower: # If in finnish
                return sitelink["link"]
            if "menu" in link_lower:
                return f"Possibly this link: {sitelink['link']}"
    return None

def extract_hours_from_search(search_data, business_title):
    # Try to extract hours from knowledgeGraph if the title matches
    kg = search_data.get("knowledgeGraph", {})
    if kg and business_title.lower() in kg.get("title", "").lower():
        attributes = kg.get("attributes", {})
        for k, v in attributes.items():
            if "hour" in k.lower():
                return v
    return None

def is_same_business(place, search_kg):
    # Compare title and address for a basic match
    if not search_kg:
        return False
    title_match = place.get("title", "").lower() == search_kg.get("title", "").lower()
    address_match = False
    if "address" in place and "attributes" in search_kg:
        for k, v in search_kg["attributes"].items():
            if "address" in k.lower() and place["address"].lower() in v.lower():
                address_match = True
    return title_match or address_match

def compare_profiles(user_profile, competitor_profiles):
   # Dynamically calculate averages for all numeric fields present in competitor profiles
   if not competitor_profiles:
       return {}

   # Collect all keys from all competitor profiles
   all_keys = set()
   for p in competitor_profiles:
       all_keys.update(p.keys())

   # Only average numeric fields
   averages = {}
   for key in all_keys:
       values = [p[key] for p in competitor_profiles if key in p and isinstance(p[key], (int, float))]
       if values:
           averages[key] = sum(values) / len(values)

   # For boolean fields, show if any competitor has it True
   bool_fields = [k for k in all_keys if any(isinstance(p.get(k), bool) for p in competitor_profiles)]
   competitor_field_presence = {field: any(p.get(field, False) for p in competitor_profiles) for field in bool_fields}

   comparison = {
       "user": user_profile,
       "competitors": competitor_profiles,
       "averages": averages,
       "competitor_field_presence": competitor_field_presence,
   }
   return comparison


SVENSKA_TEATERN_LOCATION = "Mikonkatu 2, 00100 Helsinki, Finland" # Mock data, location for users restaurant

def combine_all_info_for_place(place, search_data):
    """
    Combine all available info from /places and /search for a single place.
    """
    combined = extract_profile_from_serper_result(place)
    kg = search_data.get("knowledgeGraph", {})
    # Merge all fields from knowledgeGraph if same business
    if is_same_business(place, kg):
        for k, v in kg.items():
            if k not in combined:
                combined[k] = v
    # Find matching organic result and merge all its fields
    for organic in search_data.get("organic", []):
        if place.get("title", "").lower() in organic.get("title", "").lower():
            for k, v in organic.items():
                if k not in combined and k != "sitelinks":
                    combined[k] = v
            # Also scan sitelinks for menu and include all sitelinks
            menu_url = None
            possible_menu_url = None
            for sitelink in organic.get("sitelinks", []):
                title_lower = sitelink["title"].lower()
                link_lower = sitelink.get("link", "").lower()
                if "menu" in title_lower or "ruokalista" in title_lower:
                    menu_url = sitelink["link"]
                    break
                if "menu" in link_lower:
                    possible_menu_url = f"Possibly this link: {sitelink['link']}"
            if menu_url:
                combined["menu"] = menu_url
            elif possible_menu_url:
                combined["menu"] = possible_menu_url
            else:
                combined["menu"] = "Menu not found"
            combined["sitelinks"] = organic.get("sitelinks", [])
            break
    # If menu not found in organic, fallback to scanning all sitelinks
    if "menu" not in combined:
        menu_url = extract_menu_from_search(search_data, place.get("title", ""))
        combined["menu"] = menu_url if menu_url else "Menu not found"
    # Add hours if present in knowledgeGraph attributes
    hours = extract_hours_from_search(search_data, place.get("title", ""))
    combined["hours"] = hours if hours else "Opening hours not found"
    # Always include description if not already present
    if "description" not in combined:
        snippet = None
        for organic in search_data.get("organic", []):
            if place.get("title", "").lower() in organic.get("title", "").lower():
                snippet = organic.get("snippet")
                break
        combined["description"] = snippet if snippet else "Description not found"
    return combined

def get_places_and_cards(query=None, location=None, gl="us", num_places=5):
    """
    If query is None, use default mock location (Svenska Teatern) and fetch nearby restaurants.
    Otherwise, use the query and location provided.
    Returns a list of cards (dicts) for each place.
    """
    if not location:
        location = SVENSKA_TEATERN_LOCATION
    if not query:
        # Default: fetch nearby restaurants (e.g., "restaurant" or "ravintola")
        query = "restaurant"
    serper_places = fetch_business_profiles_from_serper(query, location, gl)
    places = serper_places.get("places", [])[:num_places]
    serper_search = fetch_business_search_from_serper(query, location, gl)
    cards = []
    for place in places:
        card = combine_all_info_for_place(place, serper_search)
        cards.append(card)
    return cards

def get_comparison_and_suggestions(cards):
    """
    Use the first card as the user's business, the rest as competitors.
    Returns comparison and AI suggestions.
    """
    if not cards:
        return {}, {}
    user_profile = cards[0]
    competitor_profiles = cards[1:]
    comparison = compare_profiles(user_profile, competitor_profiles)
    suggestions = generate_comparison_suggestions(comparison, competitor_profiles)
    return comparison, suggestions

def generate_comparison_suggestions(comparison, competitors_profiles):
    """
    Use OpenAI to generate a summary and concrete suggestions.
    Returns a dict with the summary/suggestions and a visible note about which AI was used.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        # fallback to mock if no key
        from .ai_utils import generate_comparison_suggestions as mock_ai
        result = mock_ai(comparison, competitors_profiles)
        result["ai_provider"] = "mock"
        result["ai_note"] = "Using mock AI (not OpenAI)."
        return result
    client = openai.OpenAI(api_key=openai_api_key)
    prompt = (
        "Given the following business profile comparison, generate a summary and concrete suggestions for improvement. "
        "Be specific and actionable. Here is the data:\n\n"
        f"{json.dumps(comparison, indent=2)}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful business profile consultant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=350,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return {
            "ai_summary": content,
            "ai_provider": "openai",
            "ai_note": "Using OpenAI for summary and suggestions."
        }
    except Exception as e:
        return {
            "ai_summary": f"AI suggestion unavailable: {str(e)}",
            "ai_provider": "error",
            "ai_note": "OpenAI call failed, see ai_summary for error."
        }

@csrf_exempt
def compare_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        mode = data.get("mode", "default")  # "default" or "search"
        gl = data.get("gl", "us")
        num_places = int(data.get("num_places", 5))
        if mode == "search":
            query = data.get("query")
            location = data.get("location")
            if not query or not location:
                return JsonResponse({"error": "Missing query or location"}, status=400)
            cards = get_places_and_cards(query=query, location=location, gl=gl, num_places=num_places)
        else:
            # Default: show 2-5 restaurants near Svenska Teatern
            cards = get_places_and_cards(query=None, location=None, gl=gl, num_places=num_places)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not cards:
        return JsonResponse({"error": "No results found"}, status=404)

    comparison, suggestions = get_comparison_and_suggestions(cards)

    return JsonResponse({
        "cards": cards,
        "comparison": comparison,
        "suggestions": suggestions,
    })

# For Django URL routing
from django.urls import path

urlpatterns = [
    path('compare/', compare_view, name='compare'),
]
