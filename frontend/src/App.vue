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
          <div class="sidebar-sticky-header">
            <h2>Nearby Restaurants</h2>
          </div>
          <div class="sidebar-content">
            <div
              v-if="
                defaultResults &&
                defaultResults.cards &&
                defaultResults.cards.length
              "
            >
              <RestaurantCard
                v-for="(card, idx) in defaultResults.cards"
                :key="card.place_id || card.title || idx"
                :card="card"
                :isUser="idx === 0"
              />
            </div>
            <div v-else class="loading">
              <p>Loading nearby restaurants...</p>
            </div>
          </div>
        </aside>
        <!-- Main: Search and Results -->
        <main class="main-content">
          <InputForm @comparison-result="handleResults" @reset="resetAll" />
          <ProfileResults
            v-if="searchResults"
            :results="searchResults"
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
      defaultResults: null,
      searchResults: null,
      showComparator: false,
    };
  },
  methods: {
    async fetchDefault() {
      this.defaultResults = null;
      const response = await fetch("/api/compare/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: "default" }),
      });
      this.defaultResults = await response.json();
    },
    handleResults(data) {
      this.searchResults = data;
    },
    resetAll() {
      this.searchResults = null;
    },
  },
  mounted() {
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
  overflow-y: auto;
  overflow-x: hidden;
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
}
.sidebar {
  flex: 0 0 35%;
  max-width: 35%;
  background: #f5f8fa;
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 1px 4px #0001;
  min-height: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: sticky;
  top: 0;
  align-self: flex-start;
  z-index: 2;
}
.main-content {
  flex: 0 0 65%;
  max-width: 65%;
  min-width: 0;
  word-break: break-word;
  overflow-x: hidden;
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
</style>
