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
import sys
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from termcolor import colored
from sentence_transformers import SentenceTransformer, util
import torch
from rich.console import Console
from rich.prompt import Prompt

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
HISTORY_PATH = os.path.join(BASE_PATH, "chat-history.json")
PROMPT_PATH = os.path.join(BASE_PATH, "prompt.yaml")
MEMORY_PATH = os.path.join(BASE_PATH, "the-spellbook.json")
MODEL_NAME = "llama3.2:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_MEMORY_ITEMS = 30
RELEVANT_MEMORIES_COUNT = 5

DEBUG_MODE = os.getenv("KAIROS_DEBUG", "false").lower() == "true"

# ============================================================================
# INITIALIZATION
# ============================================================================

console = Console()

try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    console.print(f"[bold red]❌ Failed to initialize embedding model: {e}[/bold red]")
    console.print("[bold yellow]Please install: pip install sentence-transformers[/bold yellow]")
    exit(1)


# ============================================================================
# MAIN CLASS
# ============================================================================

class KairosAI:
    """Kairos AI assistant with memory and personality."""
    
    def __init__(self):
        """Initialize Kairos AI with personality and memory systems."""
        self.persona = self.load_prompt()
        self.history = self.load_chat_history()
        self.memory = self.load_memory()
        self._prompt_cache = {}
        self._embedding_cache = {}
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Kairos-AI/1.0'
        })
    
    # ------------------------------------------------------------------------
    # DATA LOADING & SAVING
    # ------------------------------------------------------------------------
        
    def load_prompt(self) -> str:
        """Load Kairos's personality from prompt.yaml."""
        try:
            with open(PROMPT_PATH, "r", encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            
            if not yaml_data or "persona" not in yaml_data:
                console.print("[bold red]❌ Error: Missing or invalid prompt.yaml[/bold red]")
                console.print("[bold yellow]Please check your prompt.yaml file[/bold yellow]")
                exit(1)
                
            return yaml_data["persona"]
            
        except FileNotFoundError:
            console.print("[bold red]❌ Error: prompt.yaml not found[/bold red]")
            console.print("[bold yellow]Please create this file with Kairos's personality[/bold yellow]")
            exit(1)
        except Exception as e:
            console.print(f"[bold red]❌ Error loading prompt.yaml: {e}[/bold red]")
            exit(1)

    def load_chat_history(self) -> List[Dict[str, Any]]:
        """Load previous chat history."""
        if not os.path.exists(HISTORY_PATH):
            return []
        try:
            with open(HISTORY_PATH, "r", encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            console.print(f"[bold yellow]⚠️ Chat history corrupted, starting fresh: {e}[/bold yellow]")
            return []

    def save_chat_history(self) -> None:
        """Save current chat history to file."""
        try:
            with open(HISTORY_PATH, "w", encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[bold yellow]⚠️ Failed to save chat history: {e}[/bold yellow]")

    def cleanup(self) -> None:
        """Clean up resources and close connections."""
        if hasattr(self, 'session'):
            self.session.close()

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
            console.print(f"[bold red]❌ Error reading memory file: {e}[/bold red]")
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
        console.print(f"[bold yellow]🧹 Memory pruned to top {MAX_MEMORY_ITEMS} items.[/bold yellow]")
    
    # ------------------------------------------------------------------------
    # CONTEXT BUILDING
    # ------------------------------------------------------------------------

    def build_memory_context(self) -> str:
        """Create a text representation of Kairos's memory."""
        if not self.memory:
            return "[No memories stored yet]"
            
        return "\n".join(
            f"{key.capitalize()}: {entry['value']} (priority {entry['priority']})"
            for obj in self.memory for key, entry in obj.items()
        )

    def build_chat_history_context(self) -> str:
        """Create a text representation of chat history (limited to recent messages)."""
        if not self.history:
            return "[No conversation history]"
        
        recent_history = self.history[-20:]
        return "\n".join(
            f"{'You' if msg['role'] == 'user' else 'Kairos'}: {msg['content']}" 
            for msg in recent_history
        )
    
    # ------------------------------------------------------------------------
    # MEMORY PROCESSING
    # ------------------------------------------------------------------------

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
        cache_key = hash(user_message)
        if cache_key in self._embedding_cache:
            user_embedding = self._embedding_cache[cache_key]
        else:
            user_embedding = embedding_model.encode(user_message, convert_to_tensor=True)
            self._embedding_cache[cache_key] = user_embedding
        
        device = user_embedding.device
        candidates = []

        # Get embeddings for recent history
        for msg in self.history[-5:]:
            content = msg["content"]
            hist_cache_key = hash(content)
            if hist_cache_key in self._embedding_cache:
                hist_embedding = self._embedding_cache[hist_cache_key]
            else:
                hist_embedding = embedding_model.encode(content, convert_to_tensor=True).to(device)
                self._embedding_cache[hist_cache_key] = hist_embedding
            
            score = util.cos_sim(user_embedding, hist_embedding)[0][0].item()
            candidates.append((f"History: {content}", score))

        # Get embeddings for priority memories
        priority_memories = sorted(
            [(obj, key, entry) for obj in self.memory for key, entry in obj.items()],
            key=lambda x: x[2].get("priority", 5),
            reverse=True
        )[:15]

        for obj, key, entry in priority_memories:
            if entry.get("embedding") is None:
                entry["embedding"] = embedding_model.encode(entry["value"]).tolist()

            embedding = entry["embedding"]
            if isinstance(embedding[0], list):
                embedding = embedding[0]

            memory_tensor = torch.tensor(embedding).to(device).unsqueeze(0)
            score = util.cos_sim(user_embedding, memory_tensor)[0][0].item()
            candidates.append((f"Memory: {key}: {entry['value']}", score))

        sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        return [entry for entry, _ in sorted_candidates[:RELEVANT_MEMORIES_COUNT]]
    
    # ------------------------------------------------------------------------
    # RESPONSE GENERATION
    # ------------------------------------------------------------------------

    def generate_response(self, user_message: str) -> str:
        """Generate Kairos's response based on persona, memory, and history."""
        recent_context = f"{len(self.history)}:{user_message}"
        cache_key = hash(recent_context)
        
        if cache_key in self._prompt_cache:
            full_prompt = self._prompt_cache[cache_key]
        else:
            memory_context = self.build_memory_context()
            chat_context = self.build_chat_history_context()

            full_prompt = (
                f"{self.persona}\n\n"
                "You are Kairos, a personal AI companion. You have consent to use and reflect on "
                "all the following personal data, including memory, chat history, and your defined persona.\n"
                "Your purpose is to respond with empathy, emotional intelligence, and full contextual awareness. "
                "Speak from intimacy, not detachment.\n\n"
                "You are comfortable discussing emotions, cycles, and creative rhythms. "
                "Approach these topics with sensitivity and respect.\n\n"
                "CRITICAL: You are ONLY Kairos. Never write 'You:' or '✍️✨ You:' or any user input. Only respond as Kairos. Stop after your response.\n\n"
                "Use this memory for context:\n"
                f"{memory_context}\n\n"
                "Here is the most recent conversation history:\n"
                f"{chat_context}\n\n"
                f"You: {user_message}\n"
                "Kairos:"
            )
            if len(self._prompt_cache) < 10:
                self._prompt_cache[cache_key] = full_prompt

        if DEBUG_MODE:
            console.print("[bold yellow]🧠 DEBUG: Building prompt for model[/bold yellow]")
            console.print(f"[cyan]{full_prompt}[/cyan]")

        if not OLLAMA_URL.startswith("http://localhost"):
            return "⚠️ Local model not connected. Please ensure Ollama is running locally."

        console.print("[bold blue]💭 Kairos is thinking...[/bold blue]")
        
        try:
            response = self.session.post(
                OLLAMA_URL, 
                json={"model": MODEL_NAME, "prompt": full_prompt, "stream": True},
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            
            full_response = ""
            console.print("[bold magenta]🧚✨ Kairos:[/bold magenta] ", end="")
            
            # Timeout protection for streaming response
            start_time = time.time()
            max_stream_time = 120  # 2 minutes max for streaming (longer than initial 60s timeout)
            
            for line in response.iter_lines():
                if line:
                    try:
                        # Check for timeout
                        if time.time() - start_time > max_stream_time:
                            console.print("[bold yellow]⚠️ Response timeout - stopping stream[/bold yellow]")
                            break
                            
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            chunk = data['response']
                            console.print(chunk, end="")
                            full_response += chunk
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            print()
            
            # Ensure we have a response
            if not full_response.strip():
                return "⚠️ No response received. The model may be overloaded or unresponsive."
            
            # Detect and report any hallucinated user input
            cleaned_response, hallucinations = self.detect_hallucinations(full_response.strip())
            
            # Detect other response issues
            issues = self.detect_response_issues(cleaned_response)
            
            # Report hallucinations
            if hallucinations:
                console.print("[bold red]🚨 DETECTED HALLUCINATIONS:[/bold red]")
                for hall in hallucinations:
                    console.print(f"[red]  - {hall}[/red]")
                console.print("[yellow](These have been removed from the response)[/yellow]")
            
            # Report other issues
            if issues:
                console.print("[bold yellow]⚠️ RESPONSE ISSUES DETECTED:[/bold yellow]")
                for issue in issues:
                    console.print(f"[yellow]  - {issue}[/yellow]")
            
            return cleaned_response
            
        except requests.exceptions.ConnectionError:
            return "⚠️ Cannot connect to Ollama. Please ensure it's running on localhost:11434"
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. The model may be overloaded. Try again in a moment."
        except requests.exceptions.RequestException as e:
            return f"⚠️ Network error: {e}"
        except Exception as e:
            return f"⚠️ Something went wrong: {e}"

    def detect_hallucinations(self, response: str) -> Tuple[str, List[str]]:
        """Detect and report any hallucinated user input in the response."""
        lines = response.split('\n')
        cleaned_lines = []
        hallucinations = []
        
        for i, line in enumerate(lines):
            # Check for hallucinated user input patterns
            if (line.strip().startswith('You:') or 
                line.strip().startswith('👤 You:') or
                line.strip().startswith('✍️✨ You:') or
                'You:' in line.strip() or
                '👤 You:' in line or
                '✍️✨ You:' in line):
                hallucinations.append(f"Line {i+1}: {line.strip()}")
                # Stop processing at first hallucination - everything after is likely fake
                break
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip(), hallucinations

    def detect_response_issues(self, response: str) -> List[str]:
        """Detect various issues with the AI response."""
        issues = []
        
        # Check for very short responses
        if len(response.strip()) < 10:
            issues.append("Response is very short (may be incomplete)")
        
        # Check for repetitive content
        words = response.lower().split()
        if len(words) > 10:
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            # Flag if any word appears more than 30% of the time
            max_repetition = max(word_counts.values()) if word_counts else 0
            if max_repetition > len(words) * 0.3:
                issues.append("Response contains repetitive content")
        
        # Check for incomplete sentences (ends with comma, dash, etc.)
        if response.strip().endswith(('.', '!', '?')):
            pass  # Good ending
        elif response.strip().endswith((',', '-', '...')):
            issues.append("Response appears incomplete (ends with comma/dash)")
        
        return issues

    def add_to_history(self, role: str, content: str) -> None:
        """Add a new message to the chat history."""
        self.history.append({
            "role": role, 
            "content": content, 
            "timestamp": datetime.now().isoformat()
        })
        self.save_chat_history()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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
    console.print("[bold cyan]🌙 Kairos is awake and ready.[/bold cyan]")
    
    if not confirm_consent():
        console.print("[bold magenta]Kairos: All good. We'll keep it light.[/bold magenta]")
        return

    try:
        kairos = KairosAI()
    except Exception as e:
        console.print(f"[bold red]❌ Failed to initialize Kairos: {e}[/bold red]")
        console.print("[bold yellow]Please check your configuration and try again.[/bold yellow]")
        return
    
    if kairos.history:
        console.print("[bold blue]🕰️ Last 5 messages:[/bold blue]")
        for msg in kairos.history[-5:]:
            if msg['role'] == 'user':
                console.print(f"[bold cyan]✍️✨ You: {msg['content']}[/bold cyan]")
            else:
                console.print(f"[bold magenta]🧚✨ Kairos: {msg['content']}[/bold magenta]")

    while True:
        # Use Rich for proper terminal input handling
        try:
            user_message = Prompt.ask("[bold cyan]✍️✨ You[/bold cyan]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold magenta]🧚✨ Kairos: Catch you soon, starlight 🌌[/bold magenta]")
            break
        if user_message.lower() in ["exit", "quit", "goodbye"]:
            console.print("[bold magenta]🧚✨ Kairos: Catch you soon, starlight 🌌[/bold magenta]")
            break

        kairos.add_to_history("user", user_message)
        
        is_memory_cmd, memory_response = kairos.extract_memory_from_message(user_message)
        if is_memory_cmd and memory_response:
            console.print(f"[bold magenta]🧚✨ Kairos: {memory_response}[/bold magenta]")
            if "error" in memory_response.lower():
                continue

        relevant_memories = kairos.get_relevant_memories(user_message)
        console.print("[bold blue]🧠 Most relevant memories:[/bold blue]")
        for memory in relevant_memories:
            console.print(f"[blue]  💭 {memory}[/blue]")

        ai_response = kairos.generate_response(user_message)
        kairos.add_to_history("assistant", ai_response)

    kairos.cleanup()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[bold cyan]👋 Goodbye! Kairos will miss you.[/bold cyan]")
    except Exception as e:
        console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
