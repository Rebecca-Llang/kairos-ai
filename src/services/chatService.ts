// Chat service - API functions for chat operations
// This file will contain chat-related API calls, message sending, and history management

import { apiClient } from './api'

export const chatService = {
  sendMessage: async (message: string, includeMemories: boolean) => {
    const response = await apiClient.chat(message, includeMemories)
    return response
  },
  getChatHistory: async () => {
    const response = await apiClient.recentChatHistory()
    return response
  },
  getRecentChatHistory: async () => {
    const response = await apiClient.recentChatHistory()
    return response
  },
  deleteChatHistory: async () => {
    const response = await apiClient.deleteChatHistory()
    return response
  },
  deleteChatMessage: async (id: string) => {
    const response = await apiClient.deleteChatMessage(id)
    return response
  },
}
