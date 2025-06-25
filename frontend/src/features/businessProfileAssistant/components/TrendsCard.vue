<template>
  <section v-if="trends && trends.length" class="main-section card-modern">
    <h2 class="main-title">Local Market Trends</h2>
    <ul class="trends-list">
      <li v-for="trend in trends" :key="trend">{{ trend }}</li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  trends: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.trends-list {
  margin: 0;
  padding: 0 0 0 1.2em;
  list-style: disc;
  color: #222;
  font-size: 1.06em;
}
.trends-list li {
  margin-bottom: 0.4em;
  line-height: 1.5;
}
</style>
