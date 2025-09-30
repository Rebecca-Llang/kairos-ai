import { useState, useEffect, useCallback } from 'react';
import { chatService } from '@/services/chatService';
import { ChatMessage, ChatResponse } from '@/types';

// Chat functionality hook
export const useChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [includeMemories, setIncludeMemories] = useState(false);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isSending) return;

      setIsSending(true);
      setIsThinking(false);
      setError(null);

      const userMessage: ChatMessage = {
        id: `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        role: 'user',
        content: content.trim(),
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, userMessage]);

      try {
        // User message sent, now Kairos is thinking
        setIsThinking(true);

        const response: ChatResponse = await chatService.sendMessage(
          content.trim(),
          includeMemories
        );

        const aiMessage: ChatMessage = {
          id: `ai-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          role: 'assistant',
          content: response.response,
          timestamp: response.timestamp,
        };
        setMessages(prev => [...prev, aiMessage]);
      } catch (error) {
        console.error('Chat error:', error);
        const errorMessage =
          error instanceof Error ? error.message : 'Unknown error';
        setError(errorMessage);

        // Add an error message from Kairos instead of removing the user message
        const errorResponse: ChatMessage = {
          id: `error-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          role: 'assistant',
          content: `I'm sorry, I'm having trouble connecting right now. Error: ${errorMessage}. Please check if the backend server is running.`,
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, errorResponse]);
      } finally {
        setIsSending(false);
        setIsThinking(false);
      }
    },

    [isSending, includeMemories]
  );

  const loadChatHistory = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await chatService.getChatHistory();
      setMessages(response.data || []);
    } catch (error) {
      setError(
        error instanceof Error ? error.message : 'Failed to load chat history'
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadChatHistory();
  }, [loadChatHistory]);

  // Utility functions
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const canSend = useCallback(
    (content: string) => {
      return content.trim().length > 0 && !isSending;
    },
    [isSending]
  );

  return {
    // State
    messages,
    isLoading,
    isSending,
    isThinking,
    error,
    includeMemories,

    // Actions
    sendMessage,
    loadChatHistory,
    setIncludeMemories,
    clearError,

    // Utilities
    canSend,
  };
};

// Memory management hook
export const useMemories = () => {
  // Memory management will be implemented here
  return {};
};

// Memory search hook
export const useMemorySearch = () => {
  // Memory search will be implemented here
  return {};
};

// Theme management hook
export const useTheme = () => {
  // Theme management will be implemented here
  return {};
};

export { useNavigation } from './useNavigation';
