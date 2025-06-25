<template>
  <section class="competitor-list-section card-modern">
    <h2 class="sidebar-title card-title-modern">Competitors</h2>
    <div class="competitor-toggle">
      <button
        :class="{ active: mode === 'nearby' }"
        type="button"
        @click="setMode('nearby')"
      >
        Nearby
      </button>
      <button
        :class="{ active: mode === 'similar' }"
        type="button"
        @click="setMode('similar')"
      >
        Similar
      </button>
    </div>
    <transition :name="slideDirection" mode="out-in">
      <CompetitorsCard
        :key="mode"
        :competitors="competitors"
        @compare="$emit('compare', $event)"
      />
    </transition>
  </section>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import CompetitorsCard from "./CompetitorsCard.vue";

const props = defineProps({
  nearbyCompetitors: {
    type: Array,
    required: true,
  },
  similarCompetitors: {
    type: Array,
    required: true,
  },
  mode: {
    type: String,
    default: "nearby", // 'nearby' or 'similar'
  },
});
const emit = defineEmits(["update:mode", "compare"]);

const competitors = computed(() =>
  props.mode === "similar" ? props.similarCompetitors : props.nearbyCompetitors
);

// Track previous mode to determine slide direction
const prevMode = ref(props.mode);
const slideDirection = ref("slide-right");

watch(
  () => props.mode,
  (newMode, oldMode) => {
    if (oldMode === "nearby" && newMode === "similar") {
      slideDirection.value = "slide-left";
    } else if (oldMode === "similar" && newMode === "nearby") {
      slideDirection.value = "slide-right";
    }
    prevMode.value = newMode;
  }
);

function setMode(newMode) {
  if (newMode !== props.mode) {
    emit("update:mode", newMode);
  }
}
</script>

<style scoped>
.competitor-list-section {
  padding-bottom: 1em;
}

/* Slide left/right transitions */
.slide-left-enter-active,
.slide-left-leave-active {
  transition: transform 0.35s cubic-bezier(0.77, 0, 0.18, 1), opacity 0.35s;
}
.slide-left-enter-from {
  transform: translateX(100%);
  opacity: 0;
}
.slide-left-enter-to {
  transform: translateX(0%);
  opacity: 1;
}
.slide-left-leave-from {
  transform: translateX(0%);
  opacity: 1;
}
.slide-left-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.35s cubic-bezier(0.77, 0, 0.18, 1), opacity 0.35s;
}
.slide-right-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}
.slide-right-enter-to {
  transform: translateX(0%);
  opacity: 1;
}
.slide-right-leave-from {
  transform: translateX(0%);
  opacity: 1;
}
.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.competitor-toggle {
  display: flex;
  gap: 0.5em;
  margin-bottom: 1em;
}

.competitor-toggle button {
  background: #f7f7fa;
  border: 1.5px solid #e6eaf0;
  color: #1761a0;
  border-radius: 6px;
  padding: 0.4em 1.2em;
  font-size: 1em;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s, border 0.2s, color 0.2s;
}

.competitor-toggle button.active,
.competitor-toggle button:focus {
  background: #1761a0;
  color: #fff;
  border: 1.5px solid #1761a0;
  outline: none;
}
</style>
