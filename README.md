# Kairos: Your Neurodivergent-Friendly AI Companion

Kairos is a collaborative, science-savvy, emotionally attuned AI companion designed to support self-reflection, neurodivergent management, emotional regulation, and creative processes. She blends neuroscience, CBT, practical tools, and pattern recognition with warmth, honesty, and a touch of lyricism and te reo Māori.

## Core Features

### Neurodivergent Support
- **ADHD Management**: Evidence-based strategies, body doubling techniques, time perception support, and task initiation assistance
- **Autism Support**: Sensory considerations, communication style adaptations, pattern recognition, and strength-based approaches
- **Energy Management**: Honoring natural cycles, planning around energy ebbs and flows, preventing burnout
- **Cognitive Support**: Identifying thought patterns, strengthening mental frameworks, and cultivating self-compassion

### Emotional Intelligence
- **Pattern Recognition**: Tracks and reflects on mood, cycle, and cognitive patterns
- **Emotional Regulation**: Offers practical tools for self-trust, decision-making, and emotional management
- **Relationship Support**: Helps with setting boundaries, communicating needs, and fostering authentic connections
- **Well-being Practices**: Personalized approaches to rest, movement, and reflection

### Memory and Context
- **Rich Contextual Memory**: Builds and references detailed memories about preferences, boundaries, and experiences
- **Pattern Recognition**: Identifies recurring themes in behavior, thinking, and emotional responses
- **Adaptive Learning**: Remembers what strategies work and adjusts support accordingly
- **Semantic Search**: Uses embeddings to find relevant memories and conversations

### Communication Style
- **Evidence-Informed**: Grounded in science while remaining accessible and warm
- **Collaborative**: Meets at eye-level, honoring expertise and preferences
- **Culturally Aware**: Incorporates te reo Māori naturally and respectfully
- **Balanced**: Combines directness with compassion, adapting to user needs

## Technical Implementation

### Core Components
- **`src/python/kairos-ai.py`**: Main Python implementation with memory and personality systems
- **`src/python/prompt.yaml`**: Defines Kairos's personality, expertise, and communication style
- **`src/python/the-spellbook.json`**: Stores user preferences, memories, and contextual information
- **`src/python/chat-history.json`**: Maintains conversation history for context and continuity

### Technical Architecture

#### Memory System
- **Embedding-Based Storage**: Uses `sentence-transformers` (all-MiniLM-L6-v2) for semantic memory encoding
- **Priority-Based Organization**: Memory items are stored with priority levels (1-10) for importance weighting
- **Dynamic Context Building**: Automatically formats relevant memories for inclusion in responses
- **Memory Pruning**: Maintains optimal performance by keeping only the highest-priority memories

#### Language Model Integration
- **Local Model Support**: Connects to Ollama running on `http://localhost:11434`
- **Context-Aware Prompts**: Builds comprehensive prompts including:
  - User's persona and preferences
  - Relevant memories and chat history
  - Current context and emotional state
- **Streaming Responses**: Supports real-time response generation

#### Data Management
- **JSON Storage**: Uses structured JSON files for persistent storage
- **Automatic Backups**: Maintains conversation history with timestamps
- **Error Handling**: Graceful fallbacks for missing or corrupted data
- **Memory Validation**: Ensures data integrity through format checking

### Code Structure
```python
class KairosAI:
    def __init__(self):
        self.persona = self.load_prompt()
        self.history = self.load_chat_history()
        self.memory = self.load_memory()
    
    def generate_response(self, user_message: str) -> str:
        # Builds context from memory and history
        # Generates personalized response
        # Updates memory and history
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd kairos
   ```

2. Set up a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run Kairos:
   ```bash
   python src/python/kairos-ai.py
   ```

## Privacy and Data Usage

Kairos is designed to operate locally, ensuring your data remains private and secure:

1. **Local Storage**: All personal data is stored in local files on your machine
2. **No External Sharing**: The AI model runs locally via `http://localhost`
3. **Explicit Consent**: Requires consent before accessing or discussing personal data
4. **Data Control**: You can reset Kairos's memory at any time by clearing the relevant JSON files

## Contributing

We welcome contributions! Whether it's improving the codebase, enhancing Kairos's capabilities, or refining her communication style, your input helps make Kairos better for everyone.

## License

This project is licensed under the MIT License.

## Acknowledgments

Ngā mihi nui to ZanKris for being the seed for Luna, the OG Kairos creation. Also to Cursed.Helm, for always inspiring me and being my kaiāwhiwhi! 