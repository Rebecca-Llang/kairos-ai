// API service layer - HTTP client and API endpoint functions
// This file will contain API configuration, base URL setup, and request/response handling
import { Memory } from '@/types';
import { API_CONFIG } from '@/constants/config';

const API_BASE_URL = API_CONFIG.BASE_URL;

// Timeout configuration
const DEFAULT_TIMEOUT = API_CONFIG.TIMEOUTS.DEFAULT;
const CHAT_TIMEOUT = API_CONFIG.TIMEOUTS.CHAT;

// Helper function to create fetch with timeout
const fetchWithTimeout = async (
  url: string,
  options: RequestInit,
  timeout: number = DEFAULT_TIMEOUT
) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error(`Request timeout after ${timeout}ms`);
    }
    throw error;
  }
};

export const apiClient = {
  chat: async (message: string, includeMemories: boolean) => {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/chat`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, includeMemories }),
      },
      CHAT_TIMEOUT
    );
    return response.json();
  },
  recentChatHistory: async () => {
    const response = await fetch(`${API_BASE_URL}/chat-history?limit=10`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  deleteChatHistory: async () => {
    const response = await fetch(`${API_BASE_URL}/chat-history`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  deleteChatMessage: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/chat-history/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  memories: async () => {
    const response = await fetch(`${API_BASE_URL}/memories`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  addMemory: async (memory: Memory) => {
    const response = await fetch(`${API_BASE_URL}/memories`, {
      method: 'POST',
      body: JSON.stringify(memory),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  deleteMemory: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/memories/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  getMemoryById: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/memories/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  deleteMemories: async () => {
    const response = await fetch(`${API_BASE_URL}/memories`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  stats: async () => {
    const response = await fetch(`${API_BASE_URL}/stats`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
};
