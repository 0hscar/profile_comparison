from django.urls import path
from .views import get_competitors

urlpatterns = [
    path('competitors/', get_competitors, name='get_competitors'),
]
