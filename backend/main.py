from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import asyncio
import os

from graph.workflow import run_agent_workflow
from rag.vectorstore import similarity_search, create_vectorstore
from mcp.client import get_mcp_tools
from config import VERCEL, VERCEL_URL

app = FastAPI(
    title="AI Agent Factory API",
    version="1.0.0",
    description="Multi-Agents + MCP + RAG Demo for Engineering IA Applied"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    agent: str
    intent: str
    review: Optional[str] = ""

sessions = {}


@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    try:
        create_vectorstore()
        print("AI Agent Factory initialized!")
    except Exception as e:
        print(f"Startup warning: {e}")


@app.get("/")
async def root():
    return {
        "name": "AI Agent Factory",
        "version": "1.0.0",
        "description": "Multi-Agents demo for Pós-Graduação Engenharia de IA Aplicada",
        "agents": ["supervisor", "researcher", "executor", "reviewer"],
        "features": ["Multi-Agents (LangGraph)", "MCP Tools", "RAG (ChromaDB)", "Streaming"],
        "endpoints": {
            "GET /": "API info",
            "GET /health": "Health check",
            "POST /chat": "Chat message",
            "POST /chat/stream": "Streaming chat",
            "GET /rag/search": "RAG search",
            "GET /mcp/tools": "List MCP tools"
        },
        "deploy": {
            "vercel": VERCEL == "1",
            "url": VERCEL_URL if VERCEL else None
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai-agent-factory"}


@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Process chat message."""
    try:
        result = await run_agent_workflow(message.message)
        
        return ChatResponse(
            response=result["response"],
            agent=result["agent"],
            intent=result["intent"],
            review=result.get("review", "")
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/chat/stream")
async def chat_stream(message: ChatMessage):
    """Process chat with streaming response."""
    
    async def generate():
        try:
            # RAG search em background
            context = await asyncio.to_thread(similarity_search, message.message, k=3)
            
            # Process through agents
            result = await run_agent_workflow(message.message)
            
            # Stream response
            response_text = result["response"]
            words = response_text.split()
            
            for i, word in enumerate(words):
                chunk = {
                    "type": "chunk",
                    "content": word + (" " if i < len(words) - 1 else ""),
                    "agent": result["agent"],
                    "intent": result["intent"]
                }
                yield f"data: {json.dumps(chunk)}\n\n"
                await asyncio.sleep(0.03)
            
            yield "data: {\"type\": \"done\"}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


@app.get("/api/rag/search")
async def rag_search(q: str, k: int = 3):
    """Search in knowledge base."""
    try:
        results = similarity_search(q, k=k)
        return {"query": q, "results": results, "count": len(results)}
    except Exception as e:
        return {"query": q, "results": [], "error": str(e)}


@app.get("/api/mcp/tools")
async def mcp_tools():
    """List available MCP tools."""
    tools = get_mcp_tools()
    return {
        "tools": [
            {"name": t.name, "description": t.description} 
            for t in tools
        ]
    }


# Alias paths para compatibilidade
app.add_route("/chat", app.routes[app.routes.index("/api/chat")], methods=["POST"])
app.add_route("/chat/stream", app.routes[app.routes.index("/api/chat/stream")], methods=["POST"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))