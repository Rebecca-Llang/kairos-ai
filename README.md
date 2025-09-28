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
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Migrate existing data** (if you have old JSON files):
   ```bash
   cd src/python
   python migrations/migrate_json_to_sqlite.py
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

## Privacy First

- **Everything stays local** - No data leaves your machine
- **You control your data** - Reset Kairos's memory anytime with `npm run reset-memory`
- **Explicit consent** - Kairos asks permission before accessing personal information
- **Git protection** - Personal data files are automatically ignored by git
- **Transparent storage** - All data stored in readable JSON files

### Git Ignore Protection

The following files containing personal data are automatically ignored by git:
- `data/kairos.db*` - Database files
- `data/backups/*` - Backup files
- `data/templates/chat-history.json` - Your chat history
- `data/templates/the-spellbook-bee.json` - Your personal spellbook

Only template files (`the-spellbook.json`) are tracked by git.

## The Technical Side

Built with:
- **Python** for the AI logic and memory systems
- **Sentence Transformers** for semantic memory search and chat history analysis
- **Ollama** for local AI model hosting (Llama 3.2)
- **SQLite** for persistent data storage with embeddings
- **PyYAML** for configuration management

## File Structure

### Core Files
- **`src/python/kairos_ai.py`** - Main Python implementation with memory and personality systems
- **`config/prompt.yaml`** - Defines Kairos's personality, expertise, and communication style
- **`data/kairos.db`** - SQLite database storing chat history, memories, and embeddings
- **`src/python/database/`** - Database models, operations, and schema

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

