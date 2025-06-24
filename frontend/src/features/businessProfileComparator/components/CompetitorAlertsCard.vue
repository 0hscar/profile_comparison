<template>
  <section v-if="alerts && alerts.length" class="main-section card-modern">
    <h2 class="main-title">Competitor Alerts</h2>
    <ul class="alerts-list">
      <li v-for="alert in alerts" :key="alert">{{ alert }}</li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  alerts: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.alerts-list {
  list-style: disc inside;
  padding-left: 1rem;
  color: #222;
  font-size: 1.06em;
}
.alerts-list li {
  margin-bottom: 0.4em;
  line-height: 1.5;
}
</style>
