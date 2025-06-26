/* global global */
import axios from "axios";
import * as api from "../../../api/index";
import { TextEncoder, TextDecoder } from "util";

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

jest.mock("axios");

describe("API Service", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe("fetchBusinessProfile", () => {
    it("fetches business profile data from backend", async () => {
      const mockData = { name: "Test Biz", address: "123 Main St" };
      axios.get.mockResolvedValueOnce({ data: mockData });

      const result = await api.fetchBusinessProfile();

      expect(axios.get).toHaveBeenCalledWith(
        "http://localhost:8000/api/profiles/business-profile/"
      );
      expect(result).toEqual(mockData);
    });
  });

  describe("fetchCompetitorsProfiles", () => {
    it("fetches competitors profiles from backend", async () => {
      const mockData = {
        nearby: [{ name: "Comp1" }],
        similar: [{ name: "Comp2" }],
      };
      axios.get.mockResolvedValueOnce({ data: mockData });

      const result = await api.fetchCompetitorsProfiles();

      expect(axios.get).toHaveBeenCalledWith(
        "http://localhost:8000/api/competitors/competitors/"
      );
      expect(result).toEqual(mockData);
    });
  });

  describe("streamProfileAssistant", () => {
    it("streams AI response and calls onChunk with each chunk", async () => {
      // Mock fetch and ReadableStream
      const mockChunks = ["Hello ", "World!"];
      const encoder = new TextEncoder();
      let chunkIndex = 0;

      const mockReader = {
        read: jest.fn().mockImplementation(() => {
          if (chunkIndex < mockChunks.length) {
            const value = encoder.encode(mockChunks[chunkIndex++]);
            return Promise.resolve({ value, done: false });
          }
          return Promise.resolve({ value: undefined, done: true });
        }),
      };

      global.fetch = jest.fn().mockResolvedValue({
        body: {
          getReader: () => mockReader,
        },
      });

      const onChunk = jest.fn();
      const question = "Test?";
      const model = "gpt-4.1-mini";

      const result = await api.streamProfileAssistant(question, model, onChunk);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/ai/profile-assistant/",
        expect.objectContaining({
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question, model }),
        })
      );
      expect(onChunk).toHaveBeenCalledTimes(2);
      expect(result).toBe("Hello World!");

      // Clean up
      delete global.fetch;
    });

    it("returns undefined if response.body is missing", async () => {
      global.fetch = jest.fn().mockResolvedValue({ body: null });
      const result = await api.streamProfileAssistant("Q", "M", jest.fn());
      expect(result).toBeUndefined();
      delete global.fetch;
    });
  });
});
