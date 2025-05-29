from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json
import os
import http.client
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
# For AI integration, we'll import a utility (to be implemented)
from .ai_utils import generate_comparison_suggestions

# Function to fetch business profiles from Serper.dev API
def fetch_business_profiles_from_serper(query, location, gl="us"):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "location": location,
        "gl": gl
    })
    headers = {
        'X-API-KEY': os.environ.get('SERPER_API_KEY', ''), # Replace with your own serper API key in .env file
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

def extract_profile_from_serper_result(place):
    # Return all fields from the place result as-is (dynamic extraction)
    return dict(place)

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

@csrf_exempt
def compare_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        query = data.get("query")  # e.g., "thai food"
        location = data.get("location")  # e.g., "Finland"
        gl = data.get("gl", "us")
        if not query or not location:
            return JsonResponse({"error": "Missing query or location"}, status=400)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Fetch places from Serper.dev
    serper_results = fetch_business_profiles_from_serper(query, location, gl)
    places = serper_results.get("places", [])

    if not places:
        return JsonResponse({"error": "No results found"}, status=404)

    # Assume the first result is the user's business, others are competitors
    user_profile = extract_profile_from_serper_result(places[0])
    competitor_profiles = [extract_profile_from_serper_result(p) for p in places[1:]]

    comparison = compare_profiles(user_profile, competitor_profiles)
    suggestions = generate_comparison_suggestions(comparison, competitor_profiles)

    return JsonResponse({
        "comparison": comparison,
        "suggestions": suggestions,
    })

# For Django URL routing
from django.urls import path

urlpatterns = [
    path('compare/', compare_view, name='compare'),
]
