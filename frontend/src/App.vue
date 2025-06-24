<template>
  <div id="app">
    <!-- Main App Background -->
    <div class="fake-main-app">
      <h1>Business Profile Tool Demo</h1>
      <div class="main-content-blocks">
        <div class="block">Other Widget 1</div>
        <div class="block">Other Widget 2</div>
      </div>
      <button class="open-profile-tool-btn" @click="showProfileTool = true">
        Open Business Profile Tool
      </button>
    </div>
    <!-- Slide-out Business Profile Tool Panel -->
    <BusinessProfileSlideout
      :open="showProfileTool"
      @close="showProfileTool = false"
    />
    <div
      v-if="showProfileTool"
      class="slideout-overlay"
      @click="showProfileTool = false"
    />
  </div>
</template>

<script>
import BusinessProfileSlideout from "./features/businessProfileComparator/components/BusinessProfileSlideout.vue";

export default {
  name: "App",
  components: { BusinessProfileSlideout },
  data() {
    return {
      showProfileTool: false,
    };
  },
};
</script>
