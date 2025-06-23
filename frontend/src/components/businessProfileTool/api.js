// profile_comparison/frontend/src/components/businessProfileTool/api.js
/**
 * API service layer for Business Profile Tool.
 * Connects frontend to Django backend endpoints for all features.
 */

import axios from "axios";

// Base URL for your Django backend API
const BASE_URL = "/api/api";

// Fetch the full business profile
export async function fetchBusinessProfile() {
  const res = await axios.get(`${BASE_URL}/business-profile/`);
  return res.data;
}

export async function fetchCompetitorsProfiles() {
  const rest = await axios.get(`${BASE_URL}/competitors/`);
  console.log(rest.data);
  return rest.data;
}

// Fetch AI-generated suggestions for the business
export async function fetchAISuggestions() {
  const res = await axios.get(`${BASE_URL}/ai-suggestions/`);
  return res.data;
}

// Simulate "What If" scenario (profile improvement impact)
export async function simulateWhatIf(changes) {
  const res = await axios.post(`${BASE_URL}/simulate-what-if/`, { changes });
  return res.data;
}

// Stream profile assistant AI response (conversational)
export async function streamProfileAssistant(question, onChunk) {
  const response = await fetch(`${BASE_URL}/profile-assistant/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!response.body) return;

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let done = false;
  let fullText = "";

  while (!done) {
    const { value, done: doneReading } = await reader.read();
    done = doneReading;
    if (value) {
      const chunk = decoder.decode(value, { stream: true });
      fullText += chunk;
      if (onChunk) onChunk(chunk, fullText);
    }
  }
  return fullText;
}

// Stream social media caption AI response
export async function streamSocialCaption(prompt, onChunk) {
  const response = await fetch(`${BASE_URL}/social-caption/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });

  if (!response.body) return;

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let done = false;
  let fullText = "";

  while (!done) {
    const { value, done: doneReading } = await reader.read();
    done = doneReading;
    if (value) {
      const chunk = decoder.decode(value, { stream: true });
      fullText += chunk;
      if (onChunk) onChunk(chunk, fullText);
    }
  }
  return fullText;
}
