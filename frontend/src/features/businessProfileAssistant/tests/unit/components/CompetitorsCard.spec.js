import { mount } from "@vue/test-utils";
import CompetitorsCard from "../../../components/CompetitorsCard.vue";

describe("CompetitorsCard.vue", () => {
  const competitors = [
    {
      id: 1,
      name: "Alpha Cafe",
      website: "https://alpha.com",
      rating: 4.5,
      category: "Cafe",
      address: "123 Main St",
    },
    {
      id: 2,
      name: "Beta Bistro",
      rating: null,
      category: "Bistro",
      address: "456 Side St",
    },
  ];

  it("renders nothing if competitors prop is empty or not provided", () => {
    const wrapper = mount(CompetitorsCard, {
      props: { competitors: [] },
    });
    expect(wrapper.find("section.sidebar-section").exists()).toBe(false);

    // Not provided (should error if required, but test for robustness)
    const wrapperNoProp = mount(CompetitorsCard, {
      props: {},
    });
    expect(wrapperNoProp.find("section.sidebar-section").exists()).toBe(false);
  });

  it("renders section and competitor items when competitors are provided", () => {
    const wrapper = mount(CompetitorsCard, {
      props: { competitors },
    });
    expect(wrapper.find("section.sidebar-section").exists()).toBe(true);
    const items = wrapper.findAll(".competitor-item");
    expect(items.length).toBe(competitors.length);
    expect(items[0].text()).toContain("Alpha Cafe");
    expect(items[1].text()).toContain("Beta Bistro");
  });

  it("renders competitor name as a link if website is provided", () => {
    const wrapper = mount(CompetitorsCard, {
      props: { competitors },
    });
    const firstLink = wrapper.findAll(".competitor-name")[0];
    expect(firstLink.element.tagName).toBe("A");
    expect(firstLink.attributes("href")).toBe("https://alpha.com");
    expect(firstLink.text()).toBe("Alpha Cafe");
  });

  it("renders competitor name as plain text if website is not provided", () => {
    const wrapper = mount(CompetitorsCard, {
      props: { competitors },
    });
    const secondName = wrapper.findAll(".competitor-name")[1];
    expect(secondName.element.tagName).toBe("SPAN");
    expect(secondName.text()).toBe("Beta Bistro");
  });

  it("renders rating if provided, otherwise shows N/A", () => {
    const wrapper = mount(CompetitorsCard, {
      props: { competitors },
    });
    const ratings = wrapper.findAll(".competitor-rating");
    expect(ratings[0].text()).toContain("4.5");
    expect(ratings[1].text()).toContain("N/A");
  });

  it("renders category and address if provided", () => {
    const wrapper = mount(CompetitorsCard, {
      props: { competitors },
    });
    const items = wrapper.findAll(".competitor-item");
    expect(items[0].text()).toContain("Cafe");
    expect(items[0].text()).toContain("123 Main St");
    expect(items[1].text()).toContain("Bistro");
    expect(items[1].text()).toContain("456 Side St");
  });

  it("emits compare event with competitor object when Compare button is clicked", async () => {
    const wrapper = mount(CompetitorsCard, {
      props: { competitors },
    });
    const buttons = wrapper.findAll("button.compare-btn");
    await buttons[0].trigger("click");
    expect(wrapper.emitted("compare")).toBeTruthy();
    expect(wrapper.emitted("compare")[0][0]).toEqual(competitors[0]);
  });
});
