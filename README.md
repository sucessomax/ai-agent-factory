# AI Agent Factory

*Multi-Agents Demo com tecnologias modernas*

> Chatbot com arquitetura Multi-Agents demonstrando tecnologias modernas de IA.

## 🚀 Demonstração Online

### Versão que roda no navegador (sem API)

**Deploy instantâneo - basta fazer push para GitHub:**

```bash
# Clone e deploy para Vercel
git clone https://github.com/SEU-USUARIO/ai-agent-factory.git
cd ai-agent-factory/frontend
vercel --prod
```

**URL online:** `https://ai-agent-factory-frontend.vercel.app`

### Versão Completa (Backend + Frontend)

**Deploy com Render/Railway:**

```bash
# O Backend faz deploy automático no Render
# https://ai-agent-factory-backend.onrender.com
```

---

## 📚 Tecnologias Demonstradas

| Módulo | Tecnologia | Descrição |
|--------|------------|-----------|
| **Multi-Agents** | LangGraph | Supervisor → Researcher → Executor → Reviewer |
| **MCP** | Model Context Protocol | Ferramentas de sistema de arquivos |
| **RAG** | ChromaDB + Embeddings | Busca vetorial semântica |
| **LLMOps** | FastAPI + Streaming | API com respostas em tempo real |

**Disciplinas da Pós:**

- Fundamentos de IA e LLMs
- Prompt Engineering
- **MCP - Model Context Protocol** ✅
- **Criação de Agentes Autônomos** ✅
- Ferramentas de IA para DevOps
- **RAG e Vector Databases** ✅
- **MLOps** ✅
- **Arquitetura Multi-Agents** ✅

---

## 🎯 Como Executar

### 1. Versão Browser (Apenas Frontend)

```bash
cd frontend
npm install
npm run dev
# Acesse: http://localhost:5173
```

### 2. Versão Completa (Backend + Frontend)

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Adicione OPENAI_API_KEY no .env
python main.py

# Frontend (outro terminal)
cd frontend
npm install
npm run dev
```

### 3. Docker

```bash
docker-compose up --build
```

---

## 📁 Estrutura

```
ai-agent-factory/
├── backend/                  # FastAPI + LangChain
│   ├── main.py            # API endpoints
│   ├── agents/          # Agentes LangChain
│   ├── graph/           # LangGraph workflow
│   ├── rag/            # ChromaDB vectorstore
│   └── mcp/            # MCP tools
├── frontend/            # React + Tailwind
│   ├── src/
│   │   └── App.jsx     # Chat UI
│   ├── vite.config.js
│   └── tailwind.config.js
├── docker-compose.yml
└── README.md
```

---

## 🔌 Endpoints API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Info da API |
| GET | `/health` | Health check |
| POST | `/api/chat` | Chat simples |
| POST | `/api/chat/stream` | Chat com streaming |
| GET | `/api/rag/search?q=...` | Busca RAG |
| GET | `/api/mcp/tools` | Lista tools MCP |

---

## 🏗️ Arquitetura Multi-Agents

```
User Input
    │
    ▼
┌─────────────┐
│  Supervisor │ ← Decide próximo agente
└─────────────┘
    │
    ├──→ Researcher ← Busca na base RAG
    │       │
    │       ▼
    │   Reviewer ← Valida qualidade
    │
    └──→ Executor ← Executa tools (MCP)
            │
            ▼
        Reviewer ← Valida output
```

---

## 📝 Perguntas para Demo

Teste com essas perguntas para impressionar:

- "O que é Context Rot?"
- "Como funciona o padrão GSD?"
- "O que é MCP?"
- "Explain RAG"
- "Quais tecnologias da pósgraduação estão sendo usadas?"

---

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o
TEMPERATURE=0.7
```

---

## 📬 Contato

- **Autor:** Seu Nome
- **Course:** Pós-Graduação em Engenharia de IA Aplicada (UNIPDS)
- **GitHub:** github.com/seu-usuario

---

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

---

*Chatbot com Multi-Agents*

---

## 📬 Contato

- **Autor:** Seu Nome
- **GitHub:** github.com/seu-usuario

---

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.