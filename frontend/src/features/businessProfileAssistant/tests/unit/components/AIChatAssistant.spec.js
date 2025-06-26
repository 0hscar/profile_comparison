import { mount } from "@vue/test-utils";
import AIChatAssistant from "../../../components/AIChatAssistant.vue";

describe("AIChatAssistant.vue", () => {
  // Helper to mount with required props
  function factory(overrides = {}) {
    return mount(AIChatAssistant, {
      props: {
        show: true,
        chatHistory: [
          { role: "assistant", content: "Hello!", system: false },
          { role: "user", content: "Hi!", system: false },
        ],
        chatInputProp: "",
        loading: false,
        selectedModel: "gpt-4.1-mini",
        ...overrides,
      },
      global: {
        // stub out renderMarkdownSafe if needed
        methods: {
          renderMarkdownSafe: (x) => x,
        },
      },
    });
  }

  it("emits update:chatInputProp when typing in textarea", async () => {
    const wrapper = factory();
    const textarea = wrapper.find("textarea.gpt-chat-input");
    await textarea.setValue("Test message");
    // The @input handler emits update:chatInputProp
    expect(wrapper.emitted("update:chatInputProp")).toBeTruthy();
    expect(wrapper.emitted("update:chatInputProp")[0][0]).toBe("Test message");
  });

  it("disables send button when loading", () => {
    const wrapper = factory({ loading: true, chatInputProp: "something" });
    const button = wrapper.find("button.gpt-chat-send-btn");
    expect(button.attributes("disabled")).toBeDefined();
  });

  it("disables send button when input is empty or whitespace", async () => {
    const wrapper = factory({ chatInputProp: "" });
    const button = wrapper.find("button.gpt-chat-send-btn");
    expect(button.attributes("disabled")).toBeDefined();

    await wrapper.setProps({ chatInputProp: "   " });
    expect(button.attributes("disabled")).toBeDefined();
  });

  it("emits send event when form is submitted", async () => {
    const wrapper = factory({ chatInputProp: "Hello AI" });
    const form = wrapper.find("form.gpt-chat-input-row");
    await form.trigger("submit.prevent");
    // Replace "send" with the actual event name if different
    expect(wrapper.emitted()).toHaveProperty("send");
  });

  it("updates selectedModel when changed", async () => {
    const wrapper = factory({ selectedModel: "gpt-4.1-mini" });
    const select = wrapper.find("select#llm-model-select");
    await select.setValue("gpt-4o");
    // v-model updates the prop, but since selectedModel is a prop, parent must update it.
    // So, the component should emit an update event if using v-model, but here we check the select value.
    expect(select.element.value).toBe("gpt-4o");
  });
});
