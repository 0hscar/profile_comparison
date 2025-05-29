<template>
  <div id="app">
    <h1>Business Profile Comparator</h1>
    <InputForm @comparison-result="handleResults" />
    <ProfileResults v-if="results" :results="results" />
  </div>
</template>

<script>
import InputForm from "./components/InputForm.vue";
import ProfileResults from "./components/Results.vue";

export default {
  name: "App",
  components: {
    InputForm,
    ProfileResults,
  },
  data() {
    return {
      results: null,
    };
  },
  methods: {
    handleResults(data) {
      this.results = data;
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 2rem auto;
  max-width: 600px;
  padding: 2rem;
  background: #fafbfc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
h1 {
  text-align: center;
  margin-bottom: 2rem;
}
</style>
