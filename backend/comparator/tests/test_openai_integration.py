import os
import pytest
from unittest.mock import patch, MagicMock

from comparator.utils.ai_utils import generate_comparison_suggestions

@pytest.fixture
def comparison_data():
    return {
        "user": {
            "title": "Test Restaurant",
            "review_count": 10,
            "average_rating": 4.0,
            "photo_count": 5,
            "fields_present": ["hours", "description", "address", "phone"]
        },
        "competitors": [
            {
                "title": "Competitor 1",
                "review_count": 20,
                "average_rating": 4.5,
                "photo_count": 10,
                "fields_present": ["hours", "description", "address", "phone", "menu_link"]
            }
        ],
        "averages": {
            "review_count": 20,
            "average_rating": 4.5,
            "photo_count": 10
        },
        "competitor_field_presence": {
            "menu_link": True
        }
    }

@pytest.fixture
def competitors_profiles():
    return [
        {
            "title": "Competitor 1",
            "review_count": 20,
            "average_rating": 4.5,
            "photo_count": 10,
            "fields_present": ["hours", "description", "address", "phone", "menu_link"]
        }
    ]

def test_generate_comparison_suggestions_openai(monkeypatch, comparison_data, competitors_profiles):
    # Set up environment variable for OpenAI API key
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    # Mock openai.OpenAI and its chat.completions.create method
    mock_openai_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "AI generated summary and suggestions."
    mock_response.choices = [mock_choice]
    mock_openai_client.chat.completions.create.return_value = mock_response

    with patch("comparator.views.openai.OpenAI", return_value=mock_openai_client):
        result = generate_comparison_suggestions(comparison_data, competitors_profiles)
        assert result["ai_summary"] == "AI generated summary and suggestions."
        assert result["ai_provider"] == "openai"
        assert "openai" in result["ai_note"].lower()

def test_generate_comparison_suggestions_fallback(monkeypatch, comparison_data, competitors_profiles):
    # Ensure no OpenAI API key is set
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = generate_comparison_suggestions(comparison_data, competitors_profiles)
    assert "summary" in result
    assert "suggestions" in result
    assert result["ai_provider"] == "mock"
    assert "mock" in result["ai_note"].lower()
