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

.open-profile-tool-btn {
  position: fixed;
  right: 2.5rem;
  bottom: 2.5rem;
  z-index: 1100;
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
.open-profile-tool-btn:hover {
  background: #1761a0;
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
</style>
