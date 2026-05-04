import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, Bot, User, Cpu, Search, FileText, 
  Sparkles, Activity, Zap, MessageSquare, Loader2, Globe
} from 'lucide-react';

const AGENTS = [
  { id: 'supervisor', name: 'Supervisor', icon: Cpu, color: 'text-purple-400', bg: 'bg-purple-500/20' },
  { id: 'researcher', name: 'Researcher', icon: Search, color: 'text-blue-400', bg: 'bg-blue-500/20' },
  { id: 'executor', name: 'Executor', icon: Zap, color: 'text-emerald-400', bg: 'bg-emerald-500/20' },
  { id: 'reviewer', name: 'Reviewer', icon: FileText, color: 'text-amber-400', bg: 'bg-amber-500/20' },
];

const KNOWLEDGE_BASE = [
  "GSD (Get Shit Done) é uma metodologia de execução atômica onde o Orquestrador delega tarefas para Workers efêmeros com memória isolada.",
  "Context Rot é a degradação de contexto em longas sessões com LLMs, causando alucinações e perda de escopo.",
  "A Pós-Graduação em Engenharia de IA Aplicada cover: Fundamentos de IA, LLMs, Prompt Engineering, MCP, Agentes Autônomos, RAG, MLOps e Arquitetura Multi-Agents.",
  "LangGraph permite criar arquiteturas multiagentes com estados que fluem entre nós.",
  "MCP (Model Context Protocol) é um padrão para conectar LLMs a ferramentas externas como filesystem, GitHub, etc.",
  "RAG (Retrieval-Augmented Generation) combina busca vetorial com geração de texto.",
  "ChromaDB é um vector store open-source para RAG.",
  "DevFactory é um framework de orquestração multi-agente que previne Context Rot."
];

const generateResponse = (message) => {
  const lower = message.toLowerCase();
  let response = "";
  let agent = "researcher";
  
  if (lower.includes("context rot")) {
    response = "**Context Rot** é a degradação de contexto que ocorre em sessões longas com LLMs. O modelo começa a alucinar, perder regras de negócio e quebrar a coesão arquitetural.\n\nA solução: usar Workers efêmeros com memória isolada (como no DevFactory GSD).";
    agent = "researcher";
  } else if (lower.includes("gsd") || lower.includes("get shit done")) {
    response = "**GSD (Get Shit Done)** é a metodologia usada no DevFactory:\n\n1. **Orquestrador** (Tech Lead) - mantém contexto global\n2. **Workers Efêmeros** - executam tarefas com memória limpa\n3. **Checker/QA** - valida output vs spec\n\nIsso previne Context Rot ao máximo!";
    agent = "supervisor";
  } else if (lower.includes("mcp") || lower.includes("model context")) {
    response = "**MCP (Model Context Protocol)** é um protocolo padrão para conectar LLMs a ferramentas externas:\n\n- Filesystem (ler/gravar arquivos)\n- GitHub (operações de repo)\n- Search (busca web)\n- Database (consultas SQL)\n\nCriado pela Anthropic, agora é open-source.";
    agent = "researcher";
  } else if (lower.includes("rag")) {
    response = "**RAG (Retrieval-Augmented Generation)** combina:\n\n1. **Vector Store** (ChromaDB, Pinecone)\n2. **Embeddings** (OpenAI, Cohere)\n3. **Retrieval** (similarity search)\n4. **Generation** (LLM context)\n\nPermite que o LLM responda sobre sua base de conhecimento!";
    agent = "researcher";
  } else if (lower.includes("langgraph") || lower.includes("multi")) {
    response = "**Multi-Agents com LangGraph** permite criar sistemas onde múltiplos LLMs cooperam:\n\n- Supervisor → coordena\n- Researcher → busca infos\n- Executor → executa ações\n- Reviewer → valida\n\nO estado flui entre nós como um grafo!";
    agent = "supervisor";
  } else if (lower.includes("pós") || lower.includes("engenharia ia")) {
    response = "A **Pós-Graduação em Engenharia de IA Aplicada** (UNIPDS/Anhanguera) cover:\n\n1. Fundamentos de IA e LLMs\n2. APIs e Prompt Engineering\n3. **MCP** - Model Context Protocol\n4. **Criação de Agentes Autônomos**\n5. Ferramentas de IA para DevOps\n6. **RAG** e Vector Databases\n7. **MLOps / LLMOps**\n8. Arquitetura Multi-Agents\n9. Fine-tuning\n10. Segurança e Governança\n\nO projeto demonstra todos esses conceitos!";
    agent = "researcher";
  } else if (lower.includes("Olá") || lower.includes("oi") || lower.includes("hello")) {
    response = "🤖 **AI Agent Factory** está no ar!\n\nDemonstro as principais tecnologias da Pós-Graduação em Engenharia de IA Aplicada:\n\n- **Multi-Agents** -Supervisor → Pesquisa → Execução → Revisão\n- **MCP** - Ferramentas de sistema\n- **RAG** - Busca vetorial\n- **LangGraph** - Workflow de agentes\n\nPergunte sobre GSD, Context Rot, MCP, RAG, LangGraph ou a pósgraduação!";
    agent = "supervisor";
  } else {
    const relevant = KNOWLEDGE_BASE.filter(k => 
      k.toLowerCase().includes(lower.split(" ")[0]) || 
      lower.split(" ").some(w => k.toLowerCase().includes(w))
    );
    
    if (relevant.length > 0) {
      response = relevant[0];
    } else {
      response = `Interessante! Você perguntou sobre "${message}".\n\nBaseado na **Pós-Graduação em Engenharia de IA Aplicada**, posso explicar:\n\n- **GSD** - Metodologia de execução\n- **Context Rot** - Problema que resolvemos\n- **MCP** - Conexão com ferramentas\n- **RAG** - Busca vetorial\n- **LangGraph** - Multi-agentes\n\nQual tema te interessa mais?`;
    }
    agent = "researcher";
  }
  
  return { response, agent };
};

export default function App() {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: '🤖 **AI Agent Factory** está no ar!\n\nEste demo funciona **100% no navegador** - sem API externa necessária!\n\nDemonstro as principais tecnologias da Pós-Graduação em Engenharia de IA Aplicada:\n\n- **Multi-Agents** - Supervisão → Pesquisa → Execução → Revisão\n- **MCP** - Ferramentas de sistema de arquivos\n- **RAG** - Busca em base de conhecimento vetorial\n\nPergunte sobre GSD, Context Rot, MCP, RAG ou a pósgraduação!', 
      timestamp: Date.now() 
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeAgent, setActiveAgent] = useState(null);
  const [isOnline] = useState(window.location.hostname !== 'localhost');
  const messagesEnd = useRef(null);

  const scrollToBottom = () => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = () => {
    if (!input.trim() || loading) return;
    
    const userMsg = { role: 'user', content: input, timestamp: Date.now() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setActiveAgent('supervisor');

    setTimeout(() => {
      setActiveAgent('researcher');
    }, 300);

    setTimeout(() => {
      const { response, agent } = generateResponse(input);
      setActiveAgent(agent);
      
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: response,
          timestamp: Date.now(),
          agent: agent
        }]);
        setLoading(false);
        setActiveAgent(null);
      }, 800);
    }, 1500);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-500/20 rounded-xl">
              <Bot className="w-6 h-6 text-primary-400" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-primary-400 to-purple-400 bg-clip-text text-transparent">
                AI Agent Factory
              </h1>
              <p className="text-xs text-slate-500">Multi-Agents + MCP + RAG Demo</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            {isOnline && (
              <div className="flex items-center gap-1 px-2 py-1 bg-emerald-500/20 rounded-full">
                <Globe className="w-3 h-3 text-emerald-400" />
                <span className="text-xs text-emerald-400">Online</span>
              </div>
            )}
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-primary-400" />
              <span className="text-xs text-slate-400">GPT-4o (mock)</span>
            </div>
          </div>
        </div>
      </header>

      {/* Agent Status */}
      <div className="border-b border-slate-800/50 bg-slate-900/30">
        <div className="max-w-4xl mx-auto px-4 py-2 flex items-center gap-4 overflow-x-auto">
          {AGENTS.map(agent => (
            <div 
              key={agent.id}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                activeAgent === agent.id 
                  ? `${agent.bg} ${agent.color} agent-indicator` 
                  : 'text-slate-500'
              }`}
            >
              <agent.icon className="w-3.5 h-3.5" />
              {agent.name}
            </div>
          ))}
        </div>
      </div>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-6 space-y-4">
          {messages.map((msg, idx) => (
            <div 
              key={idx} 
              className={`flex gap-3 message-enter ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center ${
                msg.role === 'user' ? 'bg-slate-700' : 'bg-primary-500/20'
              }`}>
                {msg.role === 'user' 
                  ? <User className="w-4 h-4 text-slate-300" />
                  : <Bot className="w-4 h-4 text-primary-400" />
                }
              </div>
              
              <div className={`flex-1 max-w-[80%] ${msg.role === 'user' ? 'text-right' : ''}`}>
                <div className={`inline-block px-4 py-3 rounded-2xl ${
                  msg.role === 'user' 
                    ? 'bg-slate-800 text-slate-100' 
                    : 'bg-slate-800/50 text-slate-100 border border-slate-700/50'
                }`}>
                  <div className="text-sm whitespace-pre-wrap leading-relaxed">
                    {msg.content}
                  </div>
                </div>
                
                {msg.agent && (
                  <div className="flex items-center gap-2 mt-2 text-xs text-slate-500">
                    <Activity className="w-3 h-3" />
                    <span>Processado por: </span>
                    <span className="font-medium text-primary-400">{msg.agent}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-primary-500/20 flex items-center justify-center">
                <Bot className="w-4 h-4 text-primary-400" />
              </div>
              <div className="bg-slate-800/50 border border-slate-700/50 px-4 py-3 rounded-2xl">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 text-primary-400 animate-spin" />
                  <span className="text-sm text-slate-400">Processando...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEnd} />
        </div>
      </main>

      {/* Input */}
      <footer className="border-t border-slate-800 bg-slate-900/50">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-end gap-3 bg-slate-800/50 border border-slate-700/50 rounded-2xl p-2">
            <div className="flex-1">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Pergunte sobre GSD, Context Rot, MCP, RAG..."
                className="w-full bg-transparent text-slate-100 placeholder-slate-500 px-3 py-2 text-sm resize-none outline-none max-h-32"
                rows={1}
                disabled={loading}
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={!input.trim() || loading}
              className="flex-shrink-0 p-3 bg-primary-500 hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl transition-colors"
            >
              <Send className="w-4 h-4 text-white" />
            </button>
          </div>
          
          <div className="flex items-center justify-center gap-4 mt-3 text-xs text-slate-600">
            <div className="flex items-center gap-1">
              <MessageSquare className="w-3 h-3" />
              <span>Multi-Agents</span>
            </div>
            <div className="flex items-center gap-1">
              <Cpu className="w-3 h-3" />
              <span>MCP</span>
            </div>
            <div className="flex items-center gap-1">
              <Search className="w-3 h-3" />
              <span>RAG</span>
            </div>
            <span>•</span>
            <span>100% Browser</span>
          </div>
        </div>
      </footer>
    </div>
  );
}