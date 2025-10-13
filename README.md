# 🌙 Kairos: Your AI Companion for Neurodivergent Minds

Kairos is a warm, intelligent AI companion designed specifically for neurodivergent individuals. She combines neuroscience, emotional intelligence, and practical tools to support your unique way of thinking and being in the world.

## ✨ What Makes Kairos Special

**🧠 She understands neurodivergence** - Built with deep knowledge of ADHD, autism, and the beautiful complexity of neurodivergent minds.

**💭 She remembers and learns** - Builds rich memories about your preferences, challenges, and what works for you using semantic search.

**🌊 She honours your cycles** - Recognises your natural ebbs and flows, working with your energy patterns and creative rhythms.

**🗣️ She speaks your language** - Warm, collaborative, and culturally aware with te reo Māori integration.

## 🚀 How It Works

Kairos runs as a Python backend with a React frontend, connecting to a local AI model (Ollama). Everything stays on your machine—your data, your conversations, your privacy.

### Key Features
- **🧠 Memory System**: Complete CRUD operations for storing and managing personal memories
- **💬 Chat Interface**: Real-time conversation with Kairos AI (fully functional)
- **📚 Spellbook**: Add, edit, and delete memories with responsive interface
- **✨ Modern Web Interface**: Beautiful React frontend with TypeScript and Tailwind CSS
- **🔒 Privacy First**: Everything runs locally - no data leaves your machine
- **🧪 Testing Infrastructure**: Comprehensive test suite with coverage reporting
- **⚡ Fast Development**: Hot reload, TypeScript, ESLint, Prettier all configured

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+, Node.js 18+, Ollama

### Setup
```bash
# Install Ollama model
ollama pull llama3.2

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt flask-cors
npm install

# Run application
npm run dev:full          # Starts both backend and frontend
```

### Access Points
- **Frontend**: http://localhost:3000 (Chat & Spellbook fully functional)
- **API**: http://localhost:8000
- **CLI**: `npm run cli`

## 📁 Project Structure

```
luna-red/
├── src/
│   ├── components/          # React components (chat, layout, ui)
│   ├── pages/              # React pages
│   ├── services/           # API services
│   ├── hooks/              # Custom React hooks
│   ├── types/              # TypeScript types
│   ├── constants/          # App constants
│   ├── utils/              # Utility functions
│   └── python/             # Backend (AI, API, database)
├── config/                 # Kairos personality config
├── data/                   # Database and templates
└── venv/                   # Python environment
```

## 🗄️ Database & Memory System

Kairos uses SQLite for persistent storage with semantic search capabilities.

### Memory Management
Add memories on the terminal using the format:
```
remember: "your_key_name" "memory and details here" priority:7
```

Examples:
- `remember: "favorite_coffee" "oat milk flat white with extra shot" priority:8`
- `remember: "energy_pattern" "morning person, crashes at 2pm, needs protein snacks" priority:9`
- `remember: "focus_strategies" "25-minute pomodoro sessions work best, with 5-minute breaks and no notifications" priority:8`

## 🧪 Testing & Development

### Quick Start
```bash
# Install dependencies
npm install
pip install -r requirements.txt flask-cors

# Run the application
npm run dev:full          # Start both backend and frontend
```

### Available Commands

#### Development
```bash
npm run dev               # Frontend dev server (Vite)
npm run start             # Backend API server (Flask)
npm run dev:full          # Both backend and frontend (recommended)
npm run cli               # CLI interface with Kairos
npm run debug             # Backend in debug mode
```

#### Testing
```bash
# Run all tests (backend + frontend)
npm test

# Frontend tests
npm run test:frontend           # Watch mode (auto-rerun on changes)
npm run test:frontend:run       # Run once
npm run test:frontend:coverage  # Run with coverage report

# Backend tests
npm run test:backend            # All Python tests (11 tests)

# Coverage
npm run test:coverage           # Generate coverage report
```

#### Code Quality
```bash
# Linting
npm run lint              # Python linting (flake8)
npm run lint:frontend     # TypeScript/React linting (ESLint)
npm run lint:fix          # Auto-fix linting issues

# Formatting
npm run format            # Format Python code (Black)
npm run format:frontend   # Format frontend code (Prettier)
npm run format:check      # Check formatting without changes

# Type Checking
npm run type-check        # TypeScript type checking
```

#### Database & Migrations
```bash
npm run migrate           # Run database migrations
```

#### Build & Deploy
```bash
npm run build             # Build frontend for production
npm run preview           # Preview production build
```

### Testing Strategy

Kairos uses a comprehensive testing approach with **Unit Tests** (80%) and **Integration Tests** (15%), with **E2E Tests** (5%) planned for the future.

#### **Unit Tests**
- **Tool**: Vitest with React Testing Library
- **Coverage**: Components, hooks, utilities
- **Speed**: Fast (3-5 seconds)
- **Location**: `src/**/__tests__/*.test.tsx`

**Current**: 29 tests total (11 backend + 18 frontend) across core functionality.

#### **Coverage Reports**
```bash
npm run test:coverage
```

Generates terminal summary and HTML report (`coverage/index.html`). Target: 60%+ coverage.

## 🔒 Privacy First

- **Everything stays local** - No data leaves your machine
- **You control your data** - Reset Kairos's memory anytime
- **Explicit consent** - Kairos asks permission before accessing personal information
- **Git protection** - Personal data files are automatically ignored by git

## 🏗️ The Technical Side

Built with:
- **Python** for the AI logic and memory systems
- **React + TypeScript** for the modern web interface
- **SQLite** for persistent data storage with embeddings
- **Ollama** for local AI model hosting
- **Sentence Transformers** for semantic memory search
- **Flask** for the API server
- **Tailwind CSS** for styling

## 🔮 Status & Roadmap

**✅ Complete & Functional:**
- **Backend**: Python Flask API with SQLite database and Kairos AI
- **Chat Interface**: Fully functional real-time conversation system
- **Spellbook**: Complete memory management (add/edit/delete) with responsive UI
- **Testing**: Comprehensive test suite (29 tests total) with coverage reporting
- **Code Quality**: ESLint, Prettier, TypeScript, Vitest all configured
- **Development**: Hot reload, path aliases, modern build system

**🚧 In Progress:**
- **About Page**: Basic placeholder (needs content)
- **Persona Page**: AI personality settings (placeholder)
- **History Page**: Conversation history viewer (placeholder)

**🚀 Future Enhancements:**
- Complete About page with project information
- AI personality customization interface
- Conversation history browsing
- Advanced memory search and filtering
- E2E testing with Playwright
- Performance optimizations

## 🤝 Contributing

Contributions are welcome for code improvements, better documentation, or suggestions for making Kairos more helpful.

## 🙏 Acknowledgments

Ngā mihi nui to ZanKris for planting the seed that became Luna, the original Kairos. And to Cursed.Helm, for always inspiring and being my kaiāwhiwhi (supporter) in this journey.

---

*Kairos honours the wisdom in your unique mind.* ✨