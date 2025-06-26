import { mount } from "@vue/test-utils";
import CompetitorList from "../../../components/CompetitorList.vue";

// Mock child component to avoid recursion
jest.mock("../../../components/CompetitorsCard.vue", () => ({
  name: "CompetitorsCard",
  template: "<div class='stub-competitors-card'></div>",
  props: ["competitors"],
}));

describe("CompetitorList.vue", () => {
  const nearbyCompetitors = [
    { id: 1, name: "Nearby 1" },
    { id: 2, name: "Nearby 2" },
  ];
  const similarCompetitors = [
    { id: 3, name: "Similar 1" },
    { id: 4, name: "Similar 2" },
  ];

  function factory(props = {}) {
    return mount(CompetitorList, {
      props: {
        nearbyCompetitors,
        similarCompetitors,
        mode: "nearby",
        ...props,
      },
      global: {
        stubs: {
          CompetitorsCard: true,
        },
      },
    });
  }

  it("renders section and title", () => {
    const wrapper = factory();
    expect(wrapper.find("section.competitor-list-section").exists()).toBe(true);
    expect(wrapper.find(".sidebar-title").text()).toContain("Competitors");
  });

  it("shows 'Nearby' and 'Similar' toggle buttons", () => {
    const wrapper = factory();
    const buttons = wrapper.findAll(".competitor-toggle button");
    expect(buttons.length).toBe(2);
    expect(buttons[0].text()).toBe("Nearby");
    expect(buttons[1].text()).toBe("Similar");
  });

  it("emits update:mode when toggle button is clicked", async () => {
    const wrapper = factory({ mode: "nearby" });
    const similarBtn = wrapper.findAll(".competitor-toggle button")[1];
    await similarBtn.trigger("click");
    expect(wrapper.emitted("update:mode")).toBeTruthy();
    expect(wrapper.emitted("update:mode")[0][0]).toBe("similar");
  });

  it("computes competitors based on mode", async () => {
    const wrapper = factory({ mode: "nearby" });
    // Should pass nearbyCompetitors to CompetitorsCard
    expect(wrapper.vm.competitors).toEqual(nearbyCompetitors);

    await wrapper.setProps({ mode: "similar" });
    expect(wrapper.vm.competitors).toEqual(similarCompetitors);
  });

  it("emits compare event from CompetitorsCard", async () => {
    const wrapper = factory();
    // Find stubbed CompetitorsCard and emit compare event
    wrapper.findComponent({ name: "CompetitorsCard" }).vm.$emit("compare", { id: 1 });
    await wrapper.vm.$nextTick();
    expect(wrapper.emitted("compare")).toBeTruthy();
    expect(wrapper.emitted("compare")[0][0]).toEqual({ id: 1 });
  });
});
