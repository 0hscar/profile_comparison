const { mount } = require("@vue/test-utils");
const SidebarRestaurantList =
  require("@/components/SidebarRestaurantList.vue").default;

describe("shows correct headings and toggles between lists", () => {
  it("renders user business and toggles", () => {
    const wrapper = mount(SidebarRestaurantList, {
      props: {
        defaultUserBusiness: { name: "User Restaurant" },
        defaultNearby: [{ name: "Nearby 1" }],
        defaultSimilar: [{ name: "Similar 1" }],
        showNearby: true,
      },
      global: {
        stubs: ["RestaurantCard"],
      },
    });
    expect(wrapper.text()).toContain("Nearby Restaurants");
    expect(wrapper.text()).toContain("Nearby");
    expect(wrapper.text()).toContain("Similar");
    wrapper.find(".toggle-btn").trigger("click");
    expect(wrapper.emitted("toggle")).toBeTruthy();
  });
});
