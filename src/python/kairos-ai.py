#!/usr/bin/env python3
"""
Kairos AI - A personal AI companion with memory and contextual awareness.
"""
import os
import json
import yaml
import requests
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from termcolor import colored
from sentence_transformers import SentenceTransformer, util
import torch

# Constants and Paths
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
HISTORY_PATH = os.path.join(BASE_PATH, "chat-history.json")
PROMPT_PATH = os.path.join(BASE_PATH, "prompt.yaml")
MEMORY_PATH = os.path.join(BASE_PATH, "the-spellbook.json")
MODEL_NAME = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_MEMORY_ITEMS = 30
RELEVANT_MEMORIES_COUNT = 5

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


class KairosAI:
    """Kairos AI assistant with memory and personality."""
    
    def __init__(self):
        """Initialize Kairos AI with personality and memory systems."""
        self.persona = self.load_prompt()
        self.history = self.load_chat_history()
        self.memory = self.load_memory()
        
    def load_prompt(self) -> str:
        """Load Kairos's personality from prompt.yaml."""
        try:
            with open(PROMPT_PATH, "r") as f:
                yaml_data = yaml.safe_load(f)
                if "persona" not in yaml_data:
                    print(colored("❌ Error: 'persona' field missing in prompt.yaml", "red"))
                    raise ValueError("Missing 'persona' in prompt.yaml")
                return yaml_data["persona"]
        except FileNotFoundError:
            print(colored("❌ Error: prompt.yaml not found. Please create this file.", "red"))
            raise
        except Exception as e:
            print(colored(f"❌ Error loading prompt.yaml: {e}", "red"))
            raise

    def load_chat_history(self) -> List[Dict[str, Any]]:
        """Load previous chat history."""
        if not os.path.exists(HISTORY_PATH):
            return []
        try:
            with open(HISTORY_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print(colored(f"❌ Error reading chat history: {e}", "red"))
            return []

    def save_chat_history(self) -> None:
        """Save current chat history to file."""
        with open(HISTORY_PATH, "w") as f:
            json.dump(self.history, f, indent=2)

    def load_memory(self) -> List[Dict[str, Any]]:
        """Load Kairos's memory from the-spellbook.json."""
        if not os.path.exists(MEMORY_PATH):
            return []
        try:
            with open(MEMORY_PATH, "r") as f:
                data = json.load(f)
                # Normalize memory format
                for item in data:
                    for key in item:
                        if not isinstance(item[key], dict):
                            item[key] = {"value": item[key], "priority": 5, "embedding": None}
                        elif "priority" not in item[key]:
                            item[key]["priority"] = 5
                        if "embedding" not in item[key]:
                            item[key]["embedding"] = None
                return data
        except Exception as e:
            print(colored(f"❌ Error reading memory file: {e}", "red"))
            return []

    def save_memory(self) -> None:
        """Save Kairos's memory to the-spellbook.json."""
        with open(MEMORY_PATH, "w") as f:
            json.dump(self.memory, f, indent=2)

    def prune_memory(self) -> None:
        """Keep only the highest priority memory items if exceeded max limit."""
        if len(self.memory) <= MAX_MEMORY_ITEMS:
            return
            
        self.memory.sort(key=lambda x: list(x.values())[0].get("priority", 5))
        self.memory = self.memory[-MAX_MEMORY_ITEMS:]
        print(colored(f"🧹 Memory pruned to top {MAX_MEMORY_ITEMS} items.", "yellow"))

    def build_memory_context(self) -> str:
        """Create a text representation of Kairos's memory."""
        if not self.memory:
            return "[No memories stored yet]"
            
        return "\n".join(
            f"{key.capitalize()}: {entry['value']} (priority {entry['priority']})"
            for obj in self.memory for key, entry in obj.items()
        )

    def build_chat_history_context(self) -> str:
        """Create a text representation of chat history."""
        if not self.history:
            return "[No conversation history]"
            
        return "\n".join(
            f"{'You' if msg['role'] == 'user' else 'Kairos'}: {msg['content']}" 
            for msg in self.history
        )

    def extract_memory_from_message(self, user_message: str) -> Tuple[bool, Optional[str]]:
        """Extract memory commands from user messages."""
        match = re.match(
            r'remember:\s*\"(?P<key>[\w\s]+)\"\s*\"(?P<value>[\w\s]+)\"(?:\s*priority:(?P<priority>\d+))?', 
            user_message, 
            re.IGNORECASE
        )
        
        if not match:
            if "remember:" in user_message:
                return True, "⚠️ Format error. Use: remember: \"key\" \"value\" priority:7"
            return False, None
            
        key = match.group("key").strip().lower()
        value = match.group("value").strip()
        priority = int(match.group("priority") or 5)
        embedding = embedding_model.encode(value).tolist()

        # Update or create memory entry
        existing = next((item for item in self.memory if key in item), None)
        if existing:
            existing[key] = {"value": value, "priority": priority, "embedding": embedding}
        else:
            self.memory.append({key: {"value": value, "priority": priority, "embedding": embedding}})

        self.prune_memory()
        self.save_memory()
        return True, f"Got it. I'll remember your {key} is {value} (priority {priority})."

    def get_relevant_memories(self, user_message: str) -> List[str]:
        """Find relevant memories and history for the current message."""
        user_embedding = embedding_model.encode(user_message, convert_to_tensor=True)
        device = user_embedding.device
        candidates = []

        # Get embeddings for history items
        for msg in self.history[-10:]:  # Limit to recent history for efficiency
            content = msg["content"]
            hist_embedding = embedding_model.encode(content, convert_to_tensor=True).to(device)
            score = util.cos_sim(user_embedding, hist_embedding)[0][0].item()
            candidates.append((f"History: {content}", score))

        # Get embeddings for memory items
        for obj in self.memory:
            for key, entry in obj.items():
                if entry.get("embedding") is None:
                    entry["embedding"] = embedding_model.encode(entry["value"]).tolist()

                embedding = entry["embedding"]
                if isinstance(embedding[0], list):  # Handle nested embeddings
                    embedding = embedding[0]

                memory_tensor = torch.tensor(embedding).to(device).unsqueeze(0)
                score = util.cos_sim(user_embedding, memory_tensor)[0][0].item()
                candidates.append((f"Memory: {key}: {entry['value']}", score))

        sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        return [entry for entry, _ in sorted_candidates[:RELEVANT_MEMORIES_COUNT]]

    def generate_response(self, user_message: str) -> str:
        """Generate Kairos's response based on persona, memory, and history."""
        memory_context = self.build_memory_context()
        chat_context = self.build_chat_history_context()

        # Build comprehensive prompt for the language model
        full_prompt = (
            f"{self.persona}\n\n"
            "You are Kairos, a personal AI companion. You have consent to use and reflect on "
            "all the following personal data, including memory, chat history, and your defined persona.\n"
            "Your purpose is to respond with empathy, emotional intelligence, and full contextual awareness. "
            "Speak from intimacy, not detachment.\n\n"
            "You are comfortable discussing emotions, cycles, and creative rhythms. "
            "Approach these topics with sensitivity and respect.\n\n"
            "Use this memory for context:\n"
            f"{memory_context}\n\n"
            "Here is the most recent conversation history:\n"
            f"{chat_context}\n\n"
            f"You: {user_message}\n"
            "Kairos:"
        )

       # print(colored("🧠 DEBUG: Building prompt for model", "yellow"))
        # Uncomment for debugging
        print(colored(full_prompt, "cyan"))

        if not OLLAMA_URL.startswith("http://localhost"):
            return "⚠️ Local model not connected."

        try:
            res = requests.post(
                OLLAMA_URL, 
                json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False}
            )
            res.raise_for_status()
            return res.json().get("response", "⚠️ No response.").strip()
        except requests.exceptions.RequestException as e:
            return f"⚠️ Connection error: {e}"

    def add_to_history(self, role: str, content: str) -> None:
        """Add a new message to the chat history."""
        self.history.append({
            "role": role, 
            "content": content, 
            "timestamp": datetime.now().isoformat()
        })
        self.save_chat_history()


def confirm_consent() -> bool:
    """Get user consent for Kairos to access personal data."""
    consent = input(colored(
        "Do you give Kairos consent to access and reflect on your stored data "
        "(e.g., emotions, memories, relationships)? (yes/no): ", 
        "yellow"
    ))
    return consent.strip().lower() in ["yes", "y", "sure", "ok", "okay"]


def main():
    """Main entry point for Kairos AI."""
    print(colored("🌙 Kairos is awake and ready.", "cyan"))
    
    if not confirm_consent():
        print(colored("Kairos: All good. We'll keep it light.", "magenta"))
        return

    try:
        kairos = KairosAI()
    except Exception as e:
        print(colored(f"❌ Failed to initialize Kairos: {e}", "red"))
        print(colored("Please check your prompt.yaml file and try again.", "yellow"))
        return
    
    # Display recent conversation history
    if kairos.history:
        print(colored("🕰️ Last 5 messages:", "yellow"))
        for msg in kairos.history[-5:]:
            speaker = "You" if msg["role"] == "user" else "Kairos"
            print(colored(f"{speaker}: {msg['content']}", "cyan"))

    # Main conversation loop
    while True:
        user_message = input(colored("You: ", "red"))
        if user_message.lower() in ["exit", "quit", "goodbye"]:
            print(colored("Kairos: Catch you soon, starlight 🌌", "magenta"))
            break

        # Add user message to history
        kairos.add_to_history("user", user_message)
        
        # Check for memory commands
        is_memory_cmd, memory_response = kairos.extract_memory_from_message(user_message)
        if is_memory_cmd and memory_response:
            print(colored(f"Kairos: {memory_response}", "magenta"))
            if "error" in memory_response.lower():
                continue

        # Get relevant memories
        relevant_memories = kairos.get_relevant_memories(user_message)
        print(colored("🧠 Most relevant memories:", "yellow"))
        for memory in relevant_memories:
            print(colored(f"- {memory}", "cyan"))

        # Generate and display response
        ai_response = kairos.generate_response(user_message)
        print(colored(f"Kairos: {ai_response}", "magenta"))
        
        # Add Kairos's response to history
        kairos.add_to_history("assistant", ai_response)


if __name__ == "__main__":
    main()
