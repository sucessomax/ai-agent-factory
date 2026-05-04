import os
import json
from typing import Any, Callable
from langchain.tools import tool

class MCPClient:
    """Cliente MCP para连接到 servidores."""
    
    def __init__(self):
        self.server_script = os.getenv("MCP_SERVER_SCRIPT", "")
        self._tools = {}
    
    def register_tool(self, name: str, func: Callable):
        """Registra uma ferramenta."""
        self._tools[name] = func
    
    def get_tool(self, name: str) -> Callable:
        """Get tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> list:
        """Lista tools disponíveis."""
        return list(self._tools.keys())


mcp_client = MCPClient()


@mcp_client.register_tool("read_file")
def read_file(path: str) -> str:
    """Lê arquivo do sistema."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"


@mcp_client.register_tool("write_file")
def write_file(path: str, content: str) -> str:
    """Grava arquivo no sistema."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Arquivo escrito: {path}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp_client.register_tool("list_directory")
def list_directory(path: str) -> str:
    """Lista diretório."""
    try:
        files = os.listdir(path)
        return json.dumps(files, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp_client.register_tool("file_exists")
def file_exists(path: str) -> str:
    """Verifica se arquivo existe."""
    return str(os.path.exists(path))


def get_mcp_tools() -> list:
    """Retorna tools como decoradores LangChain."""
    return [
        tool(description="Lê arquivo do sistema de arquivos", name="read_file")(read_file),
        tool(description="Grava conteúdo em arquivo", name="write_file")(write_file),
        tool(description="Lista arquivos em diretório", name="list_directory")(list_directory),
        tool(description="Verifica se arquivo existe", name="file_exists")(file_exists),
    ]