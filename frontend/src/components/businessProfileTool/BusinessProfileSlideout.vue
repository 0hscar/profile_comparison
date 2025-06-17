<template>
  <div
    class="business-profile-slideout"
    :class="{ open: open }"
    tabindex="-1"
    aria-modal="true"
    role="dialog"
  >
    <!-- Sticky Header -->
    <div class="slideout-sticky-header">
      <button class="close-btn" aria-label="Close" @click="$emit('close')">
        &times;
      </button>
      <h1>Business Profile Analyzer</h1>
    </div>
    <div class="dashboard-layout">
      <!-- Sidebar: Business Search & Competitor List -->
      <aside class="sidebar">
        <!-- Competitor List Placeholder -->
        <section class="sidebar-section" v-if="selectedBusiness">
          <h2 class="sidebar-title">Competitors</h2>
          <ul class="competitor-list">
            <li
              v-for="comp in competitorHighlights"
              :key="comp"
              class="competitor-item"
            >
              {{ comp }}
            </li>
          </ul>
        </section>
        <!-- Gamification Badges -->
        <section class="sidebar-section" v-if="selectedBusiness">
          <h2 class="sidebar-title">Badges</h2>
          <div class="badges-list">
            <BadgeCard
              v-for="badge in gamification.badges"
              :key="badge.name"
              :badge="badge"
            />
          </div>
        </section>
        <!-- Business Info -->
        <section class="sidebar-section" v-if="selectedBusiness">
          <h2 class="sidebar-title">Business Info</h2>
          <div class="sidebar-business-info">
            <div><strong>Name:</strong> {{ selectedBusiness.name }}</div>
            <div><strong>Address:</strong> {{ selectedBusiness.address }}</div>
            <div><strong>Phone:</strong> {{ selectedBusiness.phone }}</div>
            <div>
              <strong>Website:</strong>
              <a :href="selectedBusiness.website" target="_blank">{{
                selectedBusiness.website
              }}</a>
            </div>
            <div>
              <strong>Category:</strong> {{ selectedBusiness.category }}
            </div>
            <div>
              <strong>Price Level:</strong> {{ selectedBusiness.priceLevel }}
            </div>
          </div>
        </section>
      </aside>
      <!-- Main Content: Profile Analysis & AI Features -->
      <main class="main-content">
        <!-- Profile Health & Score -->
        <section v-if="selectedBusiness" class="main-section">
          <h2 class="main-title">Profile Health</h2>
          <div class="score-bar">
            <progress
              :value="gamification.score"
              max="100"
              class="score-progress"
            ></progress>
            <span class="score-label">{{ gamification.score }}%</span>
          </div>
          <div v-if="gamification.score === 100" class="score-complete">
            🎉 Your profile is fully optimized! Keep it fresh for ongoing
            rewards.
          </div>
          <div class="profile-stats">
            <div>
              <strong>Rating:</strong>
              {{ selectedBusiness && selectedBusiness.rating }} ({{
                selectedBusiness && selectedBusiness.review_count
              }}
              reviews)
            </div>
            <div>
              <strong>Recent Reviews:</strong>
              {{ selectedBusiness && selectedBusiness.recentReviews }} (last 3
              months)
            </div>
            <div>
              <strong>Photo Count:</strong>
              {{ selectedBusiness && selectedBusiness.photoCount }}
            </div>
            <div>
              <strong>Menu:</strong>
              <a
                v-if="selectedBusiness && selectedBusiness.menuAvailable"
                :href="selectedBusiness && selectedBusiness.menuUrl"
                target="_blank"
                >View Menu</a
              >
              <span v-else>No menu online</span>
            </div>
            <div>
              <strong>Profile Completeness:</strong>
              {{ selectedBusiness && selectedBusiness.profileCompleteness }}%
            </div>
            <div>
              <strong>Last Update:</strong>
              {{ selectedBusiness && selectedBusiness.lastProfileUpdate }}
            </div>
          </div>
        </section>
        <!-- AI Suggestions -->
        <section v-if="aiSuggestions.length" class="main-section">
          <h2 class="main-title">AI Suggestions</h2>
          <ul class="suggestions-list">
            <li v-for="suggestion in aiSuggestions" :key="suggestion">
              {{ suggestion }}
            </li>
          </ul>
        </section>
        <!-- What If Simulator -->
        <section v-if="selectedBusiness" class="main-section">
          <h2 class="main-title">What If Simulator</h2>
          <div class="simulator-inputs">
            <label>
              Photos to Add
              <input
                type="number"
                v-model.number="simulated.photos"
                min="0"
                class="simulator-input"
              />
            </label>
            <label>
              Reviews to Gain
              <input
                type="number"
                v-model.number="simulated.reviews"
                min="0"
                class="simulator-input"
              />
            </label>
            <button class="simulator-btn" @click="simulateImpact">
              Simulate
            </button>
          </div>
          <div v-if="simulated.result !== null" class="simulator-result">
            Predicted Profile Score: {{ simulated.result }}%
          </div>
        </section>
        <!-- Local Market Trends -->
        <section v-if="localTrends.length" class="main-section">
          <h2 class="main-title">Local Market Trends</h2>
          <ul class="trends-list">
            <li v-for="trend in localTrends" :key="trend">{{ trend }}</li>
          </ul>
        </section>
        <!-- Photo Insights -->
        <section v-if="photoInsights.length" class="main-section">
          <h2 class="main-title">Photo Insights</h2>
          <ul class="photo-insights-list">
            <li v-for="insight in photoInsights" :key="insight">
              {{ insight }}
            </li>
          </ul>
        </section>
        <!-- Profile History -->
        <section v-if="profileHistory.length" class="main-section">
          <h2 class="main-title">Profile History</h2>
          <ul class="history-list">
            <li v-for="entry in profileHistory" :key="entry.date">
              {{ entry.date }} - Score: {{ entry.score }}% | Photos:
              {{ entry.photos }} | Reviews: {{ entry.reviews }}
            </li>
          </ul>
        </section>
        <!-- Competitor Alerts -->
        <section v-if="competitorAlerts.length" class="main-section">
          <h2 class="main-title">Competitor Alerts</h2>
          <ul class="alerts-list">
            <li v-for="alert in competitorAlerts" :key="alert">{{ alert }}</li>
          </ul>
        </section>
        <!-- Voice-Driven Profile Assistant -->
        <section v-if="selectedBusiness" class="main-section">
          <h2 class="main-title">Profile Assistant (Voice)</h2>
          <div class="assistant-row">
            <input
              v-model="voiceQuery"
              type="text"
              placeholder="Ask how to improve your business..."
              class="assistant-input"
            />
            <button class="assistant-btn" @click="askAssistant">Ask</button>
          </div>
          <div v-if="assistantResponse" class="assistant-response">
            {{ assistantResponse }}
          </div>
        </section>
        <!-- Social Media Booster -->
        <section v-if="selectedBusiness" class="main-section">
          <h2 class="main-title">Social Media Booster</h2>
          <div class="booster-row">
            <input
              v-model="captionPrompt"
              type="text"
              placeholder="Describe your post or select a review/photo..."
              class="booster-input"
            />
            <button class="booster-btn" @click="generateCaption">
              Generate Caption
            </button>
          </div>
          <div v-if="socialCaption" class="booster-response">
            {{ socialCaption }}
          </div>
        </section>
        <!-- Snapshot Export -->
        <section v-if="selectedBusiness" class="main-section">
          <button class="export-btn" @click="exportSnapshot">
            Download Snapshot Report
          </button>
        </section>
      </main>
    </div>
  </div>
  <div v-if="open" class="slideout-overlay" @click="$emit('close')" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import BadgeCard from "./BadgeCard.vue";
import * as api from "./api.js";

// Slideout open/close prop
defineProps({
  open: { type: Boolean, required: true },
});

// State

const selectedBusiness = ref(null);
const aiSuggestions = ref([]);
const gamification = ref({ score: 0, badges: [] });
const competitorHighlights = ref([]);
const simulated = ref({ photos: 0, reviews: 0, result: null });
const localTrends = ref([]);
const voiceQuery = ref("");
const assistantResponse = ref("");
const photoInsights = ref([]);
const captionPrompt = ref("");
const socialCaption = ref("");
const profileHistory = ref([]);
const competitorAlerts = ref([]);
const loading = ref(false);

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
    };
    gamification.value = profile.gamification || { score: 0, badges: [] };
    competitorHighlights.value = profile.competitorHighlights || [];
    localTrends.value = profile.localTrends || [];
    photoInsights.value = profile.photoInsights || [];
    profileHistory.value = profile.profileHistory || [];
    competitorAlerts.value = profile.competitorAlerts || [];
    // fallback for demo: if backend doesn't provide, keep empty
  } catch (e) {
    // handle error
    selectedBusiness.value = null;
  }
  loading.value = false;
}

async function fetchAISuggestions() {
  try {
    const data = await api.fetchAISuggestions();
    aiSuggestions.value = data.suggestions || [];
  } catch (e) {
    aiSuggestions.value = [];
  }
}

async function simulateImpact() {
  loading.value = true;
  try {
    const changes = {
      photos: simulated.value.photos,
      reviews: simulated.value.reviews,
    };
    const result = await api.simulateWhatIf(changes);
    simulated.value.result = result.predictedScore?.toFixed(1) ?? null;
  } catch (e) {
    simulated.value.result = null;
  }
  loading.value = false;
}

function askAssistant() {
  assistantResponse.value = "";
  api.streamProfileAssistant(voiceQuery.value, (chunk, fullText) => {
    assistantResponse.value = fullText;
  });
}

function generateCaption() {
  socialCaption.value = "";
  api.streamSocialCaption(captionPrompt.value, (chunk, fullText) => {
    socialCaption.value = fullText;
  });
}

function exportSnapshot() {
  // TODO: Implement snapshot export (e.g., html2pdf)
}

onMounted(async () => {
  await fetchAllProfileData();
  await fetchAISuggestions();
});
</script>

<style scoped>
.business-profile-slideout {
  position: fixed;
  top: 0;
  right: 0;
  width: clamp(960px, 50vw, 100vw);
  min-width: 0;
  max-width: 100vw;
  height: 100vh;
  background: #fafbfc;
  box-shadow: -2px 0 16px #0002;
  z-index: 1001;
  transform: translateX(100%);
  transition: transform 0.35s cubic-bezier(0.77, 0, 0.18, 1);
  overflow: hidden;
  padding: 0;
  display: flex;
  flex-direction: column;
}
.business-profile-slideout.open {
  transform: translateX(0);
}
.slideout-sticky-header {
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
.slideout-sticky-header h1 {
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
  flex: 1 1 auto;
  min-height: 0;
  height: 100%;
}
.sidebar {
  flex: 0 0 35%;
  max-width: 35%;
  background: #f5f8fa;
  border-radius: 8px;
  padding: 1.5rem 1rem 1.5rem 1rem;
  box-shadow: 0 1px 4px #0001;
  min-height: 0;
  max-height: none;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  align-self: stretch;
  z-index: 2;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.sidebar-section {
  margin-bottom: 2rem;
}
.sidebar-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #2d8cf0;
}
.sidebar-input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  margin-bottom: 0.5rem;
}
.autocomplete-list {
  background: #fff;
  border: 1px solid #e6eaf0;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  max-height: 160px;
  overflow-y: auto;
}
.autocomplete-item {
  padding: 0.5rem;
  cursor: pointer;
  transition: background 0.15s;
}
.autocomplete-item:hover {
  background: #e6eaf0;
}
.autocomplete-address {
  display: block;
  font-size: 0.85em;
  color: #888;
}
.sidebar-btn {
  width: 100%;
  background: #2d8cf0;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 0;
  font-size: 1rem;
  margin-top: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}
.sidebar-btn:hover {
  background: #1761a0;
}
.competitor-list {
  list-style: disc inside;
  padding-left: 1rem;
}
.competitor-item {
  margin-bottom: 0.25rem;
}
.badges-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
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
  gap: 2rem;
}
.main-section {
  margin-bottom: 2rem;
}
.main-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #2d8cf0;
}
.score-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}
.score-progress {
  width: 180px;
  height: 1.2rem;
  border-radius: 8px;
  background: #eee;
}
.score-label {
  font-weight: bold;
  font-size: 1.1rem;
}
.score-complete {
  color: #10b981;
  font-weight: 600;
  margin-top: 0.5rem;
}
.suggestions-list,
.trends-list,
.photo-insights-list,
.history-list,
.alerts-list {
  list-style: disc inside;
  padding-left: 1rem;
}
.simulator-inputs {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  margin-bottom: 0.5rem;
}
.simulator-input {
  width: 70px;
  padding: 0.3rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  margin-left: 0.5rem;
}
.simulator-btn {
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.simulator-btn:hover {
  background: #4338ca;
}
.simulator-result {
  margin-top: 0.5rem;
  font-weight: 500;
}
.assistant-row,
.booster-row {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  margin-bottom: 0.5rem;
}
.assistant-input,
.booster-input {
  flex: 1 1 auto;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
}
.assistant-btn,
.booster-btn {
  background: #a21caf;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.assistant-btn:hover,
.booster-btn:hover {
  background: #701a75;
}
.assistant-response,
.booster-response {
  background: #f3f4f6;
  border-radius: 6px;
  padding: 0.5rem;
  margin-top: 0.5rem;
  font-size: 1rem;
}
.export-btn {
  background: #10b981;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.7rem 1.5rem;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.export-btn:hover {
  background: #047857;
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
  .business-profile-slideout {
    width: 100vw;
    min-width: 0;
    max-width: 100vw;
    padding: 0;
  }
}
</style>
