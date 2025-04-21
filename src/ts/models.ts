export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: string; // ISO 8601 format
}

export interface Memory {
  [key: string]: string | string[]; // Key-value pairs for memory
}

export interface AIResponse {
  response: string;
}
