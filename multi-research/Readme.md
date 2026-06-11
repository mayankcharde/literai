# 🧠 Multi-Agent Research Assistant

An intelligent research system powered by **9 specialized AI agents** that work together to research any topic and generate comprehensive reports with Q&A capability.

## ✨ Features

- 🔬 **9 AI Agents** working in coordination
- 📝 **Automated Research Reports** on any topic
- 🤖 **RAG Q&A** - Ask questions about your research
- 📊 **Quality Scoring** with confidence metrics
- 💾 **Research History** stored in MongoDB
- 🔐 **User Authentication** (JWT)
- 📱 **Modern React Frontend**

## 🏗 Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core language |
| FastAPI | API framework |
| LangGraph | Agent orchestration |
| Mistral AI | LLM provider |
| Tavily | Web search |

### Frontend (MERN)
| Technology | Purpose |
|------------|---------|
| React.js | UI framework |
| Redux | State management |
| TailwindCSS | Styling |
| Axios | API calls |

### Database
| Technology | Purpose |
|------------|---------|
| MongoDB | User data, history |
| ChromaDB | Vector storage for RAG |

## 🤖 The 9 Agents

| # | Agent | Role |
|---|-------|------|
| 1 | **Orchestrator** | Plans strategy & coordinates all agents |
| 2 | **Planner** | Creates research questions |
| 3 | **Searcher** | Searches web for information |
| 4 | **Analyzer** | Extracts key insights from data |
| 5 | **Writer** | Writes the research report |
| 6 | **Fact Checker** | Verifies facts & citations |
| 7 | **Reviewer** | Reviews quality & gives feedback |
| 8 | **Summarizer** | Creates multiple summaries |
| 9 | **Formatter** | Formats final output |

## 🚀 Quick Start

### Backend Setup

```bash
# Clone repo
git clone https://github.com/yourusername/multi-agent-research.git
cd multi-agent-research

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLP data
python -m textblob.download_corpora

# Set environment variables
# Create .env file with your API keys

# Run backend
cd backend
python -m uvicorn main:app --reload --port 8000
Frontend Setup
bash
cd frontend
npm install
npm start
MongoDB Setup
bash
# Using Docker
docker run -d --name mongodb -p 27017:27017 mongo

# Or use MongoDB Atlas (free cloud)
🔑 Environment Variables
Create .env file:

env
MISTRAL_API_KEY=your_mistral_key
TAVILY_API_KEY=your_tavily_key
MONGODB_URI=mongodb://localhost:27017/research_db
JWT_SECRET=your_secret_key






🎯 How It Works
Enter a topic (e.g., "Future of AI in healthcare")

9 agents work in sequence - Planning → Searching → Writing → Reviewing

Get comprehensive report with quality score

Ask questions about the report using RAG

Download report in multiple formats

📊 Agent Workflow
text
Start → Orchestrator → Planner → Searcher → Analyzer → Writer 
→ Fact Checker → Reviewer → Summarizer → Formatter → Complete


Credits
LangGraph - Agent framework

Mistral AI - Language model

Tavily - Search API

Made with ❤️ using LangGraph + Mistral AI + MERN

text

This simpler version includes:
- ✅ Clean, readable format
- ✅ All 9 agents with brief descriptions
- ✅ MERN stack mention
- ✅ User authentication
- ✅ MongoDB storage
- ✅ Simple setup instructions
- ✅ Clear workflow explanation

