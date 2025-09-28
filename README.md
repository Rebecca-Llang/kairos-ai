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
- **✨ Beautiful Terminal Interface**: Rich, colorful output with proper input handling
- **🚨 Hallucination Detection**: Automatically detects and removes fake user input from AI responses
- **⏱️ Smart Timeouts**: Prevents hanging responses with intelligent timeout management

## 🛠️ Getting Started

1. **Install Ollama** and pull the Llama 3.2 model:
   ```bash
   ollama pull llama3.2
   ```

2. **Set up the Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Migrate existing data** (if you have old JSON files):
   ```bash
   npm run migrate
   ```

4. **Run Kairos**:
   ```bash
   npm start
   # or directly:
   python src/python/kairos_ai.py
   ```

5. **Give consent** when prompted - Kairos will ask for permission to access your personal data before diving into deep conversations.

## Project Structure

```
luna-red/
├── README.md
├── package.json                    # Project scripts and metadata
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Modern Python project config
├── .gitignore
├── src/
│   └── python/
│       ├── kairos_ai.py           # Main AI application
│       ├── database/
│       │   ├── connection.py      # Database connection management
│       │   ├── models.py          # Data models (ChatMessage, SpellbookMemory)
│       │   ├── operations.py      # CRUD operations
│       │   └── schema.sql         # Database schema
│       ├── migrations/
│       │   └── migrate_json_to_sqlite.py  # Data migration script
│       └── tests/
│           ├── test_models.py      # Model unit tests
│           ├── test_operations.py  # Database operation tests
│           ├── test_database_integration.py  # Integration tests
│           └── test_migration.py   # Migration tests
├── config/
│   └── prompt.yaml               # Kairos's personality & system prompt
├── data/
│   ├── kairos.db                 # SQLite database (generated, ignored by git)
│   ├── backups/                  # Backup files (ignored by git)
│   └── templates/                # Template files
│       ├── chat-history.json     # Personal chat history (ignored by git)
│       ├── the-spellbook-bee.json # Personal spellbook (ignored by git)
│       └── the-spellbook.json    # Empty template (tracked by git)
└── venv/                          # Python virtual environment
```

## Database Integration

Kairos now uses SQLite for persistent storage, providing better performance and data integrity than JSON files.

### Database Features
- **Chat History**: All conversations stored with timestamps
- **Memory System**: Persistent spellbook with priorities and embeddings
- **Data Integrity**: Constraints and validation ensure clean data
- **Backup Support**: Automatic backups during migration

### Database Commands
While chatting with Kairos, you can use these commands:
- `db:stats` - Show database statistics
- `db:clear_chat` - Clear all chat history
- `db:delete_memory <key>` - Delete specific memory
- `db:help` - Show all database commands

### Memory Management
Add memories using the format:
```
remember: "your_key_name" "memory and details here" priority:7
```

Examples:
- `remember: "favorite_coffee" "oat milk flat white with extra shot" priority:8`
- `remember: "energy_pattern" "morning person, crashes at 2pm, needs protein snacks" priority:9`
- `remember: "focus_strategies" "25-minute pomodoro sessions work best, with 5-minute breaks and no notifications" priority:8`

**Note**: You can include punctuation, special characters, and detailed descriptions in your memories. The system uses semantic search to find relevant memories even with different wording.

## Development

### Running Tests
```bash
# Run all tests
npm test

# Run specific test suites
npm run test:models
npm run test:operations
npm run test:integration
npm run test:migration
```

### Code Quality
```bash
# Format code
npm run format

# Lint code
npm run lint
```

### Database Management
```bash
# Run migration
npm run migrate

# Debug mode
npm run debug
```

## 🔒 Privacy First

<<<<<<< HEAD
- **Everything stays local** - No data leaves your machine
- **You control your data** - Reset Kairos's memory anytime with `npm run reset-memory`
- **Explicit consent** - Kairos asks permission before accessing personal information
- **Git protection** - Personal data files are automatically ignored by git
- **Transparent storage** - All data stored in readable JSON files
||||||| 7e15a12
- **Everything stays local** - No data leaves your machine
- **You control your data** - Reset Kairos's memory anytime with `npm run reset-memory`
- **Explicit consent** - Kairos asks permission before accessing personal information
- **Transparent storage** - All data stored in readable JSON files
=======
- **🏠 Everything stays local** - No data leaves your machine
- **🎛️ You control your data** - Reset Kairos's memory anytime with `npm run reset`
- **✅ Explicit consent** - Kairos asks permission before accessing personal information
- **📄 Transparent storage** - All data stored in readable JSON files
>>>>>>> main

<<<<<<< HEAD
### Git Ignore Protection

The following files containing personal data are automatically ignored by git:
- `data/kairos.db*` - Database files
- `data/backups/*` - Backup files
- `data/templates/chat-history.json` - Your chat history
- `data/templates/the-spellbook-bee.json` - Your personal spellbook

Only template files (`the-spellbook.json`) are tracked by git.

## The Technical Side
||||||| 7e15a12
## The Technical Side
=======
## 🏗️ The Technical Side
>>>>>>> main

Built with:
<<<<<<< HEAD
- **Python** for the AI logic and memory systems
- **Sentence Transformers** for semantic memory search and chat history analysis
- **Ollama** for local AI model hosting (Llama 3.2)
- **SQLite** for persistent data storage with embeddings
- **PyYAML** for configuration management
||||||| 7e15a12
- **Python** for the AI logic and memory systems
- **TypeScript** for the VS Code extension
- **Sentence Transformers** for semantic memory search
- **Ollama** for local AI model hosting
- **JSON** for simple, transparent data storage
=======
- **🐍 Python** for the AI logic and memory systems
- **🧠 Sentence Transformers** for semantic memory search
- **🦙 Ollama** for local AI model hosting
- **📄 JSON** for simple, transparent data storage
- **✨ Rich** for beautiful terminal output and proper input handling
- **🎨 Termcolor** for colored console output
>>>>>>> main

## 📁 File Structure

### Core Files
<<<<<<< HEAD
- **`src/python/kairos_ai.py`** - Main Python implementation with memory and personality systems
- **`config/prompt.yaml`** - Defines Kairos's personality, expertise, and communication style
- **`data/kairos.db`** - SQLite database storing chat history, memories, and embeddings
- **`src/python/database/`** - Database models, operations, and schema
||||||| 7e15a12
- **`src/python/kairos-ai.py`** - Main Python implementation with memory and personality systems
- **`src/python/prompt.yaml`** - Defines Kairos's personality, expertise, and communication style
- **`src/python/the-spellbook.json`** - Stores user preferences, memories, and contextual information
- **`src/python/chat-history.json`** - Maintains conversation history for context and continuity
=======
- **`src/python/kairos_ai.py`** - Main Python implementation with memory and personality systems
- **`src/python/prompt.yaml`** - Defines Kairos's personality, expertise, and communication style
- **`src/python/the-spellbook.json`** - Template for user preferences, memories, and contextual information
- **`src/python/the-spellbook-bee.json`** - Rebecca's personal memory data (not tracked in git)
- **`src/python/chat-history.json`** - Conversation history for context and continuity (not tracked in git)

### Test Files
- **`tests/run_tests.py`** - Main test runner
- **`tests/test_core.py`** - Core functionality tests
- **`tests/test_data.py`** - Data validation tests
- **`tests/test_config.py`** - Configuration tests
- **`tests/test_kairos_system.py`** - System integration tests
- **`tests/test_api_quick.py`** - API quick tests
>>>>>>> main

### Configuration Files
- **`package.json`** - Project configuration and npm scripts
- **`requirements.txt`** - Python dependencies
- **`tsconfig.json`** - TypeScript configuration (for future frontend)
- **`eslint.config.mjs`** - ESLint configuration

## ⚡ Commands

```bash
npm start          # Start Kairos AI
npm run debug      # Start with debug output
npm run reset      # Clear all memories and chat history

npm test           # Run complete test suite
npm run test:core  # Run core functionality tests
npm run test:data  # Run data validation tests
npm run test:config # Run configuration tests
npm run test:system # Run system integration tests
npm run test:api   # Run API quick tests
npm run test:quick # Quick syntax validation

npm run setup      # Initialize frontend project
npm run dev        # Run backend + frontend concurrently
```

## 🐛 Debugging & Troubleshooting

### Debug Mode
Enable detailed debugging output:
```bash
KAIROS_DEBUG=true npm start
```

### Common Issues
- **Response timeouts**: Kairos has intelligent timeout management (2 minutes for streaming)
- **Hallucinations**: Automatically detected and removed - you'll see `🚨 DETECTED HALLUCINATIONS:` if any occur
- **Terminal issues**: Rich framework handles input/output properly across platforms
- **Memory issues**: Use `npm run reset` to clear all memories and start fresh

### Response Quality Monitoring
Kairos automatically detects and reports:
- **Hallucinated user input** (fake "You:" messages)
- **Repetitive content** (words repeated >30% of the time)
- **Incomplete responses** (ending with commas/dashes)
- **Very short responses** (may indicate incomplete generation)

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