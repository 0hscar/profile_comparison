import { ref, computed } from "vue";
import * as api from "../api";

/**
 * Composable for fetching and managing business profile and competitor data.
 * Company-level best practice: Keeps data logic out of components, reusable and testable.
 */
export function useProfileData() {
  // State
  const selectedBusiness = ref(null);
  const nearbyCompetitors = ref([]);
  const similarCompetitors = ref([]);
  const competitorMode = ref("nearby"); // "nearby" or "similar"
  const gamification = ref({ score: 0, badges: [] });
  const competitorHighlights = ref([]);
  const localTrends = ref([]);
  const photoInsights = ref([]);
  const profileHistory = ref([]);
  const competitorAlerts = ref([]);
  const loading = ref(false);

  const competitorList = computed(() =>
    competitorMode.value === "nearby"
      ? nearbyCompetitors.value
      : similarCompetitors.value
  );

  async function fetchCompetitorProfiles() {
    try {
      const competitors = await api.fetchCompetitorsProfiles();
      nearbyCompetitors.value = Array.isArray(competitors.nearby)
        ? competitors.nearby
        : [];
      similarCompetitors.value = Array.isArray(competitors.similar)
        ? competitors.similar
        : [];
    } catch (e) {
      nearbyCompetitors.value = [];
      similarCompetitors.value = [];
    }
  }

  /**
   * Fetch all business profile data (profile, gamification, trends, insights, etc.)
   */
  async function fetchAllProfileData() {
    loading.value = true;
    try {
      const profile = await api.fetchBusinessProfile();
      selectedBusiness.value = {
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
        profileCompleteness: profile.profile_completeness ?? null,
        lastProfileUpdate: profile.last_profile_update ?? null,
        menuAvailable: profile.menu_available ?? false,
        menuUrl: profile.menu_url ?? "",
      };
      gamification.value = profile.gamification || { score: 0, badges: [] };
      competitorHighlights.value = profile.competitorHighlights || [];
      localTrends.value = profile.localTrends || [];
      photoInsights.value = profile.photoInsights || [];
      profileHistory.value = profile.profileHistory || [];
      competitorAlerts.value = profile.competitorAlerts || [];
    } catch (e) {
      selectedBusiness.value = null;
    }
    loading.value = false;
  }

  /**
   * Export snapshot (stub for future implementation)
   */
  function exportSnapshot() {
    // TODO: Implement snapshot export (e.g., html2pdf)
  }

  return {
    // State
    selectedBusiness,
    competitorList,
    competitorMode,
    nearbyCompetitors,
    similarCompetitors,
    gamification,
    competitorHighlights,
    localTrends,
    photoInsights,
    profileHistory,
    competitorAlerts,
    loading,
    // Methods
    fetchAllProfileData,
    fetchCompetitorProfiles,
    exportSnapshot,
  };
}
