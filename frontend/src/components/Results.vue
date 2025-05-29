<template>
  <div v-if="results" class="results-container">
    <h2>Comparison Summary</h2>
    <div class="summary">
      <p>{{ results.suggestions.summary }}</p>
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
      <ul>
        <li><strong>Name:</strong> {{ results.comparison.user.name }}</li>
        <li>
          <strong>Reviews:</strong> {{ results.comparison.user.review_count }}
        </li>
        <li>
          <strong>Average Rating:</strong>
          {{ results.comparison.user.average_rating }}
        </li>
        <li>
          <strong>Images:</strong> {{ results.comparison.user.num_images }}
        </li>
        <li>
          <strong>Has Hours:</strong>
          {{ results.comparison.user.has_hours ? "Yes" : "No" }}
        </li>
        <li>
          <strong>Has Description:</strong>
          {{ results.comparison.user.has_description ? "Yes" : "No" }}
        </li>
        <li>
          <strong>Has Menu Link:</strong>
          {{ results.comparison.user.has_menu_link ? "Yes" : "No" }}
        </li>
        <li>
          <strong>Unanswered Recent Reviews:</strong>
          {{ results.comparison.user.recent_reviews_unanswered }}
        </li>
      </ul>

      <h4>Competitors</h4>
      <div
        v-for="comp in results.comparison.competitors"
        :key="comp.name"
        class="competitor"
      >
        <strong>{{ comp.name }}</strong>
        <ul>
          <li><strong>Reviews:</strong> {{ comp.review_count }}</li>
          <li><strong>Average Rating:</strong> {{ comp.average_rating }}</li>
          <li><strong>Images:</strong> {{ comp.num_images }}</li>
          <li>
            <strong>Has Hours:</strong> {{ comp.has_hours ? "Yes" : "No" }}
          </li>
          <li>
            <strong>Has Description:</strong>
            {{ comp.has_description ? "Yes" : "No" }}
          </li>
          <li>
            <strong>Has Menu Link:</strong>
            {{ comp.has_menu_link ? "Yes" : "No" }}
          </li>
          <li>
            <strong>Unanswered Recent Reviews:</strong>
            {{ comp.recent_reviews_unanswered }}
          </li>
        </ul>
      </div>
    </div>
    <button @click="$emit('reset')">Compare Another</button>
  </div>
  <div v-else class="loading">
    <p>Loading results...</p>
  </div>
</template>

<script>
export default {
  name: "ProfileResults",
  props: {
    results: {
      type: Object,
      required: false,
      default: null,
    },
  },
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
