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

### Setup & Run
```bash
# 1. Install Ollama model
ollama pull llama3.2

# 2. Set up Python backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt flask-cors

# 3. Set up frontend
npm install

# 4. Run application
# Terminal 1: API server
source venv/bin/activate && cd src/python && python api_server.py

# Terminal 2: Frontend
npm run dev

# Or terminal-only mode
npm start
```

### Access Points
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Terminal**: Run `npm start` for CLI interface

## 📁 Project Structure

```
luna-red/
├── README.md
├── package.json                    # Project scripts and dependencies
├── requirements.txt                # Python dependencies
├── src/
│   ├── python/                    # Backend
│   │   ├── kairos_ai.py          # Main AI application
│   │   ├── api_server.py         # Flask API server
│   │   ├── database/             # Database models and operations
│   │   └── tests/                # Backend tests
│   ├── components/               # React components
│   ├── pages/                    # React pages
│   ├── services/                 # API services
│   ├── hooks/                    # Custom React hooks
│   └── types/                    # TypeScript types
├── config/
│   └── prompt.yaml              # Kairos's personality & system prompt
├── data/
│   ├── kairos.db                # SQLite database (generated)
│   └── templates/               # Template files
└── venv/                        # Python virtual environment
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

### Testing
```bash
# Backend tests
npm test                    # All Python tests
npm run test:api           # API tests

# Frontend tests
npm run type-check         # TypeScript checking
npm run lint:frontend      # Code linting

# API testing
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Kairos!"}'
```

### Development
```bash
# Code quality
npm run format             # Format Python code
npm run lint               # Lint Python code

# Development scripts
npm run dev:full          # Start both backend and frontend
npm run build             # Build for production
npm run preview           # Preview production build
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
- React Frontend with TypeScript and Tailwind
- Database integration with full CRUD operations
- Memory system with semantic search

**🚀 Next Steps:**
- UI Components (Shadcn/ui)
- Real-time chat interface
- Memory management interface
- API integration with productivity tools

## 🤝 Contributing

Contributions are welcome for code improvements, better documentation, or suggestions for making Kairos more helpful.

## 🙏 Acknowledgments

Ngā mihi nui to ZanKris for planting the seed that became Luna, the original Kairos. And to Cursed.Helm, for always inspiring and being my kaiāwhiwhi (supporter) in this journey.

---

*Kairos honours the wisdom in your unique mind.* ✨