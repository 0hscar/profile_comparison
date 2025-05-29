<template>
  <div class="input-form">
    <h2>Business Profile Comparator</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="business">Your Business Name</label>
        <input
          id="business"
          v-model="business"
          type="text"
          required
          placeholder="e.g. My Restaurant"
        />
      </div>
      <div class="form-group">
        <label for="competitors">Competitors (one per line)</label>
        <textarea
          id="competitors"
          v-model="competitorsText"
          rows="3"
          placeholder="e.g. Competitor A&#10;Competitor B"
        ></textarea>
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? "Comparing..." : "Compare Profiles" }}
      </button>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
export default {
  name: "InputForm",
  data() {
    return {
      business: "",
      competitorsText: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    async submitForm() {
      this.error = null;
      this.loading = true;
      try {
        const competitors = this.competitorsText
          .split("\n")
          .map((c) => c.trim())
          .filter((c) => c.length > 0);

        const response = await fetch("/api/compare/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            business: this.business,
            competitors,
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
input,
textarea {
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
</style>
