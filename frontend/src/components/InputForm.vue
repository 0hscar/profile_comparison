<template>
  <div class="input-form responsive-search-form">
    <h2>Business Profile Comparator</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="query">Search Query</label>
        <input
          id="query"
          v-model="query"
          type="text"
          required
          placeholder="e.g. thai food"
        />
      </div>
      <div class="form-group">
        <label for="location">Location</label>
        <v-select
          id="location"
          :options="locationOptions"
          v-model="location"
          :filterable="true"
          placeholder="Select or search location"
        />
      </div>
      <div class="form-group">
        <label for="gl">Country Code (gl)</label>
        <v-select
          id="gl"
          :options="glOptions"
          v-model="gl"
          :filterable="true"
          placeholder="Select or search country code"
        />
      </div>
      <div class="button-row">
        <AppButton
          type="submit"
          :disabled="loading"
        >
          {{ loading ? "Searching..." : "Compare Profiles" }}
        </AppButton>
        <AppButton
          type="button"
          variant="secondary"
          @click="$emit('reset')"
        >
          Back to Default
        </AppButton>
      </div>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import vSelect from "vue3-select";
import "vue3-select/dist/vue3-select.css";
import AppButton from "./AppButton.vue";

export default {
  name: "InputForm",
  components: { vSelect, AppButton },
  data() {
    return {
      query: "",
      location: null,
      gl: null,
      loading: false,
      error: null,
      locationOptions: [
        "Finland",
        "Sweden",
        "Norway",
        "Denmark",
        "Germany",
        "United States",
        "United Kingdom",
        "France",
        "Italy",
        "Spain"
      ],
      glOptions: [
        "fi", "se", "no", "dk", "de", "us", "uk", "fr", "it", "es"
      ]
    };
  },
  methods: {
    async submitForm() {
      this.error = null;
      this.loading = true;
      try {
        if (!this.query || !this.location || !this.gl) {
          throw new Error("Please fill in all fields.");
        }
        const response = await fetch("/api/compare/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            mode: "search",
            query: this.query,
            location: this.location,
            gl: this.gl,
          }),
        });

        if (!response.ok) {
          const err = await response.json();
          throw new Error(err.error || "Failed to compare profiles.");
        }

        const data = await response.json();
        this.$emit("comparison-result", data);
      } catch (e) {
        this.error = e.message || "An error occurred.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.input-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fafbfc;
  border-radius: 8px;
  box-shadow: 0 2px 8px #0001;
}
.form-group {
  margin-bottom: 1.2rem;
}
label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}
input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #bbb;
  border-radius: 4px;
  font-size: 1rem;
}
button {
  background: #2d8cf0;
  color: #fff;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}
button:disabled {
  background: #b3d4fc;
  cursor: not-allowed;
}
.error {
  color: #d93025;
  margin-top: 1rem;
  text-align: center;
}
.button-row {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 0.5rem;
}
.button-row .app-btn {
  min-width: 120px;
  max-width: 180px;
  font-size: 1rem;
  padding: 0.5rem 1.1rem;
  border-radius: 4px;
}
</style>
