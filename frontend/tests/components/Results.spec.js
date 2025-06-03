const { mount } = require("@vue/test-utils");
const Results = require("@/components/Results.vue").default;

describe("Results.vue", () => {
  it("shows loader when loading is true", () => {
    const wrapper = mount(Results, {
      props: { isLoading: true },
      global: {
        stubs: {},
      },
    });
    console.log("Wrapper props :", wrapper.props());
    console.log("Wrapper HTLM: ", wrapper.html());
    expect(wrapper.find(".results-spinner").exists()).toBe(true);
    expect(wrapper.text()).toContain("Loading results...");
  });

  it("shows results when loading is false", () => {
    const wrapper = mount(Results, {
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
    console.log(wrapper.html());
    expect(wrapper.find(".results-spinner").exists()).toBe(false);
    expect(wrapper.text()).toContain("Test");
    expect(wrapper.text()).toContain("Somewhere");
    expect(wrapper.text()).toContain("5");
  });
});
