# AI Agent Factory

*Chatbot with Multi-Agents architecture*

> Chatbot demonstrating Multi-Agents, MCP, RAG and LangGraph technologies.

## 🚀 Quick Start

### Browser Version (Works instantly)

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173

### Full Version (Backend + Frontend)

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY to .env
python main.py

# Frontend (another terminal)
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up --build
```

---

## 📚 Technologies

| Technology | Description |
|------------|-------------|
| **LangGraph** | Multi-Agents workflow |
| **MCP** | Model Context Protocol |
| **RAG** | Vector search with ChromaDB |
| **FastAPI** | Python API |
| **React + Tailwind** | Modern UI |

---

## 🏗️ Architecture

```
User Input
    │
    ▼
┌─────────────┐
│  Supervisor │ ← Decision maker
└─────────────┘
    │
    ├──→ Researcher ← Search knowledge
    │       │
    │       ▼
    │   Reviewer ← Validate
    │
    └──→ Executor ← Execute tools
            │
            ▼
        Reviewer ← Validate output
```

---

## 📁 Structure

```
ai-agent-factory/
├── backend/
│   ├── main.py            # FastAPI endpoints
│   ├── agents/           # LangChain agents
│   ├── graph/           # LangGraph workflow
│   ├── rag/            # ChromaDB vectorstore
│   └── mcp/            # MCP tools
├── frontend/            # React + Tailwind
│   ├── src/
│   │   └── App.jsx     # Chat UI
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/chat` | Chat message |
| POST | `/api/chat/stream` | Streaming chat |
| GET | `/api/rag/search` | RAG search |
| GET | `/api/mcp/tools` | List MCP tools |

---

## 🔧 Configuration

```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o
TEMPERATURE=0.7
```

---

## 📄 License

MIT License