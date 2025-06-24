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
        <BadgesCard
          v-if="profileData.selectedBusiness.value"
          :badges="profileData.gamification.value.badges"
        />
        <!-- Competitor List Enhanced -->
        <CompetitorsCard
          v-if="profileData.selectedBusiness.value"
          :competitors="profileData.competitorList.value"
          @compare="chatAssistant.insertCompetitorPrompt"
        />
      </aside>
      <!-- Main Content: Profile Analysis & AI Features -->
      <main class="main-content">
        <!-- Combined Profile Info & Health -->
        <ProfileCard
          v-if="profileData.selectedBusiness.value"
          :profile="profileData.selectedBusiness.value"
          :gamification="profileData.gamification.value"
          @edit-profile="goToEditProfile"
        />
        <!-- Unified AI Chat -->
        <AIChatAssistant
          v-if="profileData.selectedBusiness.value"
          :show="true"
          :chat-history="chatAssistant.chatHistory.value"
          :chat-input-prop="chatAssistant.chatInput.value"
          :loading="chatAssistant.loading.value"
          @update:chatInputProp="(val) => (chatAssistant.chatInput.value = val)"
          @send="chatAssistant.sendChat"
        />
        <!-- Local Market Trends -->
        <TrendsCard
          v-if="profileData.localTrends.value.length"
          :trends="profileData.localTrends.value"
        />
        <!-- Photo Insights -->
        <PhotoInsightsCard
          v-if="profileData.photoInsights.value.length"
          :insights="profileData.photoInsights.value"
        />
        <!-- Competitor Alerts -->
        <CompetitorAlertsCard
          v-if="profileData.competitorAlerts.value.length"
          :alerts="profileData.competitorAlerts.value"
        />
        <!-- Profile History (Toggleable) -->
        <ProfileHistoryCard
          v-if="profileData.selectedBusiness.value"
          :history="profileData.profileHistory.value"
        />

        <!-- Snapshot Export -->
        <section v-if="profileData.selectedBusiness.value" class="main-section">
          <button class="export-btn" @click="profileData.exportSnapshot">
            Download Snapshot Report
          </button>
        </section>
      </main>
    </div>
  </div>
  <div v-if="open" class="slideout-overlay" @click="$emit('close')" />
</template>

<script setup>
import { onMounted } from "vue";
import BadgesCard from "./BadgesCard.vue";
import CompetitorsCard from "./CompetitorsCard.vue";
import ProfileCard from "./ProfileCard.vue";
import AIChatAssistant from "./AIChatAssistant.vue";
import TrendsCard from "./TrendsCard.vue";
import PhotoInsightsCard from "./PhotoInsightsCard.vue";
import ProfileHistoryCard from "./ProfileHistoryCard.vue";
import CompetitorAlertsCard from "./CompetitorAlertsCard.vue";
import { useProfileData } from "../composables/useProfileData";
import { useChatAssistant } from "../composables/useChatAssistant";

// Slideout open/close prop
defineProps({
  open: { type: Boolean, required: true },
});

// Use the whole composable object (no destructuring) to preserve Vue reactivity for all refs and avoid subtle bugs.
const profileData = useProfileData();
const chatAssistant = useChatAssistant();

onMounted(async () => {
  await profileData.fetchAllProfileData();
  await profileData.fetchCompetitorProfiles();
});
function goToEditProfile() {
  // Replace with your actual navigation logic, e.g. router.push or emit event
  window.location.href = "/edit-profile";
}
</script>

<style scoped>
.business-profile-slideout {
  position: fixed;
  top: 0;
  right: 0;
  width: clamp(960px, 75vw, 100vw);
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
</style>
