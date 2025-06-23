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
      <h1>Profile & Assistant</h1>
    </div>
    <div class="dashboard-layout">
      <!-- Sidebar: Business Search & Competitor List -->
      <aside class="sidebar">
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
        <!-- Competitor List Enhanced -->
        <section class="sidebar-section" v-if="selectedBusiness">
          <h2 class="sidebar-title">Competitors</h2>
          <div class="competitor-list">
            <div
              v-for="comp in competitorList"
              :key="comp.id || comp.name"
              class="competitor-item"
            >
              <div class="competitor-header">
                <a
                  v-if="comp.website"
                  :href="comp.website"
                  target="_blank"
                  rel="noopener"
                  class="competitor-name"
                >
                  {{ comp.name }}
                </a>
                <span v-else class="competitor-name">{{ comp.name }}</span>
                <span class="competitor-rating" v-if="comp.rating">
                  {{ comp.rating }} ★
                </span>
                <span class="competitor-rating" v-else> N/A </span>
              </div>
              <div class="competitor-category" v-if="comp.category">
                {{ comp.category }}
              </div>
              <div class="competitor-address" v-if="comp.address">
                {{ comp.address }}
              </div>
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
        <!-- Unified AI Chat -->
        <section v-if="selectedBusiness" class="main-section">
          <h2 class="main-title">AI Chat Assistant</h2>
          <div class="gpt-chat-history">
            <div
              v-for="(msg, idx) in chatHistory"
              :key="idx"
              :class="[
                'gpt-message',
                msg.role === 'user'
                  ? 'gpt-user'
                  : msg.system
                  ? 'gpt-system'
                  : 'gpt-assistant',
              ]"
            >
              <div v-if="msg.system" class="gpt-system-bubble">
                {{ msg.content }}
              </div>
              <div
                v-else-if="msg.role === 'assistant'"
                class="gpt-assistant-bubble"
              >
                {{ msg.content }}
              </div>
              <div v-else-if="msg.role === 'user'" class="gpt-user-bubble">
                {{ msg.content }}
              </div>
            </div>
          </div>
          <form class="gpt-chat-input-row" @submit.prevent="sendChat">
            <input
              v-model="chatInput"
              type="text"
              placeholder="Send a message..."
              class="gpt-chat-input"
              autocomplete="off"
            />
            <button
              class="gpt-chat-send-btn"
              :disabled="loading || !chatInput.trim()"
            >
              <span v-if="!loading">Send</span>
              <span v-else>...</span>
            </button>
          </form>
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
const competitorList = ref([]);
const gamification = ref({ score: 0, badges: [] });
const competitorHighlights = ref([]);
const localTrends = ref([]);
const photoInsights = ref([]);
const profileHistory = ref([]);
const competitorAlerts = ref([]);
const loading = ref(false);

// Unified AI Chat State
const chatHistory = ref([
  {
    role: "assistant",
    content:
      '👋 Welcome! I\'m your Business Profile AI Assistant. You can ask me to help with things like generating social media post captions, simulating the effect of profile changes, analyzing competitors, or getting tips to improve your business profile. Try asking something like: "Write a catchy Instagram caption for my restaurant", "What would happen if I added 10 more photos?", or "How can I improve my Google ranking?"',
    system: true,
  },
]);
const chatInput = ref("");

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
    // fallback for demo: if backend doesn't provide, keep empty
    // No longer injecting AI suggestions into chat history
  } catch (e) {
    selectedBusiness.value = null;
  }
  loading.value = false;
}

async function fetchCompetitorProfiles() {
  try {
    const competitors = await api.fetchCompetitorsProfiles();
    // Ensure competitors is always an array
    const competitorArray = Array.isArray(competitors)
      ? competitors
      : competitors
      ? Object.values(competitors)
      : [];
    competitorList.value = competitorArray.filter(
      (comp) => comp.name && comp.address
    );
  } catch (e) {
    competitorList.value = [];
  }
}

function exportSnapshot() {
  // TODO: Implement snapshot export (e.g., html2pdf)
}

// Unified AI Chat send logic
async function sendChat() {
  const input = chatInput.value.trim();
  if (!input) return;
  chatHistory.value.push({ role: "user", content: input });
  chatInput.value = "";
  loading.value = true;

  // Add a placeholder for the assistant's streaming response
  chatHistory.value.push({ role: "assistant", content: "" });

  try {
    await api.streamProfileAssistant(input, (chunk, fullText) => {
      // Update the last assistant message as the stream progresses
      const lastMsg = chatHistory.value[chatHistory.value.length - 1];
      if (lastMsg && lastMsg.role === "assistant") {
        lastMsg.content = fullText;
      }
    });
  } catch (e) {
    const lastMsg = chatHistory.value[chatHistory.value.length - 1];
    if (lastMsg && lastMsg.role === "assistant") {
      lastMsg.content = "Sorry, I couldn't process your request.";
    }
  }
  loading.value = false;
}

onMounted(async () => {
  await fetchAllProfileData();
  await fetchCompetitorProfiles();
});
</script>

<style scoped>
.gpt-chat-history {
  background: #f7f7fa;
  border-radius: 12px;
  padding: 2em 1.5em 1em 1.5em;
  margin-bottom: 1.5em;
  max-height: 600px;
  min-height: 350px;
  overflow-y: auto;
  border: 1px solid #e6eaf0;
  display: flex;
  flex-direction: column;
  gap: 1.2em;
}
.gpt-message {
  display: flex;
  flex-direction: row;
  margin-bottom: 0;
}
.gpt-user {
  justify-content: flex-end;
}
.gpt-user-bubble {
  background: #e6f0fa;
  color: #1a2b3c;
  border-radius: 12px 12px 4px 12px;
  padding: 0.9em 1.2em;
  margin-left: auto;
  max-width: 70%;
  font-size: 1.08em;
  box-shadow: 0 1px 2px #0001;
}
.gpt-assistant {
  justify-content: flex-start;
}
.gpt-assistant-bubble {
  background: #fff;
  color: #222;
  border-radius: 12px 12px 12px 4px;
  padding: 0.9em 1.2em;
  margin-right: auto;
  max-width: 70%;
  font-size: 1.08em;
  box-shadow: 0 1px 2px #0001;
}
.gpt-system {
  justify-content: center;
  width: 100%;
}
.gpt-system-bubble {
  background: #f3f3f6;
  color: #888;
  border-radius: 8px;
  padding: 0.8em 1.1em;
  margin: 0 auto;
  font-size: 1.05em;
  text-align: center;
  max-width: 80%;
  box-shadow: 0 1px 2px #0001;
}
.gpt-chat-input-row {
  display: flex;
  gap: 0.7em;
  margin-top: 1em;
  align-items: center;
}
.gpt-chat-input {
  flex: 1;
  padding: 1em;
  border-radius: 8px;
  border: 1px solid #e6eaf0;
  font-size: 1.08em;
  background: #f7f7fa;
  transition: border 0.2s;
}
.gpt-chat-input:focus {
  border: 1.5px solid #1761a0;
  outline: none;
}
.gpt-chat-send-btn {
  background: #1761a0;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.8em 1.6em;
  font-size: 1.08em;
  cursor: pointer;
  transition: background 0.2s;
  font-weight: 600;
}
.gpt-chat-send-btn:disabled {
  background: #b0b8c1;
  cursor: not-allowed;
}
</style>

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
  margin-top: 2em;
}

.competitor-item {
  margin-bottom: 1.5em;
  padding-bottom: 1em;
  border-bottom: 1px solid #eee;
}

.competitor-header {
  display: flex;
  align-items: center;
  gap: 0.5em;
  font-weight: 500;
}

.competitor-name {
  color: #2a5db0;
  text-decoration: none;
  font-weight: 600;
}

.competitor-name:hover {
  text-decoration: underline;
}

.competitor-rating {
  color: #f5b301;
  font-size: 0.95em;
  margin-left: 0.5em;
}

.competitor-category {
  font-size: 0.95em;
  color: #666;
  margin-top: 0.1em;
}

.competitor-address {
  font-size: 0.93em;
  color: #888;
  margin-top: 0.1em;
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
