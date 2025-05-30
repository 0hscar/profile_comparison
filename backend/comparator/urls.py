print("urls.py loaded")
from django.urls import path
from comparator.api.compare import compare_view
from comparator.api.fetch_user_restaurant import fetch_user_restaurant
from comparator.api.fetch_restaurant_groups import fetch_restaurant_groups
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_view(request):
    return JsonResponse({"message": "Test view is working!"})

urlpatterns = [
    path('compare/', compare_view, name='compare_view'),
    path('fetch_restaurant_groups/', fetch_restaurant_groups, name='fetch_restaurant_groups'),
    path('fetch_user_restaurant/', fetch_user_restaurant, name='fetch_user_restaurant'),
    path('test/', test_view, name='test_view'),
]
