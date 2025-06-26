import { mount } from "@vue/test-utils";
import BadgesCard from "../../../components/BadgesCard.vue";

describe("BadgesCard.vue", () => {
  it("renders section and title when badges are provided", () => {
    const badges = [
      { name: "Badge 1", description: "Desc 1", icon: "🏆", unlocked: true },
      { name: "Badge 2", description: "Desc 2", icon: "⭐", unlocked: false },
    ];
    const wrapper = mount(BadgesCard, {
      props: { badges },
      global: {
        stubs: ["BadgeCard"], // stub child component
      },
    });
    expect(wrapper.find("section.sidebar-section").exists()).toBe(true);
    expect(wrapper.find(".sidebar-title").text()).toContain("Badges");
  });

  it("renders a BadgeCard for each badge", () => {
    const badges = [
      { name: "Badge 1", description: "Desc 1", icon: "🏆", unlocked: true },
      { name: "Badge 2", description: "Desc 2", icon: "⭐", unlocked: false },
    ];
    const wrapper = mount(BadgesCard, {
      props: { badges },
      global: {
        stubs: {
          BadgeCard: {
            template: "<div class='stub-badge-card'></div>",
          },
        },
      },
    });
    const badgeCards = wrapper.findAll(".stub-badge-card");
    expect(badgeCards.length).toBe(badges.length);
  });

  it("does not render section if badges prop is empty", () => {
    const wrapper = mount(BadgesCard, {
      props: { badges: [] },
      global: {
        stubs: ["BadgeCard"],
      },
    });
    expect(wrapper.find("section.sidebar-section").exists()).toBe(false);
  });
});
