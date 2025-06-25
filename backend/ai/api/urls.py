from django.urls import path
from .views import (
    profile_assistant_stream,
)

urlpatterns = [
    path('profile-assistant/', profile_assistant_stream, name='profile-assistant'),
]
