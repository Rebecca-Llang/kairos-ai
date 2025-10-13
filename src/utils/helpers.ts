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

export const formatMemoryKey = (memoryKey: string): string => {
  return memoryKey
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

export const normalizeMemoryKey = (key: string): string => {
  return key
    .trim() // Remove leading/trailing whitespace
    .toLowerCase() // Convert to lowercase
    .replace(/\s+/g, '_') // Replace spaces with underscores
    .replace(/[^a-z0-9_]/g, '') // Remove special characters except underscores
    .replace(/_+/g, '_') // Replace multiple underscores with single underscore
    .replace(/^_|_$/g, ''); // Remove leading/trailing underscores
};
