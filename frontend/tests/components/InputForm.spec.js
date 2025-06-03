const { mount } = require("@vue/test-utils");
const InputForm = require("@/components/InputForm.vue").default;

// Mock the compareResponseHandler
jest.mock("@/utils/compareResponseHandler", () => ({
  __esModule: true,
  default: jest.fn(() =>
    Promise.resolve({
      user_profile: [{ Name: "Test" }],
      competitor_profiles: [],
    })
  ),
}));

describe("InputForm.vue", () => {
  it("emits set-loading when submitting", async () => {
    const wrapper = mount(InputForm, {
      props: {
        userBusinessName: "Test",
        userBusinessLocation: "Test City",
      },
      global: {
        stubs: {
          AppButton: true,
          vSelect: true,
        },
      },
    });
    // Fill required fields
    await wrapper.setData({
      query: "Test",
      location: "Test City",
      gl: "fi",
      numPlaces: 1,
    });
    // Submit the form
    await wrapper.find("form").trigger("submit.prevent");
    // Loader should be true at some point
    expect(wrapper.emitted("set-loading")[0]).toEqual([true]);
    // Loader should be false after
    await wrapper.vm.$nextTick();
    expect(wrapper.emitted("set-loading").pop()).toEqual([false]);
  });

  it("emits comparison-result after successful compare", async () => {
    const wrapper = mount(InputForm, {
      props: {
        userBusinessName: "Test",
        userBusinessLocation: "Test City",
      },
      global: {
        stubs: {
          AppButton: true,
          vSelect: true,
        },
      },
    });
    await wrapper.setData({
      query: "Test",
      location: "Test City",
      gl: "fi",
      numPlaces: 1,
    });
    await wrapper.find("form").trigger("submit.prevent");
    expect(wrapper.emitted("comparison-result")).toBeTruthy();
  });
});
