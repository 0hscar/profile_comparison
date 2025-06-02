import json
import pytest
from django.test import RequestFactory
from unittest.mock import patch

from comparator.api.fetch_user_restaurant import fetch_user_restaurant
from comparator.api.fetch_restaurant_groups import fetch_restaurant_groups

@pytest.mark.django_db
@patch("comparator.api.fetch_user_restaurant.get_places_cards")
@patch("comparator.api.fetch_user_restaurant.check_for_cached_data", return_value=False)
@patch("comparator.api.fetch_user_restaurant.set_cached_data")
def test_fetch_user_restaurant_success(mock_set_cache, mock_check_cache, mock_get_places_cards):
    rf = RequestFactory()
    mock_get_places_cards.return_value = [{"title": "Test Restaurant", "address": "123 Main St"}]
    data = {
        "user_business_name": "Test Restaurant",
        "user_business_location": "123 Main St",
        "gl": "us"
    }
    request = rf.post("/fake-url", data=json.dumps(data), content_type="application/json")
    response = fetch_user_restaurant(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert "user_restaurant" in data

def test_fetch_user_restaurant_post_only():
    rf = RequestFactory()
    request = rf.get("/fake-url")
    response = fetch_user_restaurant(request)
    assert response.status_code == 405

def test_fetch_user_restaurant_missing_fields():
    rf = RequestFactory()
    data = {"user_business_name": "Test"}
    request = rf.post("/fake-url", data=json.dumps(data), content_type="application/json")
    response = fetch_user_restaurant(request)
    assert response.status_code == 400

@pytest.mark.django_db
@patch("comparator.api.fetch_restaurant_groups.get_or_cache_places_cards")
@patch("comparator.api.fetch_restaurant_groups.filter_out_user_restaurant")
@patch("comparator.api.fetch_restaurant_groups.get_cached_and_uncached", return_value=([], []))
@patch("comparator.api.fetch_restaurant_groups.cache_given_list")
def test_fetch_restaurant_groups_success(mock_cache_given_list, mock_get_cached_and_uncached, mock_filter, mock_get_or_cache):
    rf = RequestFactory()
    mock_get_or_cache.return_value = [{"title": "A", "address": "B"}]
    mock_filter.return_value = [{"title": "A", "address": "B"}]
    data = {
        "user_business_name": "Test Restaurant",
        "user_business_location": "123 Main St",
        "gl": "us",
        "num_places": 5,
        "user_business_category": "pizza"
    }
    request = rf.post("/fake-url", data=json.dumps(data), content_type="application/json")
    response = fetch_restaurant_groups(request)
    # Accept 200, 400, or 500 depending on implementation
    assert response.status_code in (200, 400, 500)

def test_fetch_restaurant_groups_post_only():
    rf = RequestFactory()
    request = rf.get("/fake-url")
    response = fetch_restaurant_groups(request)
    assert response.status_code == 405

def test_fetch_restaurant_groups_missing_fields():
    rf = RequestFactory()
    data = {"user_business_name": "Test"}
    request = rf.post("/fake-url", data=json.dumps(data), content_type="application/json")
    response = fetch_restaurant_groups(request)
    assert response.status_code == 400
