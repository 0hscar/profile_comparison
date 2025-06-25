<template>
  <section class="main-section card-modern" v-if="historyAvailable">
    <div
      class="toggle-header"
      @click="toggle"
      style="cursor: pointer; display: flex; align-items: center; justify-content: space-between;"
    >
      <h2 class="main-title" style="margin: 0">Profile History</h2>
      <span style="font-size: 1.3em">{{ show ? "▲" : "▼" }}</span>
    </div>
    <transition name="fade">
      <div v-if="show">
        <ul class="history-list" v-if="history && history.length">
          <li v-for="entry in history" :key="entry.date">
            {{ entry.date }} - Score: {{ entry.score }}% | Photos: {{ entry.photos }} | Reviews: {{ entry.reviews }}
          </li>
        </ul>
        <div v-else style="color: #888; padding: 1em 0 0 0">
          No history from mock data
        </div>
      </div>
    </transition>
  </section>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  history: {
    type: Array,
    required: false,
    default: () => []
  }
});

const show = ref(false);

function toggle() {
  show.value = !show.value;
}

const historyAvailable = computed(() => Array.isArray(props.history));
</script>

<style scoped>
.history-list {
  margin: 0;
  padding: 0 0 0 1.2em;
  list-style: disc;
  color: #222;
  font-size: 1.06em;
}
.history-list li {
  margin-bottom: 0.4em;
  line-height: 1.5;
}
.toggle-header {
  user-select: none;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
