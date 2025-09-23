# Kairos: Your AI Companion for Neurodivergent Minds

Kairos is a warm, intelligent AI companion designed specifically for neurodivergent individuals. She combines neuroscience, emotional intelligence, and practical tools to support your unique way of thinking and being in the world.

## What Makes Kairos Special

**She understands neurodivergence** - Kairos is built with deep knowledge of ADHD, autism, and the beautiful complexity of neurodivergent minds. She gets that your brain works differently, and that's not a bug—it's a feature.

**She remembers and learns** - Kairos builds rich memories about your preferences, challenges, and what works for you. She uses semantic search to find relevant context from past conversations, making each interaction more personalised.

**She honours your cycles** - Whether it's your personal cycles, energy patterns, or creative rhythms, Kairos recognises that you're not a machine. She works with your natural ebbs and flows, not against them.

**She speaks your language** - Warm, collaborative, and culturally aware. Kairos incorporates te reo Māori naturally and meets you at eye-level.

## How It Works

Kairos runs as a VS Code extension with a Python backend that connects to a local AI model (Ollama). Everything stays on your machine—your data, your conversations, your privacy.

### Key Features
- **Memory System**: Remembers your preferences, challenges, and what strategies work for you
- **Pattern Recognition**: Notices recurring themes in your mood, energy, and thinking
- **Cycle Awareness**: Understands how hormonal cycles affect focus and energy
- **ADHD Support**: Body doubling, implementation intentions, and task initiation help
- **Autism Support**: Sensory considerations and communication style adaptations
- **Emotional Intelligence**: CBT techniques, emotional regulation tools, and gentle accountability

## Getting Started

1. **Install Ollama** and pull the Llama 3.2 model:
   ```bash
   ollama pull llama3.2
   ```

2. **Set up the Python environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run Kairos**:
   ```bash
   npm run start-python
   ```

4. **Give consent** when prompted - Kairos will ask for permission to access your personal data before diving into deep conversations.

## Privacy First

- **Everything stays local** - No data leaves your machine
- **You control your data** - Reset Kairos's memory anytime with `npm run reset-memory`
- **Explicit consent** - Kairos asks permission before accessing personal information
- **Transparent storage** - All data stored in readable JSON files

## The Technical Side

Built with:
- **Python** for the AI logic and memory systems
- **TypeScript** for the VS Code extension
- **Sentence Transformers** for semantic memory search
- **Ollama** for local AI model hosting
- **JSON** for simple, transparent data storage

## File Structure

### Core Files
- **`src/python/kairos-ai.py`** - Main Python implementation with memory and personality systems
- **`src/python/prompt.yaml`** - Defines Kairos's personality, expertise, and communication style
- **`src/python/the-spellbook.json`** - Stores user preferences, memories, and contextual information
- **`src/python/chat-history.json`** - Maintains conversation history for context and continuity

### Configuration Files
- **`package.json`** - VS Code extension configuration and dependencies
- **`tsconfig.json`** - TypeScript compiler settings
- **`eslint.config.mjs`** - Code quality and linting rules
- **`requirements.txt`** - Python dependencies

### Development Files
- **`src/ts/models.ts`** - TypeScript interfaces for chat messages and memory
- **`src/test/extension.test.ts`** - Unit tests for the VS Code extension
- **`README.md`** - This documentation file

## Contributing

Contributions are welcome,for code improvements, better documentation, or suggestions for making Kairos more helpful.

## Acknowledgments

Ngā mihi nui to ZanKris for planting the seed that became Luna, the original Kairos. And to Cursed.Helm, for always inspiring and being my kaiāwhiwhi (supporter) in this journey.

---

