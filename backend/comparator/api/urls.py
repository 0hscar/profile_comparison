from django.urls import path
from .views import (
    BusinessProfileView,
    AISuggestionsView,
    WhatIfView,
    stream_competitors,
    profile_assistant_stream,
    social_caption_stream,
)

urlpatterns = [
    path('business-profile/', BusinessProfileView.as_view(), name='business-profile'),
    path('competitors/', stream_competitors, name='stream-competitors'),
    path('ai-suggestions/', AISuggestionsView.as_view(), name='ai-suggestions'),
    path('simulate-what-if/', WhatIfView.as_view(), name='simulate-what-if'),
    path('profile-assistant/', profile_assistant_stream, name='profile-assistant'),
    path('social-caption/', social_caption_stream, name='social-caption'),
]
