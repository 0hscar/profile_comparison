const { mount } = require("@vue/test-utils");
const ProfileResults = require("@/components/Results.vue");

describe("ProfileResults.vue", () => {
  it("shows loader when loading is true", () => {
    const wrapper = mount(ProfileResults, {
      props: { loading: true },
      global: {
        stubs: {},
      },
    });
    expect(wrapper.find(".results-spinner").exists()).toBe(true);
    expect(wrapper.text()).toContain("Loading results...");
  });

  it("shows results when loading is false", () => {
    const wrapper = mount(ProfileResults, {
      props: {
        loading: false,
        userProfile: [{ Name: "Test", Address: "Somewhere", Rating: "5" }],
        competitorProfiles: [],
        comparison: [],
        suggestions: {},
        extraInsights: {},
      },
      global: {
        stubs: {},
      },
    });
    expect(wrapper.find(".results-spinner").exists()).toBe(false);
    expect(wrapper.text()).toContain("Test");
    expect(wrapper.text()).toContain("Somewhere");
    expect(wrapper.text()).toContain("5");
  });
});
