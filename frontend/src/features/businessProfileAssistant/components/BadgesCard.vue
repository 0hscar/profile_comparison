<template>
  <section class="sidebar-section card-modern" v-if="badges && badges.length">
    <h2 class="sidebar-title card-title-modern">Badges</h2>
    <div class="badges-list card-content-modern">
      <BadgeCard v-for="badge in badges" :key="badge.name" :badge="badge" />
    </div>
  </section>
</template>

<script setup>
import BadgeCard from "./BadgeCard.vue";

defineProps({
  badges: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.badges-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1em;
  margin-top: 0.5em;
}
</style>
