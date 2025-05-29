from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json

# For AI integration, we'll import a utility (to be implemented)
from .ai_utils import generate_comparison_suggestions

# Mocked function to fetch business profile data
def fetch_business_profile(business_name_or_url):
    # In a real implementation, fetch from Google, Yelp, etc.
    # Here we return mocked data for demonstration.
    profiles = {
        "My Restaurant": {
            "name": "My Restaurant",
            "review_count": 12,
            "average_rating": 4.1,
            "num_images": 3,
            "has_hours": True,
            "has_description": True,
            "has_menu_link": False,
            "recent_reviews_unanswered": 2,
        },
        "Competitor A": {
            "name": "Competitor A",
            "review_count": 34,
            "average_rating": 4.5,
            "num_images": 18,
            "has_hours": True,
            "has_description": True,
            "has_menu_link": True,
            "recent_reviews_unanswered": 0,
        },
        "Competitor B": {
            "name": "Competitor B",
            "review_count": 28,
            "average_rating": 4.3,
            "num_images": 22,
            "has_hours": True,
            "has_description": False,
            "has_menu_link": True,
            "recent_reviews_unanswered": 1,
        },
    }
    return profiles.get(business_name_or_url, {
        "name": business_name_or_url,
        "review_count": 0,
        "average_rating": 0.0,
        "num_images": 0,
        "has_hours": False,
        "has_description": False,
        "has_menu_link": False,
        "recent_reviews_unanswered": 0,
    })

def compare_profiles(user_profile, competitor_profiles):
    # Calculate averages and identify missing fields
    if not competitor_profiles:
        return {}

    avg_review_count = sum(p["review_count"] for p in competitor_profiles) / len(competitor_profiles)
    avg_rating = sum(p["average_rating"] for p in competitor_profiles) / len(competitor_profiles)
    avg_images = sum(p["num_images"] for p in competitor_profiles) / len(competitor_profiles)
    avg_unanswered = sum(p["recent_reviews_unanswered"] for p in competitor_profiles) / len(competitor_profiles)

    fields = ["has_hours", "has_description", "has_menu_link"]
    competitor_field_presence = {field: any(p[field] for p in competitor_profiles) for field in fields}

    comparison = {
        "user": user_profile,
        "competitors": competitor_profiles,
        "averages": {
            "review_count": avg_review_count,
            "average_rating": avg_rating,
            "num_images": avg_images,
            "recent_reviews_unanswered": avg_unanswered,
        },
        "competitor_field_presence": competitor_field_presence,
    }
    return comparison

@csrf_exempt
def compare_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        business = data.get("business")
        competitors = data.get("competitors", [])
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user_profile = fetch_business_profile(business)
    competitor_profiles = [fetch_business_profile(name) for name in competitors]

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
