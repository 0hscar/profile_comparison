import io
import time
from unittest import mock

from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status

# Patch the generator to control streaming output
def fake_profile_assistant_response(question, profile, model="gpt-4.1-mini"):
    # Simulate streaming chunks
    yield "chunk1"
    time.sleep(0.1)
    yield "chunk2"
    time.sleep(0.1)
    yield "chunk3"

@override_settings(ROOT_URLCONF="ai.api.urls")
class ProfileAssistantStreamTests(APITestCase):
    def setUp(self):
        self.url = reverse("profile-assistant")
        self.default_data = {"question": "What is AI?", "model": "gpt-4.1-mini"}

    @mock.patch("ai.api.views.profile_assistant_response", side_effect=fake_profile_assistant_response)
    def test_valid_post_streams_chunks(self, mock_response):
        response = self.client.post(self.url, {"question": "What is AI?"}, format="json", stream=True)
        # Django's test client doesn't support true streaming, so we read the content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/event-stream")
        content = b"".join(response.streaming_content).decode()
        self.assertIn("chunk1", content)
        self.assertIn("chunk2", content)
        self.assertIn("chunk3", content)
        # Heartbeats (spaces) should be present
        self.assertIn(" ", content)

    @mock.patch("ai.api.views.profile_assistant_response", side_effect=fake_profile_assistant_response)
    def test_missing_question_and_model_uses_defaults(self, mock_response):
        response = self.client.post(self.url, {}, format="json", stream=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing 'question'", response.json().get("error", ""))

    @mock.patch("ai.api.views.profile_assistant_response", side_effect=fake_profile_assistant_response)
    def test_empty_question(self, mock_response):
        response = self.client.post(self.url, {"question": ""}, format="json", stream=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing 'question'", response.json().get("error", ""))

    @mock.patch("ai.api.views.profile_assistant_response", side_effect=fake_profile_assistant_response)
    def test_unsupported_model(self, mock_response):
        # The view does not validate model, so it should still stream
        response = self.client.post(self.url, {"question": "Test", "model": "unknown-model"}, format="json", stream=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = b"".join(response.streaming_content).decode()
        self.assertIn("chunk1", content)

    @mock.patch("ai.api.views.profile_assistant_response", side_effect=Exception("AI error"))
    def test_error_in_profile_assistant_response(self, mock_response):
        response = self.client.post(self.url, self.default_data, format="json", stream=True)
        self.assertEqual(response.status_code, 200)
        content = b"".join(response.streaming_content).decode()
        self.assertIn("Issue with AI response", content)
