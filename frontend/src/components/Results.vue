<template>
  <div v-if="results" class="results-container">
    <!-- Restaurant Cards (Search Results) -->
    <div v-if="results.cards && results.cards.length">
      <h2>Restaurants</h2>
      <div>
        <RestaurantCard
          v-for="(card, idx) in results.cards"
          :key="card.place_id || card.title || idx"
          :card="card"
          :isUser="idx === 0"
        />
      </div>
    </div>

    <h2>Comparison Summary</h2>
    <div class="summary">
      <p v-if="results.suggestions.ai_summary">{{ results.suggestions.ai_summary }}</p>
      <p v-else-if="results.suggestions.summary">{{ results.suggestions.summary }}</p>
    </div>

    <div v-if="results.suggestions.ai_provider || results.suggestions.ai_note" class="ai-meta">
      <p>
        <span v-if="results.suggestions.ai_provider"><strong>AI Provider:</strong> {{ results.suggestions.ai_provider }}. </span>
        <span v-if="results.suggestions.ai_note"><strong>Note:</strong> {{ results.suggestions.ai_note }} (applies to both summary and suggestions)</span>
      </p>
    </div>

    <h3>Suggestions</h3>
    <ul>
      <li
        v-for="(suggestion, idx) in results.suggestions.suggestions"
        :key="idx"
      >
        {{ suggestion }}
      </li>
    </ul>

    <h3>Details</h3>
    <div class="details">
      <h4>Your Business</h4>
      <div class="your-restaurant-row">
        <RestaurantCard
          v-if="results.comparison && results.comparison.user"
          :card="results.comparison.user"
          :isUser="true"
        />
      </div>

      <h4>Competitors</h4>
      <div
        v-for="(comp, idx) in results.comparison.competitors"
        :key="comp.name || comp.id || idx"
        class="competitor"
      >
        <RestaurantCard :card="comp" :isUser="false" />
      </div>
    </div>
    <AppButton
      variant="primary"
      block
      @click="$emit('reset')"
      style="margin-top: 2rem;"
    >
      Compare Another
    </AppButton>
  </div>
  <div v-else class="loading">
    <p>Loading results...</p>
  </div>
</template>

<script>
import RestaurantCard from "./RestaurantCard.vue";
import AppButton from "./AppButton.vue";
export default {
  name: "ProfileResults",
  components: { RestaurantCard, AppButton },
  props: {
    results: {
      type: Object,
      required: false,
      default: null,
    },
  },
  methods: {
    formatKey(key) {
      // Convert snake_case or camelCase to Title Case for display
      return key
        .replace(/_/g, ' ')
        .replace(/([a-z])([A-Z])/g, '$1 $2')
        .replace(/\b\w/g, l => l.toUpperCase());
    }
  }
};
</script>

<style scoped>
.results-container {
 max-width: 700px;
 margin: 2rem auto;
 padding: 2rem;
 background: #fafbfc;
 border-radius: 8px;
 box-shadow: 0 2px 8px #0001;
}
.summary {
 background: #e6f7ff;
 padding: 1rem;
 border-radius: 4px;
 margin-bottom: 1rem;
}
.details {
 margin-top: 1.5rem;
}
.competitor {
 margin-bottom: 1rem;
 padding-bottom: 0.5rem;
 border-bottom: 1px solid #eee;
}
.loading {
 text-align: center;
 margin-top: 3rem;
}
button {
 margin-top: 2rem;
 padding: 0.5rem 1.5rem;
 background: #007bff;
 color: #fff;
 border: none;
 border-radius: 4px;
 cursor: pointer;
}
button:hover {
 background: #0056b3;
}
</style>
