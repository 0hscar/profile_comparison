<template>
  <div
    class="comparator-slideout"
    :class="{ open: open }"
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
        @click="$emit('close')"
        >&times;</AppButton
      >
      <h1>Business Profile Comparator</h1>
    </div>
    <div class="dashboard-layout">
      <aside class="sidebar">
        <SidebarRestaurantList
          :defaultUserBusiness="defaultUserBusiness"
          :defaultNearby="defaultNearby"
          :defaultSimilar="defaultSimilar"
          :showNearby="showNearby"
          :userBusinessName="userBusinessName"
          :userBusinessLocation="userBusinessLocation"
          @toggle="$emit('toggle-restaurant-group', $event)"
          @comparison-result="$emit('comparison-result', $event)"
        />
      </aside>
      <main class="main-content">
        <InputForm
          @comparison-result="$emit('comparison-result', $event)"
          @reset="$emit('reset')"
          :userBusinessName="userBusinessName"
          :userBusinessLocation="userBusinessLocation"
          @set-loading="$emit('set-loading', $event)"
        />
        <ProfileResults
          v-if="
            userProfile ||
            (competitorProfiles && competitorProfiles.length) ||
            isLoading
          "
          :userProfile="userProfile"
          :competitorProfiles="competitorProfiles"
          :comparison="comparison"
          :suggestions="suggestions"
          :extraInsights="extraInsights"
          :isLoading="isLoading"
          @reset="$emit('reset')"
        />
      </main>
    </div>
  </div>
  <div v-if="open" class="slideout-overlay" @click="$emit('close')"></div>
</template>

<script>
import AppButton from "./AppButton.vue";
import SidebarRestaurantList from "./SidebarRestaurantList.vue";
import InputForm from "./InputForm.vue";
import ProfileResults from "./Results.vue";

export default {
  name: "ComparatorSlideout",
  components: {
    AppButton,
    SidebarRestaurantList,
    InputForm,
    ProfileResults,
  },
  props: {
    open: { type: Boolean, required: true },
    defaultUserBusiness: { type: Object, default: null },
    defaultNearby: { type: Array, default: () => [] },
    defaultSimilar: { type: Array, default: () => [] },
    showNearby: { type: Boolean, default: true },
    userBusinessName: { type: String, default: "" },
    userBusinessLocation: { type: String, default: "" },
    userProfile: { type: [Object, Array], default: null },
    competitorProfiles: { type: Array, default: () => [] },
    comparison: { type: [Object, Array], default: null },
    suggestions: { type: Object, default: null },
    extraInsights: { type: Object, default: null },
    isLoading: { type: Boolean, default: false },
  },
};
</script>

<style scoped>
.comparator-slideout {
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
    max-width: 100vw;
    padding: 0;
  }
}
</style>
