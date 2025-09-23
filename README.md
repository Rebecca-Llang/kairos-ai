# 🌙 Kairos: Your AI Companion for Neurodivergent Minds

Kairos is a warm, intelligent AI companion designed specifically for neurodivergent individuals. She combines neuroscience, emotional intelligence, and practical tools to support your unique way of thinking and being in the world.

## ✨ What Makes Kairos Special

**🧠 She understands neurodivergence** - Kairos is built with deep knowledge of ADHD, autism, and the beautiful complexity of neurodivergent minds. She gets that your brain works differently, and that's not a bug—it's a feature.

**💭 She remembers and learns** - Kairos builds rich memories about your preferences, challenges, and what works for you. She uses semantic search to find relevant context from past conversations, making each interaction more personalised.

**🌊 She honours your cycles** - Whether it's your personal cycles, energy patterns, or creative rhythms, Kairos recognises that you're not a machine. She works with your natural ebbs and flows, not against them.

**🗣️ She speaks your language** - Warm, collaborative, and culturally aware. Kairos incorporates te reo Māori naturally and meets you at eye-level.

## 🚀 How It Works

Kairos runs as a Python backend that connects to a local AI model (Ollama). Everything stays on your machine—your data, your conversations, your privacy.

### Key Features
- **🧠 Memory System**: Remembers your preferences, challenges, and what strategies work for you
- **🔍 Pattern Recognition**: Notices recurring themes in your mood, energy, and thinking
- **🌙 Cycle Awareness**: Understands how hormonal cycles affect focus and energy
- **🎯 ADHD & Neurodivergent Support**: Body doubling, implementation intentions, and task initiation help with communication style adaptations
- **❤️ Emotional Intelligence**: CBT techniques, emotional regulation tools, and gentle accountability

## 🛠️ Getting Started

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
   npm start
   ```

4. **Give consent** when prompted - Kairos will ask for permission to access your personal data before diving into deep conversations.

## 🔒 Privacy First

- **🏠 Everything stays local** - No data leaves your machine
- **🎛️ You control your data** - Reset Kairos's memory anytime with `npm run reset`
- **✅ Explicit consent** - Kairos asks permission before accessing personal information
- **📄 Transparent storage** - All data stored in readable JSON files

## 🏗️ The Technical Side

Built with:
- **🐍 Python** for the AI logic and memory systems
- **🧠 Sentence Transformers** for semantic memory search
- **🦙 Ollama** for local AI model hosting
- **📄 JSON** for simple, transparent data storage

## 📁 File Structure

### Core Files
- **`src/python/kairos_ai.py`** - Main Python implementation with memory and personality systems
- **`src/python/prompt.yaml`** - Defines Kairos's personality, expertise, and communication style
- **`src/python/the-spellbook.json`** - Template for user preferences, memories, and contextual information
- **`src/python/the-spellbook-bee.json`** - Rebecca's personal memory data (not tracked in git)
- **`src/python/chat-history.json`** - Conversation history for context and continuity (not tracked in git)

### Configuration Files
- **`package.json`** - Project configuration and dependencies
- **`requirements.txt`** - Python dependencies

## ⚡ Commands

```bash
npm start          # Start Kairos AI
npm run debug      # Start with debug output
npm run reset      # Clear all memories and chat history

npm test           # Run complete test suite
npm run test:core  # Run core functionality tests
npm run test:data  # Run data validation tests
npm run test:config # Run configuration tests
npm run test:quick # Quick syntax validation

npm run setup      # Initialize frontend project
npm run dev        # Run backend + frontend concurrently
```

## 🔮 Future Plans

- **🌐 React Frontend** - Beautiful, accessible web interface
- **🗄️ Database Integration** - SQLite for better data management and SQL learning
- **🔗 API Integration** - Connect with productivity tools and cycle trackers

## 🤝 Contributing

Contributions are welcome for code improvements, better documentation, or suggestions for making Kairos more helpful.

## 🙏 Acknowledgments

Ngā mihi nui to ZanKris for planting the seed that became Luna, the original Kairos. And to Cursed.Helm, for always inspiring and being my kaiāwhiwhi (supporter) in this journey.

---

*Kairos honours the wisdom in your unique mind.* ✨