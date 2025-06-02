print("ai_utils.py loaded")
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from comparator.utils.ai_prompts import restuaruant_compare_prompt_system, restaurant_compare_prompt_user
from comparator.utils.timing_utils import timeit
from django.http import JsonResponse
import json
import openai
import re
from typing import Any

def build_query_for_prompt(query: str, cards: list) -> str:
    """
    Build a query string for the prompt based on the provided query and cards.
    If query is empty, use the first card's title and address."""
    query = f"""{query}"""
    for idx, c in enumerate(cards, 1):
        query += f"""
        {idx}.
        Restaurant: {c.get("title", "Unknown Title")}
        Address: {c.get("address", "Unknown Address")}
        Rating: {c.get("rating", "No Rating")}
        Price Level: {c.get("priceLevel", "No Price")}
        Rating Count: {c.get("ratingCount", "No Rating Count")}
        Hours: {c.get("hours", "No Hours")}
        Menu: {c.get("menu", "No Menu")}
        Website: {c.get("website", "No Website")}
        Photos: {c.get("photos", "No Photos")}

        """
    return query

class Profile(BaseModel):
    Name: str
    Address: str
    Rating: str
    NumberOfReviews: str
    PriceLevel: str
    Cuisine: str
    Description: str
    AdditionalDetails: str
    Hours: str
    Menu: str
    Website: str
    Photos: list[str]


class AnalysisOutput(BaseModel):
    user_profile: list[Profile]
    competitor_profiles: list[list[Profile]]
    comparison: list[str]
    suggestions: list[str]
    extra_insights: list[str]

@timeit("OpenAI API call")
def sendToAI(user_query: str, competitor_query: str) -> AnalysisOutput | None:
    ai_api_key = os.environ.get("OPENAI_API_KEY")

    if not ai_api_key:
        raise Exception("OPENAI_API_KEY environment variable is not set.")

    client = openai.OpenAI(api_key=ai_api_key)

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": restuaruant_compare_prompt_system()},
            {"role": "user", "content": restaurant_compare_prompt_user(user_query, competitor_query)}
        ],
        text_format=AnalysisOutput,
        #max_tokens=5000,
        temperature=0
    )

    # Debug output, known bug where competitor query gets wild on second search without reload
    print("System prompt: ", restuaruant_compare_prompt_system())
    print("User prompt: ", restaurant_compare_prompt_user(user_query, competitor_query))

    content = response.output_parsed

    return content
