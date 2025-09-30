// Memory service - API functions for memory operations
// This file will contain memory CRUD operations, search, and bulk actions

import { Memory } from '@/types'
import { apiClient } from './api'

export const memoryService = {
  getMemories: async () => {
    const response = await apiClient.memories()
    if (!response) {
      throw new Error('Failed to get memories')
    }

    return response
  },
  addMemory: async (memory: Memory) => {
    const response = await apiClient.addMemory(memory)
    if (!response) {
      throw new Error('Failed to add memory')
    }
    return response
  },
  deleteMemory: async (id: string) => {
    const response = await apiClient.deleteMemory(id)
    if (!response) {
      throw new Error('Failed to delete memory')
    }
    return response
  },
  getMemoryById: async (id: string) => {
    const response = await apiClient.getMemoryById(id)
    if (!response) {
      throw new Error('Failed to get memory by id')
    }
    return response
  },
  deleteMemories: async () => {
    const response = await apiClient.deleteMemories()
    if (!response) {
      throw new Error('Failed to delete memories')
    }
    return response
  },
}
