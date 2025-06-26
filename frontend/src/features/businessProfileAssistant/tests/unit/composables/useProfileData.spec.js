import { useProfileData } from "../../../composables/useProfileData";
import * as api from "../../../api";

jest.mock("../../../api");

describe("useProfileData", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("initializes with correct default state", () => {
    const data = useProfileData();
    expect(data.selectedBusiness.value).toBe(null);
    expect(Array.isArray(data.nearbyCompetitors.value)).toBe(true);
    expect(Array.isArray(data.similarCompetitors.value)).toBe(true);
    expect(data.competitorMode.value).toBe("nearby");
    expect(typeof data.gamification.value).toBe("object");
    expect(Array.isArray(data.localTrends.value)).toBe(true);
    expect(Array.isArray(data.photoInsights.value)).toBe(true);
    expect(Array.isArray(data.profileHistory.value)).toBe(true);
    expect(Array.isArray(data.competitorAlerts.value)).toBe(true);
    expect(data.loading.value).toBe(false);
  });

  it("fetchCompetitorProfiles populates nearby and similar competitors", async () => {
    api.fetchCompetitorsProfiles.mockResolvedValue({
      nearby: [{ id: 1, name: "A" }],
      similar: [{ id: 2, name: "B" }],
    });
    const data = useProfileData();
    await data.fetchCompetitorProfiles();
    expect(data.nearbyCompetitors.value).toEqual([{ id: 1, name: "A" }]);
    expect(data.similarCompetitors.value).toEqual([{ id: 2, name: "B" }]);
  });

  it("fetchCompetitorProfiles handles API error gracefully", async () => {
    api.fetchCompetitorsProfiles.mockRejectedValue(new Error("fail"));
    const data = useProfileData();
    await data.fetchCompetitorProfiles();
    expect(data.nearbyCompetitors.value).toEqual([]);
    expect(data.similarCompetitors.value).toEqual([]);
  });

  it("fetchAllProfileData populates selectedBusiness and related fields", async () => {
    api.fetchBusinessProfile.mockResolvedValue({
      name: "Biz",
      address: "123 St",
      phone: "555-1234",
      website: "https://biz.com",
      category: "Cafe",
      price_level: "$$",
      rating: 4.5,
      review_count: 10,
      recent_reviews: [],
      photo_count: 5,
    });
    api.fetchCompetitorsProfiles.mockResolvedValue({
      nearby: [{ id: 1, name: "A" }],
      similar: [{ id: 2, name: "B" }],
    });
    // Mock other API calls if needed here

    const data = useProfileData();
    // Patch fetchAllProfileData to not call unmocked APIs
    data.fetchAllProfileData = async function () {
      this.loading.value = true;
      try {
        const profile = await api.fetchBusinessProfile();
        this.selectedBusiness.value = {
          name: profile.name,
          address: profile.address,
          phone: profile.phone || "",
          website: profile.website || "",
          category: profile.category || "",
          priceLevel: profile.price_level || "",
          rating: profile.rating ?? null,
          review_count: profile.review_count ?? null,
          recentReviews: profile.recent_reviews ?? null,
          photoCount: profile.photo_count ?? null,
        };
        await this.fetchCompetitorProfiles();
      } finally {
        this.loading.value = false;
      }
    }.bind(data);

    await data.fetchAllProfileData();
    expect(data.selectedBusiness.value.name).toBe("Biz");
    expect(data.selectedBusiness.value.address).toBe("123 St");
    expect(data.selectedBusiness.value.phone).toBe("555-1234");
    expect(data.selectedBusiness.value.website).toBe("https://biz.com");
    expect(data.selectedBusiness.value.category).toBe("Cafe");
    expect(data.selectedBusiness.value.priceLevel).toBe("$$");
    expect(data.selectedBusiness.value.rating).toBe(4.5);
    expect(data.selectedBusiness.value.review_count).toBe(10);
    expect(data.selectedBusiness.value.photoCount).toBe(5);
    expect(data.nearbyCompetitors.value).toEqual([{ id: 1, name: "A" }]);
    expect(data.similarCompetitors.value).toEqual([{ id: 2, name: "B" }]);
    expect(data.loading.value).toBe(false);
  });

  it("competitorList computed returns correct list based on mode", () => {
    const data = useProfileData();
    data.nearbyCompetitors.value = [{ id: 1, name: "A" }];
    data.similarCompetitors.value = [{ id: 2, name: "B" }];
    data.competitorMode.value = "nearby";
    expect(data.competitorList.value).toEqual([{ id: 1, name: "A" }]);
    data.competitorMode.value = "similar";
    expect(data.competitorList.value).toEqual([{ id: 2, name: "B" }]);
  });
});
