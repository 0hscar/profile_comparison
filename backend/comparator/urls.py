from django.urls import path, include
import comparator.api.urls

urlpatterns = [
    path('api/', include(comparator.api.urls.urlpatterns)),
]
