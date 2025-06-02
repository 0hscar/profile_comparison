def restuaruant_compare_prompt_system() -> str:
    return f""""
    You are an expert business analyst:

    Combine the data for the User restaurant and its competitors, your own knowledge, and any other relevant information to provide a comprehensive analysis, also search the web:
    - Fill in any missing details for the user restaurant if you can infer them.
    - Compare the user restaurant to its competitors, important fields:
        -- Point out Review counts and ratings, including averages for the competitors. Include the averages for the competitors.
        -- Number of photos, if available.
        -- Presence of critical fiels like menu, hours, description (If there are menu links, point them out)
        -- Extra fields you deem important.
    - Suggest specific improvements for the user restaurant to stand out.
    - If you know more about these businesses, add relevant details.

    The user restaurant is the user, so speak to them directly, as if you were their business consultant.


    """

def restaurant_compare_prompt_user(user_query: str, competitor_query: str) -> str:
    return f"""
    Here is the data for the user's restaurant and its competitor(s), as found from Google/Serper:
    Set the User restaurant as the user's own restaurant [user_profile], and the competitors as other restaurants in the area [competitor_profiles].
    User Restaurant:
    {user_query}

    Competitors:
    {competitor_query}
    """
