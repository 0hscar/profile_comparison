from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ai/', include('ai.api.urls')),
    path('api/profiles/', include('profiles.api.urls')),
    path('api/competitors/', include('competitors.api.urls')),
    # path('api/alerts/', include('alerts.api.urls')),  # Uncomment when alerts app is ready
]
