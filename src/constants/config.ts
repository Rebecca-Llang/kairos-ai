// API Configuration
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/api',
  TIMEOUTS: {
    DEFAULT: 30000, // 30 seconds
    CHAT: 60000, // 60 seconds for AI responses
  },
} as const;

// App Configuration
export const APP_CONFIG = {
  MAX_MESSAGE_LENGTH: 1000,
  DEFAULT_MEMORY_PRIORITY: 5,
} as const;
