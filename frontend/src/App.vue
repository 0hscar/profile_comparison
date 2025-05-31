<template>
  <div id="app">
    <!-- Fake Main App Background -->
    <div class="fake-main-app">
      <h1>Totally not a fake app background</h1>
      <div class="main-content-blocks">
        <div class="block">Fancy Widget Number 1</div>
        <div class="block">Not So Fanct Widget Number 2</div>
        <div class="block">The Real Fancy Widget Number 5</div>
      </div>
      <AppButton
        class="open-comparator-btn"
        variant="primary"
        round
        @click="showComparator = true"
      >
        Open Comparator
      </AppButton>
    </div>
    <!-- Slide-out Comparator Panel -->
    <div
      class="comparator-slideout"
      :class="{ open: showComparator }"
      tabindex="-1"
      aria-modal="true"
      role="dialog"
    >
      <div class="comparator-sticky-header">
        <AppButton
          class="close-btn"
          variant="secondary"
          round
          aria-label="Close"
          @click="showComparator = false"
          >&times;</AppButton
        >
        <h1>Business Profile Comparator</h1>
      </div>

      <div class="dashboard-layout">
        <!-- Sidebar: Default/Closest Results -->
        <aside class="sidebar">
          <div class="sidebar-content">
            <div v-if="defaultUserBusiness" class="sidebar-sticky-controls">
              <RestaurantCard
                :card="defaultUserBusiness"
                :isUser="true"
                :showDirectCompare="false"
              />
              <h2 style="margin-top: 0.5rem; text-align: center">
                {{ showNearby ? "Nearby Restaurants" : "Similar Restaurants" }}
              </h2>
              <div
                class="toggle-group"
                style="margin-top: 1rem; margin-bottom: 1rem"
              >
                <button
                  :class="['toggle-btn', { active: showNearby }]"
                  @click="toggleRestaurantGroup('nearby')"
                  type="button"
                >
                  Nearby
                </button>
                <button
                  :class="['toggle-btn', { active: !showNearby }]"
                  @click="toggleRestaurantGroup('similar')"
                  type="button"
                >
                  Similar
                </button>
              </div>
            </div>
            <transition name="slide" mode="out-in">
              <div :key="showNearby ? 'nearby' : 'similar'">
                <template
                  v-if="(showNearby ? defaultNearby : defaultSimilar).length"
                >
                  <RestaurantCard
                    v-for="(card, idx) in showNearby
                      ? defaultNearby
                      : defaultSimilar"
                    :key="card.place_id || card.title || idx"
                    :card="card"
                    :isUser="false"
                    :showDirectCompare="true"
                    :userBusinessName="userBusinessName"
                    :userBusinessLocation="userBusinessLocation"
                    @comparison-result="handleResults"
                  />
                </template>
                <template v-else>
                  <div class="loading">
                    <div class="spinner"></div>
                    <p>
                      Loading
                      {{ showNearby ? "nearby" : "similar" }} restaurants...
                    </p>
                  </div>
                </template>
              </div>
            </transition>
          </div>
        </aside>
        <!-- Main: Search and Results -->
        <main class="main-content">
          <InputForm
            @comparison-result="handleResults"
            @reset="resetAll"
            :userBusinessName="userBusinessName"
            :userBusinessLocation="userBusinessLocation"
          />
          <ProfileResults
            v-if="
              userProfile || (competitorProfiles && competitorProfiles.length)
            "
            :userProfile="userProfile"
            :competitorProfiles="competitorProfiles"
            :comparison="comparison"
            :suggestions="suggestions"
            :extraInsights="extraInsights"
            @reset="resetAll"
          />
        </main>
      </div>
    </div>
    <!-- Overlay when open -->
    <div
      v-if="showComparator"
      class="slideout-overlay"
      @click="showComparator = false"
    ></div>
  </div>
</template>

<script>
import InputForm from "./components/InputForm.vue";
import ProfileResults from "./components/Results.vue";
import RestaurantCard from "./components/RestaurantCard.vue";
import AppButton from "./components/AppButton.vue";

export default {
  name: "App",
  components: { InputForm, ProfileResults, RestaurantCard, AppButton },
  data() {
    return {
      defaultNearby: [],
      defaultSimilar: [],
      defaultUserBusiness: null,
      searchResults: [],
      comparison: null,
      suggestions: null,
      extraInsights: null,
      userProfile: null,
      competitorProfiles: [],
      showComparator: false,
      userBusinessName: "Stefan's Steakhouse",
      userBusinessLocation: "Helsinki, Finland",
      updatingNearby: false,
      showNearby: true, // true = show nearby, false = show similar
    };
  },

  methods: {
    async fetchUserRestaurant() {
      // Fetch only the user's restaurant card
      const payload = {
        user_business_name: this.userBusinessName || "Stefan's Steakhouse",
        user_business_location:
          this.userBusinessLocation || "Helsinki, Finland",
      };
      const response = await fetch("/api/fetch_user_restaurant/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      this.defaultUserBusiness = data.user_restaurant || null;
    },
    async fetchDefault() {
      this.defaultNearby = [];
      this.defaultSimilar = [];
      this.updatingNearby = true;
      const payload = {
        // Manually inserted for now
        user_business_name: this.userBusinessName || "Stefan's Steakhouse",
        user_business_location:
          this.userBusinessLocation || "Helsinki, Finland",
        user_business_category: "steak",
        num_places: 5,
      };
      const response = await fetch("/api/fetch_restaurant_groups/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      this.defaultNearby = data.nearby_restaurants || [];
      this.defaultSimilar = data.similar_restaurants || [];
      this.updatingNearby = false;
      console.log("nearby:", data.nearby_restaurants);
      console.log("similar:", data.similar_restaurants);
    },
    updateBusiness() {
      this.fetchUserRestaurant();
      this.fetchDefault();
    },
    handleResults(data) {
      // Set userProfile and competitorProfiles for Results.vue
      this.userProfile = data.user_profile || null;
      this.competitorProfiles = Array.isArray(data.competitor_profiles)
        ? data.competitor_profiles
        : [];
      this.comparison = data.comparison || null;
      this.suggestions = data.suggestions || null;
      this.extraInsights = data.extra_insights || null;
    },

    resetAll() {
      this.searchResults = null;
      this.comparison = null;
      this.suggestions = null;
      this.extraInsights = null;
      this.userProfile = null;
      this.competitorProfiles = [];
      this.fetchUserRestaurant();
      this.fetchDefault();
    },
    toggleRestaurantGroup(group) {
      this.showNearby = group === "nearby";
    },
  },
  mounted() {
    this.fetchUserRestaurant();
    this.fetchDefault();
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  min-height: 100vh;
  background: #e8eaf0;
  position: relative;
}

.fake-main-app {
  min-height: 100vh;
  padding: 3rem 2rem 2rem 2rem;
  background: linear-gradient(120deg, #e8eaf0 60%, #f7fafd 100%);
  border-radius: 0 0 24px 24px;
  box-shadow: 0 2px 16px #0001;
  position: relative;
  z-index: 1;
}

.fake-main-app h1 {
  text-align: center;
  font-size: 2.2rem;
  margin-bottom: 2.5rem;
  color: #2d8cf0;
  letter-spacing: 1px;
}

.main-content-blocks {
  display: flex;
  gap: 2rem;
  justify-content: center;
  margin-bottom: 3rem;
}
.block {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px #0001;
  padding: 2rem 2.5rem;
  min-width: 180px;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: #444;
}

.open-comparator-btn {
  position: fixed;
  right: 2.5rem;
  bottom: 2.5rem;
  z-index: 10;
  background: #2d8cf0;
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 1.1rem 2.2rem;
  font-size: 1.2rem;
  box-shadow: 0 2px 8px #0002;
  cursor: pointer;
  transition: background 0.2s;
}
.open-comparator-btn:hover {
  background: #1761a0;
}

.comparator-slideout {
  position: fixed;
  top: 0;
  right: 0;
  width: 50vw;
  min-width: 340px;
  max-width: 100vw;
  height: 100vh;
  background: #fafbfc;
  box-shadow: -2px 0 16px #0002;
  z-index: 1001;
  transform: translateX(100%);
  transition: transform 0.35s cubic-bezier(0.77, 0, 0.18, 1);
  overflow: hidden;
  padding: 0 0 0 0;
  display: flex;
  flex-direction: column;
}
.comparator-slideout.open {
  transform: translateX(0);
}
.comparator-sticky-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: #fafbfc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.2rem 2.5rem 1.2rem 2.5rem;
  border-bottom: 1px solid #e6eaf0;
  min-height: 64px;
}
.comparator-sticky-header h1 {
  flex: 1 1 auto;
  text-align: center;
  margin: 0;
  font-size: 2rem;
  color: #2d8cf0;
}
.business-fields-row {
  display: flex;
  align-items: flex-end;
  gap: 1.5rem;
  padding: 1.2rem 2.5rem 0.5rem 2.5rem;
  background: #fafbfc;
  border-bottom: 1px solid #e6eaf0;
  z-index: 9;
}
.business-fields-row .form-group {
  margin-bottom: 0;
}
.update-business-btn {
  margin-bottom: 0.2rem;
  height: 2.5rem;
}
.close-btn {
  position: static;
  margin-right: 1.5rem;
  margin-left: 0;
  background: none;
  border: none;
  font-size: 2.2rem;
  color: #888;
  cursor: pointer;
  z-index: 11;
  transition: color 0.2s;
  align-self: flex-start;
}
.close-btn:hover {
  color: #2d8cf0;
}
.dashboard-layout {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  padding: 0 2.5rem 2.5rem 2.5rem;
  flex: 1 1 auto;
  min-height: 0;
  height: 100%;
}
.sidebar {
  flex: 0 0 35%;
  max-width: 35%;
  background: #f5f8fa;
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 1px 4px #0001;
  min-height: 0;
  max-height: none;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  align-self: stretch;
  z-index: 2;
  height: auto;
}
.main-content {
  flex: 1 1 65%;
  max-width: 65%;
  min-width: 0;
  word-break: break-word;
  overflow-x: hidden;
  overflow-y: auto;
  min-height: 0;
  height: auto;
  align-self: stretch;
  display: flex;
  flex-direction: column;
}
.sidebar-sticky-header {
  position: sticky;
  top: 0;
  z-index: 3;
  background: #f5f8fa;
  padding: 1.5rem 1rem 1rem 1rem;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 1px 4px #0001;
}
.sidebar-sticky-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: #2d8cf0;
  text-align: center;
}
.sidebar-content {
  padding: 0 1rem 1.5rem 1rem;
}
.loading {
  text-align: center;
  margin-top: 2rem;
}

/* Spinner animation */
.spinner {
  margin: 0 auto 1rem auto;
  border: 4px solid #e6eaf0;
  border-top: 4px solid #2d8cf0;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  animation: spin 1s linear infinite;
  display: block;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.slideout-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.25);
  z-index: 1000;
  transition: opacity 0.2s;
}
@media (max-width: 900px) {
  .dashboard-layout {
    flex-direction: column;
    padding: 0 1rem 2rem 1rem;
  }
  .sidebar {
    max-height: none;
    min-height: unset;
    margin-bottom: 2rem;
  }
  .comparator-slideout {
    width: 100vw;
    min-width: 0;
    padding: 0;
  }
}

/* Slide transition for nearby/similar list */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.4s cubic-bezier(0.55, 0, 0.1, 1),
    opacity 0.4s cubic-bezier(0.55, 0, 0.1, 1);
  will-change: transform, opacity;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
.slide-enter-to,
.slide-leave-from {
  transform: translateX(0%);
  opacity: 1;
}
/* Responsive search box improvements */
.main-content form,
.main-content .input-form {
  width: 100%;
  max-width: 500px;
  margin: 0 auto 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.main-content .form-group {
  width: 100%;
}
.main-content input,
.main-content .v-select {
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}
.main-content .app-btn {
  width: auto;
  min-width: 120px;
  max-width: 220px;
  font-size: 1rem;
  padding: 0.6rem 1.2rem;
  align-self: flex-start;
  margin-bottom: 0.5rem;
}
.toggle-group {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.sidebar-sticky-controls {
  position: sticky;
  top: 0;
  z-index: 4;
  background: #f5f8fa;
  padding-top: 1rem;
  box-shadow: 0 2px 8px #0001;
}
.toggle-btn {
  background: #e6eaf0;
  color: #2d8cf0;
  border: none;
  border-radius: 4px 4px 0 0;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.toggle-btn.active,
.toggle-btn:hover {
  background: #2d8cf0;
  color: #fff;
}
</style>
