import { mount } from "@vue/test-utils";
import BadgeCard from "../../../components/BadgeCard.vue";

describe("BadgeCard.vue", () => {
  it("renders badge name and description", () => {
    const badge = {
      name: "Superstar",
      description: "Awarded for excellence",
      icon: "⭐",
      unlocked: true,
    };
    const wrapper = mount(BadgeCard, {
      props: { badge },
    });
    expect(wrapper.text()).toContain("Superstar");
    expect(wrapper.text()).toContain("Awarded for excellence");
    expect(wrapper.html()).toContain("⭐");
    expect(wrapper.classes()).not.toContain("opacity-50");
    expect(wrapper.classes()).not.toContain("grayscale");
  });

  it("shows default icon if badge.icon is missing", () => {
    const badge = {
      name: "NoIcon",
      description: "No icon provided",
      unlocked: true,
    };
    const wrapper = mount(BadgeCard, {
      props: { badge },
    });
    expect(wrapper.text()).toContain("NoIcon");
    // Default icon is 🏅 (unicode)
    expect(wrapper.html()).toContain("🏅");
  });

  it("shows 'Locked' if badge is not unlocked", () => {
    const badge = {
      name: "LockedBadge",
      description: "You need to unlock this",
      icon: "🔒",
      unlocked: false,
    };
    const wrapper = mount(BadgeCard, {
      props: { badge },
    });
    expect(wrapper.text()).toContain("Locked");
    expect(wrapper.classes()).toContain("badge-card");
    // Should have opacity-50 and grayscale classes
    expect(wrapper.classes()).toContain("opacity-50");
    expect(wrapper.classes()).toContain("grayscale");
  });

  it("renders without description if not provided", () => {
    const badge = {
      name: "NoDesc",
      icon: "🎯",
      unlocked: true,
    };
    const wrapper = mount(BadgeCard, {
      props: { badge },
    });
    expect(wrapper.text()).toContain("NoDesc");
    // Should not throw or render description
    expect(wrapper.text()).not.toContain("undefined");
  });
});
