// TypeScript type definitions - All application types in one place
// This file will contain interfaces and types for chat, memories, API responses, and more

// Chat types
export interface ChatMessage {
  id?: number
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface ChatRequest {
  message: string
  includeMemories?: boolean
}

export interface ChatResponse {
  response: string
  relevantMemories: string[]
  timestamp: string
}

// Memory types
export interface Memory {
  id?: number
  memory_key: string
  memory_value: string
  priority: number
  created_at?: string
  updated_at?: string
}

export interface CreateMemoryRequest {
  memory_key: string
  memory_value: string
  priority: number
}

export interface UpdateMemoryRequest {
  memory_key: string
  memory_value: string
  priority: number
}

// API types
export interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
}

export interface ApiError {
  message: string
  status: number
  code?: string
}

export interface PaginationParams {
  page: number
  limit: number
  search?: string
}
