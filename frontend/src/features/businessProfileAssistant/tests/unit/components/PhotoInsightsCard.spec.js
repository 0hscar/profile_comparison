import { mount } from "@vue/test-utils";
import PhotoInsightsCard from "../../../components/PhotoInsightsCard.vue";

describe("PhotoInsightsCard.vue", () => {
  it("renders nothing if insights prop is empty or not provided", () => {
    // No prop
    const wrapperNoProp = mount(PhotoInsightsCard, {
      props: { insights: [] }
    });
    expect(wrapperNoProp.find("section.main-section").exists()).toBe(false);

    // Empty array
    const wrapperEmpty = mount(PhotoInsightsCard, {
      props: { insights: [] }
    });
    expect(wrapperEmpty.find("section.main-section").exists()).toBe(false);
  });

  it("renders section and title when insights are provided", () => {
    const insights = ["Great lighting in photos", "High engagement"];
    const wrapper = mount(PhotoInsightsCard, {
      props: { insights }
    });
    expect(wrapper.find("section.main-section").exists()).toBe(true);
    expect(wrapper.find(".main-title").text()).toContain("Photo Insights");
  });

  it("renders all insights in the list", () => {
    const insights = ["Insight 1", "Insight 2", "Insight 3"];
    const wrapper = mount(PhotoInsightsCard, {
      props: { insights }
    });
    const items = wrapper.findAll("ul.photo-insights-list li");
    expect(items.length).toBe(insights.length);
    insights.forEach((insight, idx) => {
      expect(items[idx].text()).toBe(insight);
    });
  });
});
