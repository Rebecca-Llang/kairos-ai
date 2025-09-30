#!/usr/bin/env python3
"""
Kairos AI - A personal AI companion with memory and contextual awareness.
"""
import os
import json
import yaml
import requests
import re
import time
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from termcolor import colored
from sentence_transformers import SentenceTransformer, util
import torch
from database.operations import (
    init_db,
    add_chat_message,
    get_chat_history,
    add_memory,
    get_memory_by_key,
    get_all_memories,
    clear_chat_history,
    delete_memory_by_key,
    get_database_stats,
)
from database.models import ChatMessage, SpellbookMemory

# Constants and Paths
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_PATH))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "kairos.db")
PROMPT_PATH = os.path.join(PROJECT_ROOT, "config", "prompt.yaml")
SCHEMA_PATH = os.path.join(BASE_PATH, "database", "schema.sql")
MODEL_NAME = "llama3.2"  # Try "phi4-mini" or "qwen2.5:3b" for faster responses
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_MEMORY_ITEMS = 30
RELEVANT_MEMORIES_COUNT = 5

DEBUG_MODE = os.getenv("KAIROS_DEBUG", "false").lower() == "true"
try:
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    print(colored(f"❌ Failed to initialize embedding model: {e}", "red"))
    print(colored("Please install: pip install sentence-transformers", "yellow"))
    exit(1)


class KairosAI:
    """Kairos AI assistant with memory and personality."""

    def __init__(self):
        """Initialize Kairos AI with personality and memory systems."""
        if not init_db(DB_PATH, SCHEMA_PATH):
            print(colored("❌ Failed to initialize database", "red"))
            exit(1)

        self.persona = self.load_prompt()
        self.history = self.load_chat_history()
        self.memory = self.load_memory()

    def load_prompt(self) -> str:
        """Load Kairos's personality from prompt.yaml."""
        try:
            with open(PROMPT_PATH, "r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f)

            if not yaml_data or "persona" not in yaml_data:
                print(colored("❌ Error: Missing or invalid prompt.yaml", "red"))
                print(colored("Please check your prompt.yaml file", "yellow"))
                exit(1)

            return yaml_data["persona"]

        except FileNotFoundError:
            print(colored("❌ Error: prompt.yaml not found", "red"))
            print(
                colored("Please create this file with Kairos's personality", "yellow")
            )
            exit(1)
        except Exception as e:
            print(colored(f"❌ Error loading prompt.yaml: {e}", "red"))
            exit(1)

    def load_chat_history(self) -> List[Dict[str, Any]]:
        """Load previous chat history from database."""
        try:
            return get_chat_history(db_path=DB_PATH)
        except Exception as e:
            print(colored(f"⚠️ Chat history corrupted, starting fresh: {e}", "yellow"))
            return []

    def save_chat_message(self, role: str, content: str) -> None:
        """Save a single chat message to database."""
        try:
            add_chat_message(role=role, content=content, db_path=DB_PATH)
        except Exception as e:
            print(colored(f"⚠️ Failed to save chat message: {e}", "yellow"))

    def load_memory(self) -> List[Dict[str, Any]]:
        """Load Kairos's memory from database."""
        try:
            memories = get_all_memories(db_path=DB_PATH)
            # Convert database format to expected format
            formatted_memories = []
            for memory in memories:
                formatted_memories.append(
                    {
                        memory["memory_key"]: {
                            "value": memory["memory_value"],
                            "priority": memory["priority"],
                            "embedding": memory.get("embedding"),
                        }
                    }
                )
            return formatted_memories
        except Exception as e:
            print(colored(f"⚠️ Memory corrupted, starting fresh: {e}", "yellow"))
            return []

    def save_memory(
        self,
        memory_key: str,
        memory_value: str,
        priority: int = 5,
        embedding: Optional[List[float]] = None,
    ) -> None:
        """Save a single memory to database."""
        try:
            add_memory(
                memory_key=memory_key,
                memory_value=memory_value,
                priority=priority,
                embedding=embedding,
                db_path=DB_PATH,
            )
        except Exception as e:
            print(colored(f"⚠️ Failed to save memory: {e}", "yellow"))

    def prune_memory(self) -> None:
        """Keep only the highest priority memory items if exceeded max limit."""
        if len(self.memory) <= MAX_MEMORY_ITEMS:
            return

        self.memory.sort(key=lambda x: list(x.values())[0].get("priority", 5))
        self.memory = self.memory[-MAX_MEMORY_ITEMS:]
        print(colored(f"🧹 Memory pruned to top {MAX_MEMORY_ITEMS} items.", "yellow"))

    def build_memory_context(self) -> str:
        """Create a text representation of Kairos's memory (limited for performance)."""
        if not self.memory:
            return "[No memories stored yet]"

        # Limit to top 10 memories by priority to prevent prompt bloat
        sorted_memories = sorted(
            self.memory,
            key=lambda x: list(x.values())[0].get("priority", 5),
            reverse=True,
        )[:10]

        return "\n".join(
            f"{key.capitalize()}: {entry['value']} (priority {entry['priority']})"
            for obj in sorted_memories
            for key, entry in obj.items()
        )

    def build_chat_history_context(self) -> str:
        """Create a text representation of chat history (limited to recent messages)."""
        if not self.history:
            return "[No conversation history]"

        # Limit to last 10 messages to prevent prompt bloat
        recent_history = self.history[-10:]
        return "\n".join(
            f"{'You' if msg['role'] == 'user' else 'Kairos'}: {msg['content']}"
            for msg in recent_history
        )

    def extract_memory_from_message(
        self, user_message: str
    ) -> Tuple[bool, Optional[str]]:
        """Extract memory commands from user messages."""
        match = re.match(
            r'remember:\s*\"(?P<key>[^"]+)\"\s*\"(?P<value>[^"]+)\"(?:\s*priority:(?P<priority>\d+))?',
            user_message,
            re.IGNORECASE,
        )

        if not match:
            if "remember:" in user_message:
                return (
                    True,
                    '⚠️ Format error. Use: remember: "your_key_name" "memory and details here" priority:7',
                )
            return False, None

        key = match.group("key").strip().lower()
        value = match.group("value").strip()
        priority = int(match.group("priority") or 5)
        embedding = embedding_model.encode(value).tolist()

        # Save memory to database
        self.save_memory(key, value, priority, embedding)

        # Update local memory for immediate use
        existing = next((item for item in self.memory if key in item), None)
        if existing:
            existing[key] = {
                "value": value,
                "priority": priority,
                "embedding": embedding,
            }
        else:
            self.memory.append(
                {key: {"value": value, "priority": priority, "embedding": embedding}}
            )

        self.prune_memory()
        return (
            True,
            f"Got it. I'll remember your {key} is {value} (priority {priority}).",
        )

    def get_relevant_memories(self, user_message: str) -> List[str]:
        """Find relevant memories and history for the current message."""
        user_embedding = embedding_model.encode(user_message, convert_to_tensor=True)
        device = user_embedding.device
        candidates = []

        # Get embeddings for history items
        for msg in self.history[-10:]:  # Limit to recent history for efficiency
            content = msg["content"]
            hist_embedding = embedding_model.encode(content, convert_to_tensor=True).to(
                device
            )
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

    def generate_response(self, user_message: str, include_memories: bool = True) -> str:
        """Generate Kairos's response based on persona, memory, and history."""
        memory_context = self.build_memory_context() if include_memories else "[Memories disabled]"
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
            f"Use this memory for context:\n"
            f"{memory_context}\n\n"
            "Here is the most recent conversation history:\n"
            f"{chat_context}\n\n"
            f"You: {user_message}\n"
            "Kairos:"
        )

        # Debug output - only show in debug mode
        if DEBUG_MODE:
            print(colored("🧠 DEBUG: Building prompt for model", "yellow"))
            print(colored(full_prompt, "cyan"))

        if not OLLAMA_URL.startswith("http://localhost"):
            return (
                "⚠️ Local model not connected. Please ensure Ollama is running locally."
            )

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False},
                timeout=60,
            )
            response.raise_for_status()
            return response.json()["response"].strip()

        except requests.exceptions.ConnectionError:
            return "⚠️ Cannot connect to Ollama. Please ensure it's running on localhost:11434"
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. Try reducing chat history or using a smaller model."
        except requests.exceptions.RequestException as e:
            return f"⚠️ Network error: {e}"
        except Exception as e:
            return f"⚠️ Something went wrong: {e}"

    def add_to_history(self, role: str, content: str) -> None:
        """Add a new message to the chat history."""
        # Add to local history for immediate use
        self.history.append(
            {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
        )
        # Save to database
        self.save_chat_message(role, content)


def handle_db_command(command: str, kairos: KairosAI) -> None:
    """Handle database management commands."""
    cmd = command.lower().strip()

    if cmd == "db:stats":
        stats = get_database_stats(DB_PATH)
        print(colored("📊 Database Statistics:", "yellow"))
        print(colored(f"  Chat messages: {stats.get('chat_history_count', 0)}", "cyan"))
        print(
            colored(f"  Memories: {stats.get('spellbook_memories_count', 0)}", "cyan")
        )

    elif cmd == "db:clear_chat":
        if clear_chat_history(DB_PATH):
            kairos.history = []
            print(colored("✅ Chat history cleared", "green"))
        else:
            print(colored("❌ Failed to clear chat history", "red"))

    elif cmd.startswith("db:delete_memory "):
        memory_key = cmd.replace("db:delete_memory ", "").strip()
        if delete_memory_by_key(memory_key, DB_PATH):
            # Remove from local memory
            kairos.memory = [item for item in kairos.memory if memory_key not in item]
            print(colored(f"✅ Memory '{memory_key}' deleted", "green"))
        else:
            print(colored(f"❌ Failed to delete memory '{memory_key}'", "red"))

    elif cmd == "db:help":
        print(colored("🗄️ Database Commands:", "yellow"))
        print(colored("  db:stats - Show database statistics", "cyan"))
        print(colored("  db:clear_chat - Clear all chat history", "cyan"))
        print(colored("  db:delete_memory <key> - Delete specific memory", "cyan"))
        print(colored("  db:help - Show this help", "cyan"))

    else:
        print(
            colored(
                "❌ Unknown database command. Use 'db:help' for available commands.",
                "red",
            )
        )


def confirm_consent() -> bool:
    """Get user consent for Kairos to access personal data."""
    # Skip consent prompt in development mode
    if os.getenv('KAIROS_DEV_MODE') == 'true':
        print(colored("Development mode: Auto-granting consent", "green"))
        return True

    consent = input(
        colored(
            "Do you give Kairos consent to access and reflect on your stored data "
            "(e.g., emotions, memories, relationships)? (yes/no): ",
            "yellow",
        )
    )
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
        print(colored("Please check your configuration and try again.", "yellow"))
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

        # Database management commands
        if user_message.lower().startswith("db:"):
            handle_db_command(user_message, kairos)
            continue

        # Add user message to history
        kairos.add_to_history("user", user_message)

        # Check for memory commands
        is_memory_cmd, memory_response = kairos.extract_memory_from_message(
            user_message
        )
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
