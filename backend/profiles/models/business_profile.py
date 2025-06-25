from typing import List
from pydantic import BaseModel

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
    profile_completeness: int = 0
    photo_count: int = 0
    recent_reviews: int = 0
    last_profile_update: str = ""
    menu_available: bool = False
    gamification: dict = {}
