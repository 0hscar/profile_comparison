from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.http import StreamingHttpResponse
from comparator.utils.business_profile_ai_utils import (
    BusinessProfile, generate_ai_suggestions, simulate_what_if,
    profile_assistant_response, generate_social_caption
)
from typing import Any, Dict

# Example: Replace with real DB or external API in production
FAKE_PROFILE = {
    "name": "Nordic Bistro",
    "address": "Mannerheimintie 1, 00100 Helsinki",
    "rating": 4.6,
    "review_count": 542,
    "price_level": "€€",
    "category": "Modern European Restaurant",
    "description": "A modern bistro in the heart of Helsinki.",
    "hours": ["Mon-Fri 11:00–22:00", "Sat 12:00–00:00", "Sun 12:00–21:00"],
    "menu_url": "https://www.nordicbistro.fi/menu/",
    "website": "https://www.nordicbistro.fi/",
    "photos": [],
}

class BusinessProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response(FAKE_PROFILE)

class AISuggestionsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        profile = BusinessProfile(**FAKE_PROFILE)
        competitors = [BusinessProfile(**FAKE_PROFILE)]  # Replace with real competitors
        suggestions = generate_ai_suggestions(profile, competitors)
        return Response(suggestions.dict())

class WhatIfView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        profile = BusinessProfile(**FAKE_PROFILE)
        changes = request.data.get("changes", {})
        result = simulate_what_if(profile, changes)
        return Response(result.dict())

@api_view(['POST'])
@permission_classes([AllowAny])
def profile_assistant_stream(request):
    question = request.data.get("question", "")
    profile = BusinessProfile(**FAKE_PROFILE)
    def stream():
        for chunk in profile_assistant_response(question, profile):
            yield chunk
    return StreamingHttpResponse(stream(), content_type="text/plain")

@api_view(['POST'])
@permission_classes([AllowAny])
def social_caption_stream(request):
    prompt = request.data.get("prompt", "")
    profile = BusinessProfile(**FAKE_PROFILE)
    def stream():
        for chunk in generate_social_caption(prompt, profile):
            yield chunk
    return StreamingHttpResponse(stream(), content_type="text/plain")
