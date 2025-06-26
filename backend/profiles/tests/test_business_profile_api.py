from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from profiles.mockdata.fake_profile import FAKE_PROFILE

class BusinessProfileAPITests(APITestCase):
    def setUp(self):
        # Adjust the reverse() argument if your url name is different
        self.url = reverse('business-profile')

    def test_get_returns_fake_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), FAKE_PROFILE)
