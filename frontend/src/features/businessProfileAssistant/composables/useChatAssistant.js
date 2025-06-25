/**
 * useChatAssistant.js
 * Composable for managing AI chat assistant logic (state, streaming, prompt insertion).
 * Company-level modularity: Keeps chat logic out of components, reusable and testable.
 */

import { ref } from "vue";
import * as api from "../api";

export const LLM_MODELS = [
  { value: "gpt-4.1-mini", label: "GPT-4.1 Mini" },
  { value: "gpt-4o", label: "GPT-4o" },
];

/**
 * useChatAssistant composable
 * Handles chat state, streaming, and prompt logic for the AI assistant.
 */
export function useChatAssistant() {
  // State
  const chatHistory = ref([
    {
      role: "assistant",
      content:
        '👋 Welcome! I\'m your Business Profile AI Assistant. You can ask me to help with things like generating social media post captions, simulating the effect of profile changes, analyzing competitors, or getting tips to improve your business profile. Try asking something like: "Write a catchy Instagram caption for my restaurant", "What would happen if I added 10 more photos?", or "How can I improve my Google ranking?"',
      system: true,
    },
  ]);
  const chatInput = ref("");
  const loading = ref(false);

  // Model selection
  const selectedModel = ref(LLM_MODELS[0].value);

  /**
   * Send a chat message to the AI assistant (with streaming response).
   */
  async function sendChat() {
    const input = chatInput.value.trim();
    if (!input) return;
    chatHistory.value.push({ role: "user", content: input });
    chatInput.value = "";
    loading.value = true;

    // Add a placeholder for the assistant's streaming response
    chatHistory.value.push({ role: "assistant", content: "" });

    try {
      await api.streamProfileAssistant(
        input,
        selectedModel.value,
        (chunk, fullText) => {
          // Update the last assistant message as the stream progresses
          const lastMsg = chatHistory.value[chatHistory.value.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            lastMsg.content = fullText;
          }
        }
      );
    } catch (e) {
      const lastMsg = chatHistory.value[chatHistory.value.length - 1];
      if (lastMsg && lastMsg.role === "assistant") {
        lastMsg.content = "Sorry, I couldn't process your request.";
      }
    }
    loading.value = false;
  }

  /**
   * Insert a competitor comparison prompt into the chat input.
   * @param {Object} comp - Competitor object
   */
  function insertCompetitorPrompt(comp) {
    const prompt = `Compare my business profile with the following competitor:

Name: ${comp.name}
Address: ${comp.address || "Not found"}
Category: ${comp.category || "Not found"}
Price: ${comp.price_level || "Not found"}
Rating: ${comp.rating || "Not found"}
Rating Count: ${comp.review_count || "Not found"}
Hours: ${comp.hours || "Not found"}
Phone: ${comp.phone || "Not found"}
Menu: ${comp.menu_url || "Not found"}
Website: ${comp.website || "Not found"}
Description: ${comp.description || "Not found"}
Photos: ${comp.photos || "Not found"}

Highlight key differences and similarities. Give actionable suggestions to improve my profile based on this competitor.`;
    chatInput.value = prompt;
  }

  return {
    chatHistory,
    chatInput,
    loading,
    sendChat,
    insertCompetitorPrompt,
    selectedModel,
    LLM_MODELS,
    // ...other exports
  };
}
