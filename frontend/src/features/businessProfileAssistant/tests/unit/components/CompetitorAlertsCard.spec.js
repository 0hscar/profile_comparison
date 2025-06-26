import { mount } from "@vue/test-utils";
import CompetitorAlertsCard from "../../../components/CompetitorAlertsCard.vue";

describe("CompetitorAlertsCard.vue", () => {
  it("renders section and title when alerts are provided", () => {
    const wrapper = mount(CompetitorAlertsCard, {
      props: {
        alerts: ["Alert 1", "Alert 2"]
      }
    });
    expect(wrapper.find("section.main-section").exists()).toBe(true);
    expect(wrapper.find(".main-title").text()).toContain("Competitor Alerts");
  });

  it("renders alert entries when alerts are provided", () => {
    const alerts = ["Alert 1", "Alert 2"];
    const wrapper = mount(CompetitorAlertsCard, {
      props: { alerts }
    });
    const items = wrapper.findAll("ul.alerts-list li");
    expect(items.length).toBe(alerts.length);
    expect(items[0].text()).toContain("Alert 1");
    expect(items[1].text()).toContain("Alert 2");
  });

  it("does not render section if alerts are empty", () => {
    const wrapper = mount(CompetitorAlertsCard, {
      props: { alerts: [] }
    });
    expect(wrapper.find("section.main-section").exists()).toBe(false);
  });

  it("does not render section if alerts prop is not provided", () => {
    const wrapper = mount(CompetitorAlertsCard, {
      props: {}
    });
    expect(wrapper.find("section.main-section").exists()).toBe(false);
  });
});
