import os
import pytest
from unittest.mock import patch, MagicMock

from comparator.utils.ai_utils import sendToAI, AnalysisOutput

@pytest.fixture
def mock_openai_response():
    from comparator.utils.ai_utils import Profile

    class MockOutputParsed:
        user_profile = [
            Profile(
                Name="Test User", Address="", Rating="", NumberOfReviews="", PriceLevel="",
                Cuisine="", Description="", AdditionalDetails="", Hours="", Menu="", Website="", Photos=[]
            )
        ]
        competitor_profiles = [[
            Profile(
                Name="Test Competitor", Address="", Rating="", NumberOfReviews="", PriceLevel="",
                Cuisine="", Description="", AdditionalDetails="", Hours="", Menu="", Website="", Photos=[]
            )
        ]]
        comparison = ["Comparison text"]
        suggestions = ["Suggestion text"]
        extra_insights = ["Extra insight"]

    mock_response = MagicMock()
    mock_response.output_parsed = MockOutputParsed()
    return mock_response

@patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"})
@patch("comparator.utils.ai_utils.openai.OpenAI")
@patch("comparator.utils.ai_utils.restuaruant_compare_prompt_system", return_value="system prompt")
@patch("comparator.utils.ai_utils.restaurant_compare_prompt_user", return_value="user prompt")
def test_sendToAI_success(
    mock_restaurant_compare_prompt_user,
    mock_restuaruant_compare_prompt_system,
    mock_openai,
    mock_openai_response
):
    # Arrange
    mock_client = MagicMock()
    mock_client.responses.parse.return_value = mock_openai_response
    mock_openai.return_value = mock_client

    user_query = "User restaurant info"
    competitor_query = "Competitor restaurant info"

    # Act
    result = sendToAI(user_query, competitor_query)

    # Assert
    assert isinstance(result, object)
    assert hasattr(result, "user_profile")
    assert hasattr(result, "competitor_profiles")
    assert hasattr(result, "comparison")
    assert hasattr(result, "suggestions")
    assert hasattr(result, "extra_insights")
    assert result.user_profile[0].Name == "Test User"
    assert result.competitor_profiles[0][0].Name == "Test Competitor"
    assert result.comparison[0] == "Comparison text"
    assert result.suggestions[0] == "Suggestion text"
    assert result.extra_insights[0] == "Extra insight"
