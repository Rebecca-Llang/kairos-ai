// API service layer - HTTP client and API endpoint functions
// This file will contain API configuration, base URL setup, and request/response handling
import { Memory } from '@/types'

const API_BASE_URL = 'http://localhost:8000/api'

export const apiClient = {
  chat: async (message: string, includeMemories: boolean) => {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, includeMemories }),
    })
    return response.json()
  },
  recentChatHistory: async () => {
    const response = await fetch(`${API_BASE_URL}/chat-history?limit=10`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  deleteChatHistory: async () => {
    const response = await fetch(`${API_BASE_URL}/chat-history`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  deleteChatMessage: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/chat-messages/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  memories: async () => {
    const response = await fetch(`${API_BASE_URL}/memories`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  addMemory: async (memory: Memory) => {
    const response = await fetch(`${API_BASE_URL}/memories`, {
      method: 'POST',
      body: JSON.stringify(memory),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  deleteMemory: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/memories/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  getMemoryById: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/memories/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  deleteMemories: async () => {
    const response = await fetch(`${API_BASE_URL}/memories`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
  stats: async () => {
    const response = await fetch(`${API_BASE_URL}/stats`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
}
