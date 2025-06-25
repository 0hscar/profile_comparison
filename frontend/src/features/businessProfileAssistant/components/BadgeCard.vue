<template>
  <div
    class="badge-card flex flex-col items-center justify-center bg-white border rounded shadow px-4 py-2 min-w-[100px] min-h-[100px] m-1"
    :class="{ 'opacity-50 grayscale': !badge.unlocked }"
  >
    <div class="text-3xl mb-1">
      <span v-if="badge.icon">{{ badge.icon }}</span>
      <span v-else>🏅</span>
    </div>
    <div class="font-semibold text-center">
      {{ badge.name }}
    </div>
    <div
      v-if="badge.description"
      class="text-xs text-gray-500 text-center"
    >
      {{ badge.description }}
    </div>
    <div
      v-if="!badge.unlocked"
      class="text-xs text-red-400 mt-1"
    >
      Locked
    </div>
  </div>
</template>

<script setup>
defineProps({
  badge: {
    type: Object,
    required: true,
    // badge: { name: String, description: String, icon: String, unlocked: Boolean }
  },
});
</script>

<style scoped>
.badge-card {
  transition: filter 0.2s, opacity 0.2s;
}
</style>
