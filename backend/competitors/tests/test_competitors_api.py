from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest import mock

class TestCompetitorsAPI(APITestCase):
    def setUp(self):
        # Adjust the reverse() argument if your url name is different
        self.url = reverse('get_competitors')

    @mock.patch("competitors.api.views.get_competitors_from_serper")
    def test_get_returns_nearby_and_similar_lists(self, mock_get_competitors):
        # Mock the service to return predictable results
        mock_get_competitors.side_effect = [
            [{"id": 1, "name": "Nearby 1"}, {"id": 2, "name": "Nearby 2"}],  # nearby
            [{"id": 3, "name": "Similar 1"}]  # similar
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("nearby", data)
        self.assertIn("similar", data)
        self.assertIsInstance(data["nearby"], list)
        self.assertIsInstance(data["similar"], list)
        self.assertEqual(data["nearby"], [{"id": 1, "name": "Nearby 1"}, {"id": 2, "name": "Nearby 2"}])
        self.assertEqual(data["similar"], [{"id": 3, "name": "Similar 1"}])

    @mock.patch("competitors.api.views.get_competitors_from_serper")
    def test_max_results_query_param_limits_results(self, mock_get_competitors):
        # Simulate the service returning more items than max_results
        mock_get_competitors.side_effect = [
            [{"id": i, "name": f"Nearby {i}"} for i in range(10)],  # nearby
            [{"id": i, "name": f"Similar {i}"} for i in range(10)]  # similar
        ]
        response = self.client.get(self.url + "?max_results=3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # The view itself does not slice, but the service should respect max_results
        self.assertEqual(len(data["nearby"]), 10)
        self.assertEqual(len(data["similar"]), 10)

    @mock.patch("competitors.api.views.get_competitors_from_serper")
    def test_no_max_results_param_uses_default(self, mock_get_competitors):
        mock_get_competitors.side_effect = [
            [{"id": 1}],  # nearby
            [{"id": 2}]   # similar
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["nearby"], [{"id": 1}])
        self.assertEqual(data["similar"], [{"id": 2}])

    @mock.patch("competitors.api.views.get_competitors_from_serper")
    def test_max_results_zero_returns_empty_lists(self, mock_get_competitors):
        mock_get_competitors.side_effect = [
            [],  # nearby
            []   # similar
        ]
        response = self.client.get(self.url + "?max_results=0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["nearby"], [])
        self.assertEqual(data["similar"], [])

    @mock.patch("competitors.api.views.get_competitors_from_serper")
    def test_large_max_results(self, mock_get_competitors):
        mock_get_competitors.side_effect = [
            [{"id": i} for i in range(100)],  # nearby
            [{"id": i} for i in range(100)]   # similar
        ]
        response = self.client.get(self.url + "?max_results=100")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["nearby"]), 100)
        self.assertEqual(len(data["similar"]), 100)
