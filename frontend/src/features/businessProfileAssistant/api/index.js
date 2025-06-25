/**
 * API service layer for Business Profile Tool.
 * Connects frontend to Django backend endpoints for all features.
 */

import axios from "axios";

// Base URLs for your Django backend API (modularized by feature)
// Points directly to the localhost to bypass Vue CLI proxy
// Via proxy used Brotli compression which broke the streaming response
const PROFILE_BASE_URL = "http://localhost:8000/api/profiles";
const COMPETITOR_BASE_URL = "http://localhost:8000/api/competitors";
const AI_BASE_URL = "http://localhost:8000/api/ai";

// Fetch the full business profile
export async function fetchBusinessProfile() {
  const res = await axios.get(`${PROFILE_BASE_URL}/business-profile/`);
  return res.data;
}

export async function fetchCompetitorsProfiles() {
  const rest = await axios.get(`${COMPETITOR_BASE_URL}/competitors/`);
  return rest.data;
}

// Stream profile assistant AI response (conversational)
export async function streamProfileAssistant(question, onChunk) {
  const response = await fetch(`${AI_BASE_URL}/profile-assistant/`, {
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
