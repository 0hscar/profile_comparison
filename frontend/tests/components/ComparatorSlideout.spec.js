const { mount } = require("@vue/test-utils");
const ComparatorSlideout =
  require("@/components/ComparatorSlideout.vue").default;

describe("ComparatorSlideout.vue", () => {
  it("renders when open is true", () => {
    const wrapper = mount(ComparatorSlideout, {
      props: {
        open: true,
        userProfile: [],
        competitorProfiles: [],
        comparison: null,
        suggestions: null,
        extraInsights: null,
        defaultUserBusiness: {},
        defaultNearby: [],
        defaultSimilar: [],
        showNearby: true,
        userBusinessName: "Test",
        userBusinessLocation: "Test City",
        loading: false,
      },
      global: {
        stubs: [
          "AppButton",
          "SidebarRestaurantList",
          "InputForm",
          "ProfileResults",
        ],
      },
    });
    expect(wrapper.find(".comparator-slideout.open").exists()).toBe(true);
  });

  it("emits close when overlay is clicked", async () => {
    const wrapper = mount(ComparatorSlideout, {
      props: {
        open: true,
        userProfile: [],
        competitorProfiles: [],
        comparison: null,
        suggestions: null,
        extraInsights: null,
        defaultUserBusiness: {},
        defaultNearby: [],
        defaultSimilar: [],
        showNearby: true,
        userBusinessName: "Test",
        userBusinessLocation: "Test City",
        loading: false,
      },
      global: {
        stubs: [
          "AppButton",
          "SidebarRestaurantList",
          "InputForm",
          "ProfileResults",
        ],
      },
    });
    await wrapper.find(".slideout-overlay").trigger("click");
    expect(wrapper.emitted("close")).toBeTruthy();
  });

  it("passes loading prop to ProfileResults", () => {
    const wrapper = mount(ComparatorSlideout, {
      props: {
        open: true,
        isLoading: true,
        userProfile: [],
        competitorProfiles: [],
        comparison: null,
        suggestions: null,
        extraInsights: null,
        defaultUserBusiness: {},
        defaultNearby: [],
        defaultSimilar: [],
        showNearby: true,
        userBusinessName: "Test",
        userBusinessLocation: "Test City",
      },
      global: {
        stubs: [
          "AppButton",
          "SidebarRestaurantList",
          "InputForm",
          "ProfileResults",
        ],
      },
    });
    const results = wrapper.findComponent({ name: "ProfileResults" });
    expect(results.props("isLoading")).toBe(true);
  });
});
