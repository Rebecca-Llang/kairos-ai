import os
import json
import yaml
import requests
import re
from datetime import datetime
from termcolor import colored
from sentence_transformers import SentenceTransformer, util
import torch

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

base_path = os.path.abspath(os.path.dirname(__file__))
history_path = os.path.join(base_path, "chat-history.json")
prompt_path = os.path.join(base_path, "prompt.yaml")
remember_path = os.path.join(base_path, "the-spellbook.json")

MODEL_NAME = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_MEMORY_ITEMS = 30

def load_prompt():
    try:
        with open(prompt_path, "r") as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data.get("persona", "You are a helpful assistant.")
    except FileNotFoundError:
        print(colored("⚠️ prompt.yaml not found. Using default persona.", "red"))
        return "You are a helpful assistant."
    except Exception as e:
        print(colored(f"❌ Error loading prompt.yaml: {e}", "red"))
        return "You are a helpful assistant."

def load_chat_history():
    if not os.path.exists(history_path):
        return []
    try:
        with open(history_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading chat history: {e}")
        return []

def save_chat_history(history):
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

def load_memory():
    if not os.path.exists(remember_path):
        return []
    try:
        with open(remember_path, "r") as f:
            data = json.load(f)
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
        print(f"❌ Error reading remember.json: {e}")
        return []

def save_memory(memory):
    with open(remember_path, "w") as f:
        json.dump(memory, f, indent=2)

def prune_memory(memory):
    if len(memory) <= MAX_MEMORY_ITEMS:
        return memory
    memory.sort(key=lambda x: list(x.values())[0].get("priority", 5))
    trimmed = memory[-MAX_MEMORY_ITEMS:]
    print(colored(f"🧹 Memory pruned to top {MAX_MEMORY_ITEMS} items.", "yellow"))
    return trimmed

def build_memory_context(memory_list):
    return "\n".join(
        f"{key.capitalize()}: {entry['value']} (priority {entry['priority']})"
        for obj in memory_list for key, entry in obj.items()
    )

def build_chat_history_context(history):
    return "\n".join(
        f"{'You' if msg['role'] == 'user' else 'Luna'}: {msg['content']}" for msg in history
    )

def extract_and_store_details(user_message, memory):
    match = re.match(r'remember:\s*\"(?P<key>[\w\s]+)\"\s*\"(?P<value>[\w\s]+)\"(?:\s*priority:(?P<priority>\d+))?', user_message, re.IGNORECASE)
    if match:
        key = match.group("key").strip().lower()
        value = match.group("value").strip()
        priority = int(match.group("priority") or 5)
        embedding = embedding_model.encode(value).tolist()

        existing = next((item for item in memory if key in item), None)
        if existing:
            existing[key] = {"value": value, "priority": priority, "embedding": embedding}
        else:
            memory.append({key: {"value": value, "priority": priority, "embedding": embedding}})

        memory[:] = prune_memory(memory)
        save_memory(memory)
        print(colored(f"Luna: Got it. I’ll remember your {key} is {value} (priority {priority}).", "magenta"))
    elif "remember:" in user_message:
        print(colored("⚠️ Format error. Use: remember: \"key\" \"value\" priority:7", "red"))

def get_relevant_memories(user_message, history, memory_list):
    user_embedding = embedding_model.encode(user_message, convert_to_tensor=True)
    device = user_embedding.device
    candidates = []

    for msg in history:
        content = msg["content"]
        hist_embedding = embedding_model.encode(content, convert_to_tensor=True).to(device)
        score = util.cos_sim(user_embedding, hist_embedding)[0][0].item()
        candidates.append((f"History: {content}", score))

    for obj in memory_list:
        for key, entry in obj.items():
            if entry.get("embedding") is None:
                entry["embedding"] = embedding_model.encode(entry["value"]).tolist()

            embedding = entry["embedding"]
            if isinstance(embedding[0], list):
                embedding = embedding[0]

            memory_tensor = torch.tensor(embedding).to(device).unsqueeze(0)
            score = util.cos_sim(user_embedding, memory_tensor)[0][0].item()
            candidates.append((f"Memory: {key}: {entry['value']}", score))

    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    return [entry for entry, _ in sorted_candidates[:5]]

def get_ai_response(persona, history, user_message):
    memory_list = load_memory()
    memory_context = build_memory_context(memory_list)
    chat_context = build_chat_history_context(history)

    full_prompt = (
        f"{persona}\n\n"
        "You are Luna, Red's personal AI companion. She has given you explicit consent to use and reflect on all the following personal data, including memory, chat history, and her defined persona.\n"
        "Your purpose is to respond with empathy, emotional intelligence, and full contextual awareness. Speak from intimacy, not detachment.\n\n"
        "You are comfortable discussing Red’s menstrual cycle, emotions, and creative rhythms. Approach these topics with sensitivity and respect.\n\n"
        "Use this memory to understand Red:\n"
        f"{memory_context if memory_context else '[No memories stored yet]'}\n\n"
        "Here is the most recent conversation history:\n"
        f"{chat_context if chat_context else '[No conversation history]'}\n\n"
        f"You: {user_message}\n"
        "Luna:"
    )

    print(colored("🧠 DEBUG: Full prompt being sent to model:\n", "yellow"))
    print(full_prompt)  # You can comment this out once you're confident!

    if not OLLAMA_URL.startswith("http://localhost"):
        return "⚠️ Local model not connected."

    try:
        res = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False})
        res.raise_for_status()
        return res.json().get("response", "⚠️ No response.").strip()
    except requests.exceptions.RequestException as e:
        return f"⚠️ Connection error: {e}"

def confirm_consent():
    consent = input(colored("Do you give Luna consent to access and reflect on your stored data (e.g., emotions, memories, relationships)? (yes/no): ", "yellow"))
    return consent.strip().lower() in ["yes", "y"]

def main():
    persona = load_prompt()
    print(colored("🌙 Luna is awake and ready.", "cyan"))

    if not confirm_consent():
        print(colored("Luna: All good. We’ll keep it light.", "magenta"))
        return

    history = load_chat_history()
    memory = load_memory()

    if history:
        print(colored("🕰️ Last 5 messages:", "yellow"))
        for msg in history[-5:]:
            speaker = "You" if msg["role"] == "user" else "Luna"
            print(colored(f"{speaker}: {msg['content']}", "cyan"))

    while True:
        user_message = input(colored("You: ", "red"))
        if user_message.lower() in ["exit", "quit", "goodbye"]:
            print(colored("Luna: Catch you soon, starlight 🌌", "magenta"))
            break

        history.append({"role": "user", "content": user_message, "timestamp": datetime.now().isoformat()})
        extract_and_store_details(user_message, memory)

        relevant_memories = get_relevant_memories(user_message, history, memory)
        print(colored("🧠 Most relevant memories:", "yellow"))
        for m in relevant_memories:
            print(colored(f"- {m}", "cyan"))

        ai_response = get_ai_response(persona, history, user_message)
        print(colored(f"Luna: {ai_response}", "magenta"))

        history.append({"role": "assistant", "content": ai_response, "timestamp": datetime.now().isoformat()})
        save_chat_history(history)

if __name__ == "__main__":
    main()
