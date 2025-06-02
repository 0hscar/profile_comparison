<template>
  <div class="sidebar-content">
    <div v-if="defaultUserBusiness" class="sidebar-sticky-controls">
      <RestaurantCard
        :card="defaultUserBusiness"
        :isUser="true"
        :showDirectCompare="false"
      />
      <h2 style="margin-top: 0.5rem; text-align: center">
        {{ showNearby ? "Nearby Restaurants" : "Similar Restaurants" }}
      </h2>
      <div class="toggle-group" style="margin-top: 1rem; margin-bottom: 1rem">
        <button
          :class="['toggle-btn', { active: showNearby }]"
          @click="$emit('toggle', 'nearby')"
          type="button"
        >
          Nearby
        </button>
        <button
          :class="['toggle-btn', { active: !showNearby }]"
          @click="$emit('toggle', 'similar')"
          type="button"
        >
          Similar
        </button>
      </div>
    </div>
    <transition name="slide" mode="out-in">
      <div :key="showNearby ? 'nearby' : 'similar'">
        <template v-if="(showNearby ? defaultNearby : defaultSimilar).length">
          <RestaurantCard
            v-for="(card, idx) in showNearby ? defaultNearby : defaultSimilar"
            :key="card.place_id || card.title || idx"
            :card="card"
            :isUser="false"
            :showDirectCompare="true"
            :userBusinessName="userBusinessName"
            :userBusinessLocation="userBusinessLocation"
            @comparison-result="$emit('comparison-result', $event)"
          />
        </template>
        <template v-else>
          <div class="loading">
            <div class="spinner"></div>
            <p>
              Loading
              {{ showNearby ? "nearby" : "similar" }} restaurants...
            </p>
          </div>
        </template>
      </div>
    </transition>
  </div>
</template>

<script>
import RestaurantCard from "./RestaurantCard.vue";
export default {
  name: "SidebarRestaurantList",
  components: { RestaurantCard },
  props: {
    defaultUserBusiness: Object,
    defaultNearby: Array,
    defaultSimilar: Array,
    showNearby: Boolean,
    userBusinessName: String,
    userBusinessLocation: String,
  },
};
</script>
