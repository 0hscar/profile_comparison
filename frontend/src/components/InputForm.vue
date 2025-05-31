<template>
  <div class="input-form responsive-search-form">
    <h2>Business Profile Comparator</h2>
    <div class="form-slide-wrapper">
      <transition name="slide" mode="out-in">
        <form
          v-if="!showCompareOneForm"
          key="main"
          @submit.prevent="submitForm(numPlaces)"
          class="slide-form"
        >
          <div class="form-group">
            <label for="query">Search</label>
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
              :taggable="true"
              placeholder="Select or search location"
            />
          </div>
          <div class="form-group">
            <label for="gl">Country Code</label>
            <v-select
              id="gl"
              :options="glOptions"
              v-model="gl"
              :filterable="true"
              placeholder="Select or search country code"
            />
          </div>
          <div class="form-group">
            <label for="num_places">Number of Places to Compare</label>
            <input
              id="num_places"
              v-model.number="numPlaces"
              type="number"
              min="1"
              max="10"
              required
              placeholder="Enter number (e.g. 1, 3, 5)"
            />
          </div>
          <div class="button-row">
            <AppButton type="submit" :disabled="loading">
              {{ loading ? "Searching..." : "Compare Profiles" }}
            </AppButton>
            <AppButton
              type="button"
              variant="secondary"
              :disabled="loading"
              @click="showCompareOneForm = true"
            >
              Search Specific Profile
            </AppButton>
          </div>
        </form>
        <form
          v-else
          key="compareone"
          @submit.prevent="submitForm(1)"
          class="slide-form"
        >
          <div class="back-row">
            <button
              type="button"
              class="back-arrow"
              @click="showCompareOneForm = false"
              aria-label="Back to main form"
            >
              <span>&larr;</span>
            </button>
          </div>
          <div class="form-group">
            <label for="query-one">Search</label>
            <input
              id="query-one"
              v-model="query"
              type="text"
              required
              placeholder="e.g. Ravintola Savoy"
            />
          </div>
          <div class="form-group">
            <label for="location-one">Location</label>
            <v-select
              id="location-one"
              :options="locationOptions"
              v-model="location"
              :filterable="true"
              :taggable="true"
              placeholder="Select or search location"
            />
          </div>
          <div class="button-row">
            <AppButton type="submit" :disabled="loading">
              {{ loading ? "Searching..." : "Compare" }}
            </AppButton>
          </div>
        </form>
      </transition>
    </div>
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
  props: {
    userBusinessName: {
      type: String,
      required: true,
    },
    userBusinessLocation: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      query: "",
      location: null,
      gl: null,
      numPlaces: 3, // Default value
      loading: false,
      error: null,
      showCompareOneForm: false,
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
        "Spain",
      ],
      glOptions: ["fi", "se", "no", "dk", "de", "us", "uk", "fr", "it", "es"],
    };
  },
  methods: {
    async submitForm(numPlacesOrEvent) {
      this.error = null;
      this.loading = true;
      try {
        let numPlaces = this.numPlaces;
        // Handle both main and compare-one form
        if (typeof numPlacesOrEvent === "number") {
          numPlaces = numPlacesOrEvent;
        } else if (
          numPlacesOrEvent &&
          typeof numPlacesOrEvent.preventDefault === "function"
        ) {
          numPlacesOrEvent.preventDefault();
        }
        if (
          !this.query ||
          !this.location ||
          (!this.gl && !this.showCompareOneForm) ||
          !numPlaces
        ) {
          throw new Error("Please fill in all fields.");
        }
        const payload = {
          mode: "search",
          query: this.query,
          location: this.location,
          gl: this.showCompareOneForm ? undefined : this.gl,
          user_business_name: this.userBusinessName,
          user_business_location: this.userBusinessLocation,
          num_places: numPlaces,
        };
        console.log("Searching for places: ", numPlaces);
        // Remove undefined gl if not needed
        if (payload.gl === undefined) delete payload.gl;
        const response = await fetch("/api/compare/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
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
  min-height: 500px;
  position: relative;
}

.form-slide-wrapper {
  position: relative;
  min-height: 350px;
}

.slide-form {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
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
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.4s cubic-bezier(0.55, 0, 0.1, 1),
    opacity 0.4s cubic-bezier(0.55, 0, 0.1, 1);
  will-change: transform, opacity;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
.slide-enter-to,
.slide-leave-from {
  transform: translateX(0%);
  opacity: 1;
}
.back-row {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.back-arrow {
  background: none;
  border: none;
  color: #2d8cf0;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  margin-right: 0.5rem;
  line-height: 1;
}
.back-arrow:focus {
  outline: 2px solid #2d8cf0;
}
</style>
