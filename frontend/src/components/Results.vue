<template>
  <div v-if="loading" class="results-loading">
    <span class="results-spinner"></span>
    <p>Loading results...</p>
  </div>
  <div
    v-else-if="userProfile || (competitorProfiles && competitorProfiles.length)"
    class="results-container"
  >
    <!-- Restaurant Cards (User and Competitors) -->
    <div>
      <h2><div class="user-banner">You</div></h2>
      <div>
        <div
          v-if="
            userProfile &&
            Array.isArray(userProfile) &&
            userProfile.length &&
            typeof userProfile[0] === 'object'
          "
          class="user"
        >
          <h3>
            {{ userProfile[0].Name }}
          </h3>

          <p>
            <strong>Address:</strong>
            {{ userProfile[0].Address }}
          </p>
          <p>
            <strong>Rating:</strong>
            {{ userProfile[0].Rating }}
          </p>
        </div>
        <template
          v-if="
            competitorProfiles &&
            competitorProfiles.length &&
            Array.isArray(competitorProfiles[0])
          "
        >
          <h2>Competitors</h2>
          <div
            v-for="(competitor, idx) in competitorProfiles[0]"
            :key="idx"
            class="competitor"
          >
            <h3>{{ competitor.Name }}</h3>
            <p>
              <strong>Address:</strong>
              {{ competitor.Address }}
            </p>
            <p>
              <strong>Rating:</strong>
              {{ competitor.Rating }}
            </p>
          </div>
        </template>

        <!-- If flat array of objects -->
        <template v-else>
          <div
            v-for="(competitor, idx) in competitorProfiles"
            :key="idx"
            class="competitor"
          >
            <h3>{{ competitor.Name }}</h3>
            <p>
              <strong>Address:</strong>
              {{ competitor.Address }}
            </p>
            <p>
              <strong>Rating:</strong>
              {{ competitor.Rating }}
            </p>
          </div>
        </template>
      </div>
    </div>

    <h2>Comparison Summary</h2>
    <div class="summary">
      <ul>
        <li v-for="(comparison, idx) in comparison || []" :key="idx">
          {{ comparison }}
        </li>
      </ul>
    </div>

    <div
      v-if="suggestions && (suggestions.ai_provider || suggestions.ai_note)"
      class="ai-meta"
    >
      <p>
        <span v-if="suggestions.ai_provider"
          ><strong>AI Provider:</strong> {{ suggestions.ai_provider }}.
        </span>
        <span v-if="suggestions.ai_note"
          ><strong>Note:</strong> {{ suggestions.ai_note }} (applies to both
          summary and suggestions)</span
        >
      </p>
    </div>

    <h2>Suggestions</h2>
    <ul>
      <li v-for="(suggestion, idx) in suggestions || []" :key="idx">
        {{ suggestion }}
      </li>
    </ul>

    <h2>Extra Insights</h2>
    <ul>
      <li v-for="(extraInsights, idx) in extraInsights || []" :key="idx">
        {{ extraInsights }}
      </li>
    </ul>
  </div>
  <div v-else class="loading">
    <p>Loading results...</p>
  </div>
</template>

<script>
export default {
  name: "ProfileResults",
  props: {
    // Instead of searchResults, accept userProfile and competitorProfiles
    userProfile: {
      type: Object,
      required: false,
      default: null,
    },
    competitorProfiles: {
      type: Array,
      required: false,
      default: () => [],
    },
    comparison: {
      type: Object,
      required: false,
      default: null,
    },
    suggestions: {
      type: Object,
      required: false,
      default: null,
    },
    extraInsights: {
      type: Object,
      required: false,
      default: null,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    formatKey(key) {
      // Convert snake_case or camelCase to Title Case for display
      return key
        .replace(/_/g, " ")
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/\b\w/g, (l) => l.toUpperCase());
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
.user {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #007bff;
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
.user-banner {
  display: inline-block;
  background: #007bff;
  color: #fff;
  font-weight: bold;
  padding: 0.25em 1em;
  border-radius: 999px;
  margin-bottom: 0.5em;
  margin-right: 0.5em;
  font-size: 1rem;
  letter-spacing: 0.05em;
}
.results-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}
.results-spinner {
  display: inline-block;
  width: 36px;
  height: 36px;
  border: 4px solid #e6eaf0;
  border-top: 4px solid #2d8cf0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
