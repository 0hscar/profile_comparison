<template>
  <section
    class="sidebar-section card-modern"
    v-if="competitors && competitors.length"
  >
    <h2 class="sidebar-title card-title-modern">Competitors</h2>
    <div class="competitor-list card-content-modern">
      <div
        v-for="comp in competitors"
        :key="comp.id || comp.name"
        class="competitor-item"
      >
        <div class="competitor-header">
          <a
            v-if="comp.website"
            :href="comp.website"
            target="_blank"
            rel="noopener"
            class="competitor-name"
          >
            {{ comp.name }}
          </a>
          <span v-else class="competitor-name">{{ comp.name }}</span>
          <span class="competitor-rating" v-if="comp.rating">
            {{ comp.rating }} ★
          </span>
          <span class="competitor-rating" v-else> N/A </span>
        </div>
        <div class="competitor-category" v-if="comp.category">
          {{ comp.category }}
        </div>
        <div class="competitor-address" v-if="comp.address">
          {{ comp.address }}
        </div>
        <button class="compare-btn" @click="$emit('compare', comp)">
          Compare
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  competitors: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.competitor-list {
  display: flex;
  flex-direction: column;
  gap: 1em;
  margin-top: 0.5em;
}

.competitor-item {
  background: #f7fafd;
  border-radius: 10px;
  padding: 1em 1.2em;
  margin-bottom: 0.2em;
  box-shadow: 0 1px 4px #2d8cf005;
  display: flex;
  flex-direction: column;
  gap: 0.3em;
}

.competitor-header {
  display: flex;
  align-items: center;
  gap: 0.7em;
  font-weight: 600;
  font-size: 1.08em;
}

.competitor-name {
  color: #2d8cf0;
  text-decoration: none;
  font-weight: 700;
}

.competitor-rating {
  color: #f7b801;
  font-size: 1em;
  margin-left: 0.5em;
}

.competitor-category,
.competitor-address {
  color: #888;
  font-size: 0.98em;
}

.compare-btn {
  margin-top: 0.5em;
  background: #2d8cf0;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4em 1em;
  cursor: pointer;
  font-size: 0.98em;
  transition: background 0.2s;
}
.compare-btn:hover {
  background: #1761a0;
}
</style>
