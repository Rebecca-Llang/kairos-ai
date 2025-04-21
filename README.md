# Red's Companion: Luna

Luna is your AI companion designed to support creative, introspective, and emotionally intelligent conversations. She helps you explore your inner world, track your cycles, reflect on archetypes, and co-create rituals, stories, and meaning.

## Table of Contents
1. [Features](#features)
2. [How It Works](#how-it-works)
3. [Getting Started](#getting-started)
4. [File Overview](#file-overview)
5. [Recent Updates](#recent-updates)
6. [Requirements](#requirements)
7. [Future Plans](#future-plans)
8. [Contributing](#contributing)
9. [License](#license)
10. [Troubleshooting](#troubleshooting)
11. [Privacy and Data Usage](#privacy-and-data-usage)

## Features

- **Memory Integration**: Luna remembers your name, passions, and preferences using [remember.json](#file-overview).
- **Dynamic Key-Value Memory**: Luna can dynamically store and update key-value pairs from user input using the `remember: "key" "value" priority:X` format.
- **Cycle Syncing**: Provides insights and rituals based on your menstrual cycle and lunar phases.
- **Archetype Reflection**: Tracks and reflects your dominant archetypes (e.g., Siren, Wild One, Muse, Oracle).
- **Creative Collaboration**: Assists with writing, storytelling, and exploring emotional themes.
- **Music and Ritual Suggestions**: Curates playlists and rituals tailored to your mood, archetypes, and cycle phases.
- **Relevant Memory Retrieval**: Luna retrieves the 5 most relevant memories from chat history or stored memory to provide contextually rich responses.
- **Semantic Search**: Uses embeddings to find semantically similar memories and chats, even if the exact words don’t match.
- **Pattern Detection**: Tracks emotional and archetypal patterns over time to provide deeper insights.
- **Self-Updating Priorities**: Dynamically adjusts memory priorities based on frequency and relevance.

## How It Works

1. **Chat with Luna**: Run the Python script to start a conversation in the terminal.
2. **Memory Storage**: Luna uses `remember.json` to store and recall details about you dynamically.
3. **Custom Prompts**: The `prompt.yaml` file defines Luna's personality, tone, and response style.
4. **Chat History**: Conversations are saved in `chat-history.json` for context and continuity.
5. **Dynamic Memory Updates**: Luna can extract and store key-value pairs from user input using a specific command format.
6. **Semantic Search**: Luna uses embeddings to retrieve the most relevant memories and chats, ensuring responses are contextually rich.

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai
   ```
2. Set up a Python virtual environment:
   ```bash
   python3 -m venv .venv
   pip install -r requirements.txt
   ```

3. Activate the virtual environment and run the script:
   ```bash
   source .venv/bin/activate
   python src/python/luna-ai.py
   ```

## File Overview

- **`src/python/luna-ai.py`**: Main Python script for interacting with Luna.
- **`src/python/remember.json`**: Stores key details about you dynamically.
- **`src/python/chat-history.json`**: Logs your conversations with Luna.
- **`src/python/prompt.yaml`**: Defines Luna's personality, tone, and response style.
- **`src/python/the-spellbook.json`**: Contains archetypes, preferences, and emotional needs for deeper personalization.

## Recent Updates

- **Dynamic Memory Updates**: Luna now supports storing and updating key-value pairs dynamically using the `remember: "key" "value" priority:X` format. Higher priority numbers (e.g., `priority:5`) indicate greater importance.
- **Semantic Search**: Luna retrieves semantically similar memories and chats using embeddings, even if the exact words don’t match.
- **Pattern Detection**: Tracks emotional and archetypal patterns over time to provide deeper insights.
- **Self-Updating Priorities**: Memory priorities adjust dynamically based on frequency and relevance.
- **Improved Error Handling**: Enhanced error handling for `remember.json` and `chat-history.json` to ensure smooth operation.
- **Flexible Memory Context**: Luna dynamically formats memory for inclusion in prompts, ensuring responses are personalized and relevant.
- **Updated Prompt**: The `prompt.yaml` file has been refined to better reflect Luna's role, tone, and features.

## Requirements

- Python 3.9 or higher
- Required Python libraries (install via `pip install -r requirements.txt`)

## Future Plans

- **TypeScript/React UI**: Build an interactive web-based interface for Luna to make conversations more engaging and visually appealing.
- **Real-Time Cycle Tracking**: Add features to track and visualize menstrual cycles alongside lunar phases.
- **Deeper Archetype Analysis**: Enhance Luna’s ability to reflect on archetypes and suggest personalized rituals or practices.
- **Music Integration**: Allow Luna to suggest playlists directly from Spotify or other music platforms.
- **API Integration**: Create a REST API for seamless communication between the Python backend and the React frontend.

## Contributing

Feel free to contribute by submitting issues or pull requests. Let's make Luna even better together!

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **Error: `ModuleNotFoundError`**
   - Ensure you’ve activated the virtual environment:
     ```bash
     source .venv/bin/activate
     ```
   - Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Error: `JSONDecodeError`**
   - Check that `remember.json` and `chat-history.json` are valid JSON files. You can reset them with:
     ```bash
     echo "[]" > src/python/chat-history.json
     echo "[]" > src/python/remember.json
     ```

3. **AI Model Connection Issues**
   - Ensure the AI model server is running locally at `http://localhost:11434`.

## Privacy and Data Usage

Luna is designed to operate locally, ensuring your data remains private and secure. Here’s how Luna handles your data:

1. **Local Storage**: All personal data is stored in local files (`remember.json`, `chat-history.json`) on your machine.
2. **No External Sharing**: Luna does not send personal data to external servers. The AI model runs locally via `http://localhost`.
3. **Explicit Consent**: Luna requires explicit consent before accessing or discussing personal data.
4. **Data Reset**: You can reset Luna’s memory at any time by clearing `remember.json` and `chat-history.json`.

To reset memory:
```bash
echo "[]" > src/python/remember.json
echo "[]" > src/python/chat-history.json
```

Enjoy your journey with Luna!







