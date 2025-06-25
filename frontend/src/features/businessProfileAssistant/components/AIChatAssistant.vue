<template>
  <section v-if="show" class="main-section card-modern ai-chat-modern">
    <h2 class="main-title card-title-modern">AI Chat Assistant</h2>
    <div class="gpt-chat-history card-content-modern">
      <div
        v-for="(msg, idx) in chatHistory"
        :key="idx"
        :class="[
          'gpt-message',
          msg.role === 'user'
            ? 'gpt-user'
            : msg.system
            ? 'gpt-system'
            : 'gpt-assistant',
        ]"
      >
        <div v-if="msg.system" class="gpt-system-bubble">
          {{ msg.content }}
        </div>
        <div v-else-if="msg.role === 'assistant'" class="gpt-assistant-bubble">
          <div v-html="renderMarkdownSafe(msg.content)"></div>
        </div>
        <div v-else-if="msg.role === 'user'" class="gpt-user-bubble">
          {{ msg.content }}
        </div>
      </div>
    </div>
    <form class="gpt-chat-input-row" @submit.prevent="onSend">
      <textarea
        ref="chatInputRef"
        :value="chatInputProp"
        placeholder="Send a message..."
        class="gpt-chat-input gpt-chat-textarea"
        autocomplete="off"
        rows="1"
        @input="
          $emit('update:chatInputProp', $event.target.value);
          autoGrow();
        "
        @keydown="onInputKeydown"
      />
      <select v-model="selectedModel">
        <option
          v-for="model in LLM_MODELS"
          :key="model.value"
          :value="model.value"
        >
          {{ model.label }}
        </option>
      </select>

      <button
        class="gpt-chat-send-btn"
        :disabled="loading || !(chatInputProp || '').trim()"
      >
        <span v-if="!loading">Send</span>
        <span v-else>...</span>
      </button>
    </form>
  </section>
</template>

<script setup>
import { ref, nextTick, watch } from "vue";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";
import { LLM_MODELS } from "../composables/useChatAssistant";

// Props from parent/composable
const props = defineProps({
  show: { type: Boolean, default: true },
  chatHistory: { type: Array, required: true },
  chatInputProp: { type: String, required: true },
  loading: { type: Boolean, default: false },
  selectedModel: {
    type: String,
    required: false,
    default: LLM_MODELS[0].value,
  },
});
const emit = defineEmits([
  "update:chatInputProp",
  "send",
  "update:selectedModel",
]);
const chatInputRef = ref(null);
const md = new MarkdownIt({
  breaks: true,
});

// Local model binding for v-model
const selectedModel = ref(props.selectedModel);
watch(selectedModel, (val) => emit("update:selectedModel", val));

function renderMarkdownSafe(content) {
  const rawHtml = md.render(content || "");
  return DOMPurify.sanitize(rawHtml);
}

function autoGrow() {
  nextTick(() => {
    const el = chatInputRef.value;
    if (el) {
      el.style.height = "auto";
      el.style.overflowY = "hidden";
      el.style.height = el.scrollHeight + "px";
      if (el.scrollHeight > 160) {
        el.style.overflowY = "auto";
        el.style.height = "160px";
      }
    }
  });
}

function onInputKeydown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    onSend();
  }
}

// Keep textarea in sync with parent input
watch(
  () => props.chatInputProp,
  () => autoGrow()
);

function onSend() {
  emit("send");
}
</script>

<style scoped>
.gpt-chat-history {
  background: #f7f7fa;
  border-radius: 12px;
  padding: 2em 1.5em 1em 1.5em;
  margin-bottom: 1.5em;
  border: 1px solid #e6eaf0;
  display: flex;
  flex-direction: column;
  gap: 1.2em;
  flex: 1 1 auto;
  min-height: 0;
  max-height: none;
  overflow-y: auto;
}
.gpt-message {
  display: flex;
  flex-direction: row;
  margin-bottom: 0;
}
.gpt-user {
  justify-content: flex-end;
}
.gpt-user-bubble {
  background: #e6f0fa;
  color: #1a2b3c;
  border-radius: 12px 12px 4px 12px;
  padding: 0.9em 1.2em;
  margin-left: auto;
  max-width: 70%;
  font-size: 1.08em;
  box-shadow: 0 1px 2px #0001;
}
.gpt-assistant {
  justify-content: flex-start;
}
.gpt-assistant-bubble {
  background: #fff;
  color: #222;
  border-radius: 12px 12px 12px 4px;
  padding: 0.9em 1.2em;
  margin-right: auto;
  max-width: 70%;
  font-size: 1.08em;
  box-shadow: 0 1px 2px #0001;
}
.gpt-system {
  justify-content: center;
  width: 100%;
}
.gpt-system-bubble {
  background: #f3f3f6;
  color: #888;
  border-radius: 8px;
  padding: 0.8em 1.1em;
  margin: 0 auto;
  font-size: 1.05em;
  text-align: center;
  max-width: 80%;
  box-shadow: 0 1px 2px #0001;
}
.gpt-chat-input-row {
  display: flex;
  gap: 0.7em;
  margin-top: 1em;
  align-items: center;
  flex: 0 0 auto;
}
.gpt-chat-input {
  flex: 1;
  padding: 1em;
  border-radius: 8px;
  border: 1px solid #e6eaf0;
  font-size: 1.08em;
  background: #f7f7fa;
  transition: border 0.2s;
  resize: none;
  min-height: 2.5em;
  max-height: 160px;
  overflow-y: auto;
  line-height: 1.5;
  box-sizing: border-box;
}
.gpt-chat-input:focus {
  border: 1.5px solid #1761a0;
  outline: none;
}
.gpt-chat-textarea {
  width: 100%;
  font-family: inherit;
  display: block;
}
.gpt-chat-send-btn {
  background: #1761a0;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.8em 1.6em;
  font-size: 1.08em;
  cursor: pointer;
  transition: background 0.2s;
  font-weight: 600;
}
.gpt-chat-send-btn:disabled {
  background: #b0b8c1;
  cursor: not-allowed;
}
</style>
