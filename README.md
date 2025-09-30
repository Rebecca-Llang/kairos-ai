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
- **🧠 Memory System**: Remembers preferences, challenges, and strategies that work for you
- **🔍 Pattern Recognition**: Notices recurring themes in mood, energy, and thinking
- **🌙 Cycle Awareness**: Understands how cycles affect focus and energy
- **🎯 Neurodivergent Support**: Body doubling, implementation intentions, and task initiation help
- **❤️ Emotional Intelligence**: CBT techniques, emotional regulation tools, and gentle accountability
- **✨ Modern Web Interface**: Beautiful React frontend with TypeScript and Tailwind CSS
- **🚨 Hallucination Detection**: Automatically detects and removes fake user input
- **⏱️ Smart Timeouts**: Prevents hanging responses with intelligent timeout management

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
- **Frontend**: http://localhost:3000
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
```bash
# Development
npm run dev               # Frontend only
npm run start             # Backend only
npm run dev:full          # Both backend and frontend

# Testing
npm test                  # All Python tests
npm run test:models       # Model tests
npm run test:core         # Core operation tests
npm run lint:frontend     # Frontend linting
npm run type-check        # TypeScript checking

# Code Quality
npm run format            # Format Python code
npm run format:frontend   # Format frontend code
npm run lint:fix          # Auto-fix linting issues

# Database
npm run migrate           # Run database migrations
npm run cli               # Run CLI interface
npm run debug             # Run in debug mode
```

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

**✅ Complete:**
- Python Backend with SQLite database and Kairos AI
- Flask API server with CORS support
- React Frontend with TypeScript and Tailwind CSS
- Database integration with full CRUD operations
- Memory system with semantic search
- Professional code quality tools (ESLint, Prettier)
- Component organization with index files
- Centralized constants and configuration
- TypeScript strict mode configuration
- Vite build system with path aliases

**🚀 Next Steps:**
- Complete UI Components (Shadcn/ui integration)
- Real-time chat interface implementation
- Memory management interface
- API integration with productivity tools
- Component testing with React Testing Library

## 🤝 Contributing

Contributions are welcome for code improvements, better documentation, or suggestions for making Kairos more helpful.

## 🙏 Acknowledgments

Ngā mihi nui to ZanKris for planting the seed that became Luna, the original Kairos. And to Cursed.Helm, for always inspiring and being my kaiāwhiwhi (supporter) in this journey.

---

*Kairos honours the wisdom in your unique mind.* ✨