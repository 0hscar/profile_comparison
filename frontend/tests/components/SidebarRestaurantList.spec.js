const { mount } = require("@vue/test-utils");
const SidebarRestaurantList = require("@/components/SidebarRestaurantList.vue");

describe("SidebarRestaurantList.vue", () => {
  it("renders user business and toggles", () => {
    const wrapper = mount(SidebarRestaurantList, {
      props: {
        defaultUserBusiness: { name: "User Restaurant" },
        defaultNearby: [{ name: "Nearby 1" }],
        defaultSimilar: [{ name: "Similar 1" }],
        showNearby: true,
      },
      global: {
        stubs: ['RestaurantCard']
      }
    });
    expect(wrapper.text()).toContain("User Restaurant");
    expect(wrapper.text()).toContain("Nearby Restaurants");
    wrapper.find(".toggle-btn").trigger("click");
    expect(wrapper.emitted("toggle")).toBeTruthy();
  });
});
