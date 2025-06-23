from typing import List, Dict, Any, Generator, Type, Callable, TypeVar, cast
from pydantic import BaseModel
import openai
import os
from comparator.utils.cache_utils import check_for_cached_data, set_cached_data, safe_cache_key
import json
from functools import wraps

T = TypeVar('T', bound=BaseModel)

class BusinessProfile(BaseModel):
    name: str
    address: str
    rating: float
    review_count: int
    price_level: str
    category: str
    description: str = ""
    hours: List[str] = []
    menu_url: str = ""
    website: str = ""
    photos: List[str] = []

class BusinessProfileList(BaseModel):
    List[BusinessProfile]

class AISuggestion(BaseModel):
    suggestions: List[str]

class WhatIfResult(BaseModel):
    predictedScore: float
    breakdown: List[Dict[str, Any]]
    aiComment: str

def ai_cache(model: Type[T]):
    """
    Decorator for caching structured AI responses.
    """
    def decorator(ai_func: Callable[..., T]) -> Callable[..., T]:
        @wraps(ai_func)
        def wrapper(*args, cache_key: str, **kwargs) -> T:
            cached = check_for_cached_data(cache_key)
            if cached:
                return model(**cached)
            result = ai_func(*args, **kwargs)
            set_cached_data(cache_key, result.dict())
            return result
        return cast(Callable[..., T], wrapper)
    return decorator

def get_openai_client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
    return openai.OpenAI(api_key=api_key)

def get_competitors_from_serper(
    profile: BusinessProfile,
    mode: str = "nearby",
    max_results: int = 5
) -> Generator[BusinessProfile, None, None]:
    """
    Uses the Serper API to search for business competitors.
    mode: "nearby" (default) or "similar"
    Returns a list of BusinessProfile objects.
    """
    import requests

    serper_api_key = os.environ.get("SERPER_API_KEY")
    if not serper_api_key:
        raise RuntimeError("SERPER_API_KEY environment variable is not set.")

    # Build the search query
    if mode == "nearby":
        query = f"{profile.category} near {profile.address}"
    elif mode == "similar":
        query = f"{profile.category} similar to {profile.name} in {profile.address}"
    else:
        raise ValueError("mode must be 'nearby' or 'similar'")

    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "gl": "fi",
        "hl": "en"
    }
    response = requests.post(
        "https://google.serper.dev/places",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise RuntimeError(f"Serper API error: {response.status_code} {response.text}")

    data = response.json()
    places = data.get("places", [])[:max_results]

    # Use OpenAI to structure the results into BusinessProfile objects
    client = get_openai_client()
    openai_prompt = f"""
    Given the following raw search results for businesses, extract a list of up to {max_results} competitors as a JSON array.
    Each competitor should be a JSON object with these fields: name, address, rating, review_count, price_level, category, description, hours, menu_url, website, photos.
    If a field is missing, use an empty string or empty list as appropriate.

    Raw search results:
    {json.dumps(places, indent=2)}

    Return ONLY a JSON array, not Python code, not markdown, not text, not BusinessProfile(...). Just plain JSON.
    """

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data extraction assistant."},
            {"role": "user", "content": openai_prompt}
        ],
        max_tokens=2048,
        temperature=0.2,
        stream=True,
    )

    buffer = ""
    inside_array = False
    brace_count = 0

    for chunk in stream:
        if hasattr(chunk.choices[0].delta, "content"):
            text = chunk.choices[0].delta.content
            for char in text:
                if char == '[' and not inside_array:
                    inside_array = True
                    continue
                if inside_array:
                    buffer += char
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            # Try to parse the object
                            try:
                                obj_str = buffer.strip().rstrip(',\n ')
                                if obj_str.endswith(']'):
                                    obj_str = obj_str[:-1]
                                competitor = json.loads(obj_str)
                                yield BusinessProfile(**competitor)
                            except Exception:
                                pass
                            buffer = ""
                    elif char == ']':
                        return  # End of array





@ai_cache(AISuggestion)
def generate_ai_suggestions_core(profile: BusinessProfile, competitors: List[BusinessProfile]) -> AISuggestion:
    client = get_openai_client()
    prompt = f"""
    Analyze the following business profile and its competitors.
    Suggest 3-5 actionable improvements to attract more customers.

    Business:
    {profile.json()}

    Competitors:
    {chr(10).join([c.json() for c in competitors])}
    """
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "You are a business profile optimization assistant."},
            {"role": "user", "content": prompt}
        ],
        text_format=AISuggestion,
        temperature=0.7,
    )
    return response.output_parsed

def generate_ai_suggestions(profile: BusinessProfile, competitors: List[BusinessProfile]) -> AISuggestion:
    cache_key = safe_cache_key(
        f"ai_suggestions:{profile.json()}|{json.dumps([c.dict() for c in competitors], sort_keys=True)}"
    )
    return generate_ai_suggestions_core(profile, competitors, cache_key=cache_key)

@ai_cache(WhatIfResult)
def simulate_what_if_core(profile: BusinessProfile, changes: Dict[str, Any]) -> WhatIfResult:
    client = get_openai_client()
    prompt = f"""
    Given the following business profile and proposed changes, predict the new profile score (0-100), provide a breakdown of the impact of each change, and a short comment.

    Business:
    {profile.json()}

    Changes:
    {changes}
    """
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "You are a business profile optimization assistant."},
            {"role": "user", "content": prompt}
        ],
        text_format=WhatIfResult,
        temperature=0.7,
    )
    return response.output_parsed

def simulate_what_if(profile: BusinessProfile, changes: Dict[str, Any]) -> WhatIfResult:
    cache_key = safe_cache_key(
        f"whatif:{profile.json()}|{json.dumps(changes, sort_keys=True)}"
    )
    return simulate_what_if_core(profile, changes, cache_key=cache_key)

def profile_assistant_response(question: str, profile: BusinessProfile) -> Generator[str, None, None]:
    """
    Stream a conversational, actionable answer to the user's business question.
    Yields chunks of text as they are generated by the AI.
    """
    client = get_openai_client()
    prompt = f"""
    You are a helpful business advisor. Given the following business profile, answer the user's question in a friendly, actionable way.

    Business:
    {profile.json()}

    User question:
    {question}
    """
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful business advisor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        temperature=0.7,
        stream=True,
    )
    for chunk in stream:
        if hasattr(chunk.choices[0].delta, "content"):
            yield chunk.choices[0].delta.content

def generate_social_caption(prompt: str, profile: BusinessProfile) -> Generator[str, None, None]:
    """
    Stream a creative, catchy social media caption for the business.
    Yields chunks of text as they are generated by the AI.
    """
    client = get_openai_client()
    ai_prompt = f"""
    Write a catchy, friendly Instagram caption for the following restaurant. Use emojis and hashtags. Base it on this prompt: "{prompt}"

    Business:
    {profile.json()}
    """
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative social media manager."},
            {"role": "user", "content": ai_prompt}
        ],
        max_tokens=128,
        temperature=0.9,
        stream=True,
    )
    for chunk in stream:
        if hasattr(chunk.choices[0].delta, "content"):
            yield chunk.choices[0].delta.content
