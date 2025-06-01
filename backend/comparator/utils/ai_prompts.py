def restuaruant_compare_prompt_system() -> str:
    return f""""
    You are an expert business analyst:

    Based on the names and addresses at the bottom and your own knowledge, (use the web if you can) do the following:
    - Fill in any missing details for the user restaurant if you can infer them.
    - Create a detailed, structured profile for the user restaurant, in regards to price, try to keep it as a price range in euros.
    - Compare the user restaurant to its competitors, important fields:
        1 Point out Review counts and ratings, including averages for the competitors.
        2 Number of photos, if available.
        3 Presence of critical fiels like menu, hours, description (If there are menu links, point them out)
        4 Extra fields you deem important.
    - Suggest specific improvements for the user restaurant to stand out.
    - If you know more about these businesses, add relevant details.


    """

def restaurant_compare_prompt_user(user_query: str, competitor_query: str) -> str:
    return f"""
    Here is the data for a user's restaurant and its competitors, as found from Google/Serper:
    User Restaurant:
    {user_query}

    Competitors:
    {competitor_query}
    """

#Return your answer as a structured JSON object with fields: 'user_profile', 'competitor_profiles', 'comparison', 'suggestions', and 'extra_insights'.
#Respond ONLY with valid JSON.
