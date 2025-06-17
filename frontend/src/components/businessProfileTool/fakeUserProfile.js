/**
 * Fake user profile data for Nordic Bistro, Helsinki.
 * Use this object as mock data for all profile-related features in the BusinessProfileSlideout.
 */

export const fakeUserProfile = {
  business: {
    name: "Nordic Bistro",
    address: "Mannerheimintie 1, 00100 Helsinki",
    latitude: 60.1699,
    longitude: 24.9384,
    phone: "+358 9 1234567",
    website: "https://www.nordicbistro.fi/",
    category: "Modern European Restaurant",
    priceLevel: "€€",
    googleCid: "1234567890123456789",
    googleMapsUrl: "https://goo.gl/maps/fakeNordicBistro",
    photos: [
      {
        url: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
        alt: "Nordic Bistro Helsinki interior",
        tags: ["interior", "dining room", "ambience"],
      },
      {
        url: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
        alt: "Signature dish at Nordic Bistro",
        tags: ["food", "main course", "signature"],
      },
      {
        url: "https://images.unsplash.com/photo-1464306076886-debca5e8a6b0?auto=format&fit=crop&w=800&q=80",
        alt: "Dessert at Nordic Bistro",
        tags: ["dessert", "food"],
      },
    ],
    openingHours: [
      { day: "Monday", hours: "11:00–22:00" },
      { day: "Tuesday", hours: "11:00–22:00" },
      { day: "Wednesday", hours: "11:00–22:00" },
      { day: "Thursday", hours: "11:00–23:00" },
      { day: "Friday", hours: "11:00–00:00" },
      { day: "Saturday", hours: "12:00–00:00" },
      { day: "Sunday", hours: "12:00–21:00" },
    ],
    social: {
      facebook: "https://www.facebook.com/nordicbistro/",
      instagram: "https://www.instagram.com/nordicbistro/",
    },
  },
  stats: {
    rating: 4.6,
    ratingCount: 542,
    reviewCount: 530,
    recentReviews: 18, // in last 3 months
    photoCount: 27,
    menuAvailable: true,
    menuUrl: "https://www.nordicbistro.fi/menu/",
    profileCompleteness: 95, // percent
    lastProfileUpdate: "2024-06-01",
  },
  reviews: [
    {
      author: "Sanna L.",
      date: "2024-06-10",
      rating: 5,
      text: "Absolutely loved the seasonal tasting menu! Beautiful presentation and cozy atmosphere.",
      replied: true,
    },
    {
      author: "Jari M.",
      date: "2024-05-28",
      rating: 4,
      text: "Great food and friendly staff. The vegan options were a pleasant surprise.",
      replied: true,
    },
    {
      author: "Elina V.",
      date: "2024-05-15",
      rating: 5,
      text: "Perfect spot for a date night. The desserts are a must-try!",
      replied: false,
    },
  ],
  keywords: [
    "modern",
    "seasonal",
    "tasting menu",
    "vegan options",
    "cozy",
    "central Helsinki",
    "desserts",
    "friendly staff",
    "ambience",
  ],
  aiSuggestions: [
    "Add more photos of vegan and gluten-free dishes.",
    "Encourage guests to tag Nordic Bistro on Instagram for a chance to win a free dessert.",
    "Reply to all recent reviews to show engagement.",
    "Highlight your seasonal tasting menu in your Google Business description.",
    "Promote weekday lunch specials on social media.",
  ],
  gamification: {
    score: 93,
    badges: [
      {
        name: "Photo Pro",
        description: "Added 25+ high-quality photos",
        icon: "📸",
        unlocked: true,
      },
      {
        name: "Review Responder",
        description: "Replied to 15+ reviews",
        icon: "💬",
        unlocked: true,
      },
      {
        name: "Menu Master",
        description: "Menu available online",
        icon: "📄",
        unlocked: true,
      },
      {
        name: "Profile 95%",
        description: "Profile completeness over 95%",
        icon: "✅",
        unlocked: true,
      },
      {
        name: "Engaged Owner",
        description: "Replied to all reviews in the last month",
        icon: "🤝",
        unlocked: false,
      },
    ],
  },
  competitorHighlights: [
    "Nearby 'Urban Eatery' has 30% more recent reviews.",
    "'Bistro Helsinki' posts daily stories on Instagram and gets high engagement.",
    "Competitors promote their lunch specials more actively.",
  ],
  localTrends: [
    "Customers are searching for: summer terrace, vegan brunch, local ingredients.",
    "High interest in chef's tasting menus and dessert samplers.",
  ],
  photoInsights: [
    "Most photos are of main courses; add more ambience and staff photos.",
    "Outdoor seating photos are underrepresented.",
    "Competitors have more photos of group events and celebrations.",
  ],
  profileHistory: [
    { date: "2024-03-01", score: 88, photos: 20, reviews: 480 },
    { date: "2024-04-01", score: 91, photos: 23, reviews: 510 },
    { date: "2024-05-01", score: 93, photos: 27, reviews: 530 },
  ],
  competitorAlerts: [
    "Urban Eatery just added 10 new photos.",
    "Bistro Helsinki is running a summer terrace campaign.",
    "A new vegan cafe opened 200m away.",
  ],
};
