<template>
  <section v-if="insights && insights.length" class="main-section card-modern">
    <h2 class="main-title">Photo Insights</h2>
    <ul class="photo-insights-list">
      <li v-for="insight in insights" :key="insight">
        {{ insight }}
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  insights: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.photo-insights-list {
  margin: 0;
  padding: 0 0 0 1.2em;
  list-style: disc;
  color: #222;
  font-size: 1.06em;
}
.photo-insights-list li {
  margin-bottom: 0.4em;
  line-height: 1.5;
}
</style>
