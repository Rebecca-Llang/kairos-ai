// Utility functions - Helper functions and utilities
// This file will contain utility functions for formatting, validation, and common operations

export const formatTimestamp = (timestamp: string): string => {
  try {
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) {
      return 'Just now';
    }
    return date.toLocaleTimeString();
  } catch {
    return 'Just now';
  }
};

export const validateInput = (_input: string) => {
  // Input validation utility will be implemented here
  return true;
};
