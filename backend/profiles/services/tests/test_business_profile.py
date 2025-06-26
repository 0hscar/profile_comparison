import pytest
from unittest import mock
from profiles.services.business_profile import profile_assistant_response
from profiles.models.business_profile import BusinessProfile
from profiles.mockdata.fake_profile import FAKE_PROFILE
from profiles.utils.constants import ALLOWED_LLM_MODELS

@pytest.fixture
def fake_profile():
    return BusinessProfile(**FAKE_PROFILE)

@pytest.fixture
def mock_openai_client():
    with mock.patch("profiles.services.business_profile.get_openai_client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_cache_decorator():
    # Patch the cache_generator_response decorator to be a no-op for testing
    with mock.patch("profiles.services.business_profile.cache_generator_response", lambda x: x):
        yield

def test_profile_assistant_response_valid_model(fake_profile, mock_openai_client, mock_cache_decorator):
    # Mock the OpenAI stream to yield fake chunks
    mock_stream = [
        mock.Mock(choices=[mock.Mock(delta=mock.Mock(content="Hello "))]),
        mock.Mock(choices=[mock.Mock(delta=mock.Mock(content="world!"))]),
    ]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_stream

    chunks = list(profile_assistant_response("What is AI?", fake_profile, model=ALLOWED_LLM_MODELS[0]))
    assert "".join(chunks) == "Hello world!"
    mock_openai_client.assert_called_once()

def test_profile_assistant_response_invalid_model(fake_profile, mock_cache_decorator):
    invalid_model = "not-a-real-model"
    with pytest.raises(ValueError) as excinfo:
        list(profile_assistant_response("Test?", fake_profile, model=invalid_model))
    assert invalid_model in str(excinfo.value)

def test_profile_assistant_response_openai_error(fake_profile, mock_openai_client, mock_cache_decorator):
    # Simulate OpenAI client raising an error
    mock_openai_client.return_value.chat.completions.create.side_effect = RuntimeError("OpenAI error")
    # Use a unique question to avoid cache hits
    with pytest.raises(RuntimeError) as excinfo:
        list(profile_assistant_response("What is AI? (error test)", fake_profile, model=ALLOWED_LLM_MODELS[0]))
    assert "OpenAI error" in str(excinfo.value)
