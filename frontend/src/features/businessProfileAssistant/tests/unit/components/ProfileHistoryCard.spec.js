import { mount } from "@vue/test-utils";
import ProfileHistoryCard from "../../../components/ProfileHistoryCard.vue";

describe("ProfileHistoryCard.vue", () => {
  it("renders section and title when historyAvailable", () => {
    const wrapper = mount(ProfileHistoryCard, {
      props: {
        history: [
          { date: "2024-01-01", score: 90, photos: 10, reviews: 5 },
          { date: "2024-01-02", score: 92, photos: 12, reviews: 6 },
        ],
      },
    });
    expect(wrapper.find("section.main-section").exists()).toBe(true);
    expect(wrapper.find(".main-title").text()).toContain("Profile History");
  });

  it("renders history entries when history is provided", async () => {
    const history = [
      { date: "2024-01-01", score: 90, photos: 10, reviews: 5 },
      { date: "2024-01-02", score: 92, photos: 12, reviews: 6 },
    ];
    const wrapper = mount(ProfileHistoryCard, {
      props: { history },
    });
    // Expand the section
    await wrapper.find(".toggle-header").trigger("click");
    const items = wrapper.findAll("ul.history-list li");
    expect(items.length).toBe(history.length);
    expect(items[0].text()).toContain("2024-01-01");
    expect(items[1].text()).toContain("2024-01-02");
  });

  it('shows "No history from mock data" when history is empty', async () => {
    const wrapper = mount(ProfileHistoryCard, {
      props: { history: [] },
    });
    // Expand the section
    await wrapper.find(".toggle-header").trigger("click");
    expect(wrapper.text()).toContain("No history from mock data");
  });

  it("toggles show/hide when header is clicked", async () => {
    const wrapper = mount(ProfileHistoryCard, {
      props: {
        history: [{ date: "2024-01-01", score: 90, photos: 10, reviews: 5 }],
      },
    });
    expect(wrapper.vm.show).toBe(false);
    await wrapper.find(".toggle-header").trigger("click");
    expect(wrapper.vm.show).toBe(true);
    await wrapper.find(".toggle-header").trigger("click");
    expect(wrapper.vm.show).toBe(false);
  });
});
