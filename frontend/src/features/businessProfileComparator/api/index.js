/**
 * API service layer for Business Profile Tool.
 * Connects frontend to Django backend endpoints for all features.
 */

import axios from "axios";

// Base URL for your Django backend API
// Temp route fix, change in backend!
const BASE_URL = "/api/api";

// Fetch the full business profile
export async function fetchBusinessProfile() {
  const res = await axios.get(`${BASE_URL}/business-profile/`);
  return res.data;
}

export async function fetchCompetitorsProfiles() {
  const rest = await axios.get(`${BASE_URL}/competitors/`);
  return rest.data;
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
