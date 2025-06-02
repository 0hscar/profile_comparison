const { mount } = require("@vue/test-utils");

// Mock the compareResponseHandler
jest.mock("../../../src/utils/compareResponseHandler.js", () => ({
  __esModule: true,
  default: jest.fn(() =>
    Promise.resolve({
      user_profile: [{ Name: "Test" }],
      competitor_profiles: [],
    })
  ),
}));

describe("RestaurantCard.vue", () => {
  const card = { name: "Test Restaurant", address: "123 Main", rating: 4.5 };

  it("shows compare button when showDirectCompare is true", () => {
    const wrapper = mount(RestaurantCard, {
      props: {
        card,
        showDirectCompare: true,
        isUser: false,
        userBusinessName: "",
        userBusinessLocation: "",
      },
      global: {
        stubs: ["AppButton"],
      },
    });
    expect(wrapper.find(".direct-compare-btn").exists()).toBe(true);
  });

  it("emits set-loading and comparison-result on direct compare", async () => {
    const wrapper = mount(RestaurantCard, {
      props: {
        card,
        showDirectCompare: true,
        isUser: false,
        userBusinessName: "",
        userBusinessLocation: "",
      },
      global: {
        stubs: ["AppButton"],
      },
    });
    await wrapper.find(".direct-compare-btn").trigger("click");
    // Loader event
    expect(wrapper.emitted("set-loading")[0]).toEqual([true]);
    // Wait for async
    await wrapper.vm.$nextTick();
    expect(wrapper.emitted("set-loading").pop()).toEqual([false]);
    expect(wrapper.emitted("comparison-result")).toBeTruthy();
  });
});
