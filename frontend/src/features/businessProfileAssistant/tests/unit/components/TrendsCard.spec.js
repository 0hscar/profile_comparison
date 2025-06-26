import { mount } from "@vue/test-utils";
import TrendsCard from "../../../components/TrendsCard.vue";

describe("TrendsCard.vue", () => {
  it("renders section and title when trends are provided", () => {
    const trends = ["Trend 1", "Trend 2"];
    const wrapper = mount(TrendsCard, {
      props: { trends }
    });
    expect(wrapper.find("section.main-section").exists()).toBe(true);
    expect(wrapper.find(".main-title").text()).toContain("Local Market Trends");
  });

  it("renders all trends in the list", () => {
    const trends = ["Trend A", "Trend B", "Trend C"];
    const wrapper = mount(TrendsCard, {
      props: { trends }
    });
    const items = wrapper.findAll("ul.trends-list li");
    expect(items.length).toBe(trends.length);
    expect(items[0].text()).toBe("Trend A");
    expect(items[1].text()).toBe("Trend B");
    expect(items[2].text()).toBe("Trend C");
  });

  it("does not render section if trends prop is empty", () => {
    const wrapper = mount(TrendsCard, {
      props: { trends: [] }
    });
    expect(wrapper.find("section.main-section").exists()).toBe(false);
  });

  it("does not render section if trends prop is not provided", () => {
    const wrapper = mount(TrendsCard, {
      props: { trends: undefined }
    });
    expect(wrapper.find("section.main-section").exists()).toBe(false);
  });
});
