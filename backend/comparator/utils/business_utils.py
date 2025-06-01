print("business_utils.py loaded")
import os
import json
import http.client
from dotenv import load_dotenv
from comparator.utils.timing_utils import timeit

def fetch_business_profiles_from_serper(query: str, location: str, gl: str, searchModeEndpoint: str) -> dict:
    """
    Fetches business profiles from the Serper API.

    Returns:
        The parsed JSON response from the Serper API if successful, otherwise an empty list.
    """
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "location": location,
        "gl": gl
    })
    headers = {
        'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
        'Content-Type': 'application/json'
    }
    conn.request("POST", searchModeEndpoint, payload, headers)

    res = conn.getresponse()
    data = res.read()
    try:
        results = json.loads(data.decode("utf-8"))
        return results
    except Exception:
        return {}

def extract_menu_from_search(search_data, business_title):
    for organic in search_data.get("organic", []):
        if business_title.lower() in organic.get("title", "").lower():
            for sitelink in organic.get("sitelinks", []):
                title_lower = sitelink["title"].lower()
                link_lower = sitelink.get("link", "").lower()
                if "menu" in title_lower or "ruokalista" in title_lower:
                    return sitelink["link"]
                if "menu" in link_lower:
                    return f"Possibly this link: {sitelink['link']}"
    for organic in search_data.get("organic", []):
        for sitelink in organic.get("sitelinks", []):
            title_lower = sitelink["title"].lower()
            link_lower = sitelink.get("link", "").lower()
            if "menu" in title_lower or "ruokalista" in title_lower:
                return sitelink["link"]
            if "menu" in link_lower:
                return f"Possibly this link: {sitelink['link']}"
    return None

def extract_hours_from_search(search_data, business_title):
    kg = search_data.get("knowledgeGraph", {})
    if kg and business_title.lower() in kg.get("title", "").lower():
        attributes = kg.get("attributes", {})
        for k, v in attributes.items():
            if "hour" in k.lower():
                return v
    return None

def is_same_business(place, search_kg):
    if not search_kg:
        return False
    title_match = place.get("title", "").lower() == search_kg.get("title", "").lower()
    address_match = False
    if "address" in place and "attributes" in search_kg:
        for k, v in search_kg["attributes"].items():
            if "address" in k.lower() and place["address"].lower() in v.lower():
                address_match = True
    return title_match or address_match

def combine_all_info_for_place(place, search_data):
    combined = dict(place)
    kg = search_data.get("knowledgeGraph", {})
    if is_same_business(place, kg):
        for k, v in kg.items():
            if k not in combined:
                combined[k] = v
    for organic in search_data.get("organic", []):
        if place.get("title", "").lower() in organic.get("title", "").lower():
            for k, v in organic.items():
                if k not in combined and k != "sitelinks":
                    combined[k] = v
            menu_url = None
            possible_menu_url = None
            for sitelink in organic.get("sitelinks", []):
                title_lower = sitelink["title"].lower()
                link_lower = sitelink.get("link", "").lower()
                if "menu" in title_lower or "ruokalista" in title_lower:
                    menu_url = sitelink["link"]
                    break
                if "menu" in link_lower:
                    possible_menu_url = f"Possibly this link: {sitelink['link']}"
            if menu_url:
                combined["menu"] = menu_url
            elif possible_menu_url:
                combined["menu"] = possible_menu_url
            else:
                combined["menu"] = "Menu not found"
            combined["sitelinks"] = organic.get("sitelinks", [])
            break
    if "menu" not in combined:
        menu_url = extract_menu_from_search(search_data, place.get("title", ""))
        combined["menu"] = menu_url if menu_url else "Menu not found"
    hours = extract_hours_from_search(search_data, place.get("title", ""))
    combined["hours"] = hours if hours else "Opening hours not found"
    if "description" not in combined:
        snippet = None
        for organic in search_data.get("organic", []):
            if place.get("title", "").lower() in organic.get("title", "").lower():
                snippet = organic.get("snippet")
                break
        combined["description"] = snippet if snippet else "Description not found"
    return combined

@timeit("get_places_cards")
def get_places_cards(query: str, location: str, gl: str, num_places: int, fullInfo=True) -> list:
    serper_places = fetch_business_profiles_from_serper(query, location, gl, "/places")
    places = list(serper_places.get("places", [])[:num_places])
    cards = []
    # Faster search when less info is needed
    if fullInfo:
        serper_search = fetch_business_profiles_from_serper(query, location, gl, "/search")
        for place in places:
            card = combine_all_info_for_place(place, serper_search)
            cards.append(card)
        return cards
    return places

def filter_out_user_restaurant(cards: list, user_business_name: str, user_business_location: str) -> list:
    """
    Remove any card from the list that matches the user's restaurant by title and address.
    """
    filtered = [
        c for c in cards if not (
            c.get("title", "").lower().strip() == user_business_name.lower().strip() and
            c.get("address", "").lower().strip() == user_business_location.lower().strip()
        )
    ]
    return filtered
