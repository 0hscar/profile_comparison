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
        <!-- Gamification Badges -->
        <section class="sidebar-section card-modern" v-if="selectedBusiness">
          <h2 class="sidebar-title card-title-modern">Badges</h2>
          <div class="badges-list card-content-modern">
            <BadgeCard
              v-for="badge in gamification.badges"
              :key="badge.name"
              :badge="badge"
            />
          </div>
        </section>
        <!-- Competitor List Enhanced -->
        <section class="sidebar-section card-modern" v-if="selectedBusiness">
          <h2 class="sidebar-title card-title-modern">Competitors</h2>
          <div class="competitor-list card-content-modern">
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
              <button class="compare-btn" @click="insertCompetitorPrompt(comp)">
                Compare
              </button>
            </div>
          </div>
        </section>
      </aside>
      <!-- Main Content: Profile Analysis & AI Features -->
      <main class="main-content">
        <!-- Combined Profile Info & Health -->
        <section
          v-if="selectedBusiness"
          class="main-section card-modern profile-card-gap"
        >
          <div class="profile-card-header">
            <h2 class="main-title card-title-modern">Profile</h2>
            <button
              class="profile-cog-btn"
              @click="goToEditProfile"
              aria-label="Edit Profile"
            >
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                <circle
                  cx="11"
                  cy="11"
                  r="10"
                  fill="#f5f8fa"
                  stroke="#b0b8c1"
                  stroke-width="1"
                />
                <path
                  d="M11 7.5A3.5 3.5 0 1 1 7.5 11 3.5 3.5 0 0 1 11 7.5m0-1.5a5 5 0 1 0 5 5 5 5 0 0 0-5-5zm0 7.5a2.5 2.5 0 1 1 2.5-2.5A2.5 2.5 0 0 1 11 13.5z"
                  fill="#2d8cf0"
                />
                <path
                  d="M11 4v2M11 16v2M4 11h2M16 11h2M6.22 6.22l1.42 1.42M14.36 14.36l1.42 1.42M6.22 15.78l1.42-1.42M14.36 7.64l1.42-1.42"
                  stroke="#2d8cf0"
                  stroke-width="1.2"
                  stroke-linecap="round"
                />
              </svg>
            </button>
          </div>
          <div class="sidebar-business-info card-content-modern">
            <div class="info-row">
              <span class="info-label">Name:</span>
              <span class="info-value">{{ selectedBusiness.name }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Address:</span>
              <span class="info-value">{{ selectedBusiness.address }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Phone:</span>
              <span class="info-value">{{ selectedBusiness.phone }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Website:</span>
              <span class="info-value">
                <a :href="selectedBusiness.website" target="_blank">{{
                  selectedBusiness.website
                }}</a>
              </span>
            </div>
            <div class="info-row">
              <span class="info-label">Category:</span>
              <span class="info-value">{{ selectedBusiness.category }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Price Level:</span>
              <span class="info-value">{{ selectedBusiness.priceLevel }}</span>
            </div>
          </div>
          <div class="profile-health-header">
            <span class="profile-health-score-label">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle
                  cx="12"
                  cy="12"
                  r="12"
                  fill="#2d8cf0"
                  fill-opacity="0.12"
                />
                <path
                  d="M7 13.5L10.5 17L17 10.5"
                  stroke="#2d8cf0"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              Health Score
            </span>
            <span class="profile-health-score-value"
              >{{ gamification.score }}%</span
            >
          </div>
          <div class="profile-health-bar-outer">
            <div
              class="profile-health-bar-inner"
              :style="{ width: gamification.score + '%' }"
            ></div>
          </div>
          <div v-if="gamification.score === 100" class="score-complete-modern">
            🎉 Your profile is fully optimized! Keep it fresh for ongoing
            rewards.
          </div>
          <div class="profile-health-stats-row">
            <div class="profile-health-stat">
              <span class="stat-label">Rating</span>
              <span class="stat-value">
                {{ selectedBusiness && selectedBusiness.rating }}
                <span
                  v-if="selectedBusiness && selectedBusiness.review_count"
                  class="stat-sub"
                  >({{ selectedBusiness.review_count }} reviews)</span
                >
              </span>
            </div>
            <div class="profile-health-stat">
              <span class="stat-label">Recent Reviews</span>
              <span class="stat-value">
                {{ selectedBusiness && selectedBusiness.recentReviews }}
                <span class="stat-sub">(last 3 months)</span>
              </span>
            </div>
            <div class="profile-health-stat">
              <span class="stat-label">Photos</span>
              <span class="stat-value">{{
                selectedBusiness && selectedBusiness.photoCount
              }}</span>
            </div>
            <div class="profile-health-stat">
              <span class="stat-label">Menu</span>
              <span class="stat-value">
                <a
                  v-if="selectedBusiness && selectedBusiness.menuAvailable"
                  :href="selectedBusiness && selectedBusiness.menuUrl"
                  target="_blank"
                  >View Menu</a
                >
                <span v-else>No menu online</span>
              </span>
            </div>
            <div class="profile-health-stat">
              <span class="stat-label">Completeness</span>
              <span class="stat-value"
                >{{
                  selectedBusiness && selectedBusiness.profileCompleteness
                }}%</span
              >
            </div>
            <div class="profile-health-stat">
              <span class="stat-label">Last Update</span>
              <span class="stat-value">{{
                selectedBusiness && selectedBusiness.lastProfileUpdate
              }}</span>
            </div>
          </div>
        </section>
        <!-- Unified AI Chat -->
        <section
          v-if="selectedBusiness"
          class="main-section card-modern ai-chat-modern"
        >
          <h2 class="main-title card-title-modern">AI Chat Assistant</h2>
          <div class="gpt-chat-history card-content-modern">
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
            <textarea
              v-model="chatInput"
              placeholder="Send a message..."
              class="gpt-chat-input gpt-chat-textarea"
              autocomplete="off"
              rows="1"
              @input="autoGrowChatInput"
              ref="chatInputRef"
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
import { ref, onMounted, nextTick } from "vue";
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
const chatInputRef = ref(null);

function autoGrowChatInput() {
  nextTick(() => {
    const el = chatInputRef.value;
    if (el) {
      el.style.height = "auto";
      el.style.overflowY = "hidden";
      el.style.height = el.scrollHeight + "px";
      if (el.scrollHeight > 160) {
        // ~8 lines
        el.style.overflowY = "auto";
        el.style.height = "160px";
      }
    }
  });
}

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

function insertCompetitorPrompt(comp) {
  const prompt = `Compare my business profile with the following competitor:

Name: ${comp.name}
Address: ${comp.address || "Not found"}
Category: ${comp.category || "Not found"}
Price: ${comp.price_level || "Not found"}
Rating: ${comp.rating || "Not found"}
Rating Count: ${comp.review_count || "Not found"}
Hours: ${comp.hours || "Not found"}
Phone: ${comp.phone || "Not found"}
Menu: ${comp.menu_url || "Not found"}
Website: ${comp.website || "Not found"}
Description: ${comp.description || "Not found"}
Photos: ${comp.photos || "Not found"}

Highlight key differences and similarities. Give actionable suggestions to improve my profile based on this competitor.`;
  chatInput.value = prompt;
  autoGrowChatInput();
}

onMounted(async () => {
  await fetchAllProfileData();
  await fetchCompetitorProfiles();
});
function goToEditProfile() {
  // Replace with your actual navigation logic, e.g. router.push or emit event
  window.location.href = "/edit-profile";
}
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
  resize: none;
  min-height: 2.5em;
  max-height: 160px;
  overflow-y: auto;
  line-height: 1.5;
  box-sizing: border-box;
}
.gpt-chat-input:focus {
  border: 1.5px solid #1761a0;
  outline: none;
}
.gpt-chat-textarea {
  width: 100%;
  font-family: inherit;
  display: block;
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

/* --- Modern Card Styles for Sidebar/Main Sections --- */
.card-modern {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px #2d8cf01a, 0 1.5px 6px #0001;
  padding: 1.5em 1.3em 1.2em 1.3em;
  margin-bottom: 1.5em;
  display: flex;
  flex-direction: column;
  gap: 0.7em;
  align-items: stretch;
}

.profile-card-gap {
  margin-top: 1.5em;
}

.profile-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.profile-cog-btn {
  background: none;
  border: none;
  box-shadow: none;
  padding: 0.1em;
  margin: 0;
  cursor: pointer;
  position: absolute;
  top: 0.2em;
  right: 0.2em;
  z-index: 2;
  display: flex;
  align-items: center;
  transition: background 0.2s;
}

.profile-cog-btn:focus {
  outline: 2px solid #2d8cf0;
}

.profile-cog-btn svg {
  display: block;
}
.card-title-modern {
  font-size: 1.18rem;
  font-weight: 700;
  color: #2d8cf0;
  margin-bottom: 0.7em;
  letter-spacing: 0.01em;
}
.card-content-modern {
  display: flex;
  flex-direction: column;
  gap: 0.7em;
}
.ai-chat-modern {
  padding: 2em 2em 1.5em 2em;
}
/* Business Info Row Styling */
.info-row {
  display: flex;
  gap: 0.7em;
  margin-bottom: 0.2em;
}
.info-label {
  color: #888;
  font-size: 0.98em;
  font-weight: 500;
  min-width: 90px;
  display: inline-block;
}
.info-value {
  color: #222;
  font-size: 1.08em;
  font-weight: 600;
  word-break: break-word;
}

/* --- Modern Profile Health Card Styles --- */
.profile-health-modern {
  padding: 0;
  margin-bottom: 2.5rem;
}

.profile-health-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px #2d8cf01a, 0 1.5px 6px #0001;
  padding: 2.2em 2em 1.5em 2em;
  margin-top: 1.2em;
  margin-bottom: 1.2em;
  display: flex;
  flex-direction: column;
  gap: 1.5em;
  align-items: stretch;
}

.profile-health-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.7em;
}

.profile-health-score-label {
  display: flex;
  align-items: center;
  gap: 0.5em;
  font-weight: 600;
  color: #2d8cf0;
  font-size: 1.1em;
  letter-spacing: 0.01em;
}

.profile-health-score-value {
  font-size: 1.5em;
  font-weight: 700;
  color: #222;
  letter-spacing: -0.01em;
}

.profile-health-bar-outer {
  width: 100%;
  height: 18px;
  background: #e6eaf0;
  border-radius: 9px;
  overflow: hidden;
  margin-bottom: 0.7em;
  box-shadow: 0 1px 4px #2d8cf005;
}

.profile-health-bar-inner {
  height: 100%;
  background: linear-gradient(90deg, #2d8cf0 60%, #5ad1e6 100%);
  border-radius: 9px 0 0 9px;
  transition: width 0.5s cubic-bezier(0.77, 0, 0.18, 1);
}

.score-complete-modern {
  background: #e6f9e6;
  color: #1a7f37;
  border-radius: 8px;
  padding: 0.7em 1em;
  font-size: 1.05em;
  margin-bottom: 0.7em;
  display: flex;
  align-items: center;
  gap: 0.5em;
}

.profile-health-stats-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5em 2.5em;
  margin-top: 0.5em;
}

.profile-health-stat {
  min-width: 140px;
  flex: 1 1 140px;
  display: flex;
  flex-direction: column;
  gap: 0.15em;
  margin-bottom: 0.5em;
}

.stat-label {
  color: #888;
  font-size: 0.98em;
  font-weight: 500;
  margin-bottom: 0.1em;
}

.stat-value {
  color: #222;
  font-size: 1.08em;
  font-weight: 600;
  word-break: break-word;
}

.stat-sub {
  color: #b0b8c1;
  font-size: 0.93em;
  font-weight: 400;
  margin-left: 0.3em;
}

.compare-btn {
  margin-top: 0.5em;
  background: #2d8cf0;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4em 1em;
  cursor: pointer;
  font-size: 0.98em;
  transition: background 0.2s;
}
.compare-btn:hover {
  background: #1761a0;
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
