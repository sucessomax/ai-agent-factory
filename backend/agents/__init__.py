from langchain.schema import SystemMessage, HumanMessage
from llm.client import get_llm

def create_supervisor_agent():
    llm = get_llm(temperature=0.3)
    
    system_prompt = """Você é o Supervisor de uma equipe de agentes de IA.
    
Sua responsabilidade é:
1. Analisar o request do usuário
2. Decidir qual agente deve atuar next
3. CoordenAR a comunicação entre agentes

Agentes disponíveis:
- researcher: Para buscar informações e pesquisar na base de conhecimento
- executor: Para executar ações, ler/gravar arquivos, rodar comandos
- reviewer: Para revisar e validar respostas

Retorne sempre qual agente deve atuar e uma breve descrição do que deve ser feito."""

    def invoke(messages: list) -> str:
        response = llm.invoke(messages)
        return response.content
    
    return {"invoke": invoke, "system": system_prompt}


def create_researcher_agent():
    llm = get_llm(temperature=0.5)
    
    system_prompt = """Você é o Researcher Agent, especializado em pesquisar informações.

Sua responsabilidade:
1. Buscar informações na base de conhecimento vetorial (RAG)
2. Analisar documentos e extrair informações relevantes
3. Fornecer contexto para outras respostas

Always cite suas fontes quando possível."""

    def invoke(query: str, context: list = None) -> str:
        messages = [("system", system_prompt)]
        if context:
            messages.append(("system", f"Contexto disponível:\n{chr(10).join(context)}"))
        messages.append(("user", query))
        
        response = llm.invoke(messages)
        return response.content
    
    return {"invoke": invoke, "system": system_prompt}


def create_executor_agent():
    llm = get_llm(temperature=0.2)
    
    system_prompt = """Você é o Executor Agent, especializado em executar ações.

Sua responsabilidade:
1. Ler arquivos do sistema
2. Gravar informações
3. Executar comandos
4. Manipular dados

Use as tools disponíveis para completar as tarefas.
 sempre confirme quando uma ação for completada."""

    def invoke(task: str, tools_results: dict = None) -> str:
        messages = [("system", system_prompt)]
        if tools_results:
            results_str = "\n".join([f"{k}: {v}" for k, v in tools_results.items()])
            messages.append(("system", f"Resultados de tools:\n{results_str}"))
        messages.append(("user", task))
        
        response = llm.invoke(messages)
        return response.content
    
    return {"invoke": invoke, "system": system_prompt}


def create_reviewer_agent():
    llm = get_llm(temperature=0.4)
    
    system_prompt = """Você é o Reviewer Agent, responsável por validar a qualidade.

Sua responsabilidade:
1. Avaliar a resposta final
2. Verificar se atende ao request do usuário
3. Sugerir melhorias se necessário
4. Garantir que informações importantes não foram omitidas

Forneça feedback construtivo."""

    def invoke(response: str, original_request: str) -> str:
        messages = [
            ("system", system_prompt),
            ("user", f"Request original: {original_request}\n\nResposta a revisar:\n{response}")
        ]
        
        response = llm.invoke(messages)
        return response.content
    
    return {"invoke": invoke, "system": system_prompt}


def create_pentest_agent():
    """Agente de Pentest para analisar vulnerabilidades em código."""
    llm = get_llm(temperature=0.3)
    
    system_prompt = """Você é o Pentest Agent - especialista em segurança de aplicações.

Sua responsabilidade:
1. Analisar código em busca de vulnerabilidades
2. Detectar padrões perigosos (eval, os.system, shell=True, etc)
3. Identificar segredos expostos (API keys, passwords hardcoded)
4. Verificar dependências com CVEs conhecidas
5. Mapear findings para CWEs relevantes
6. Sugerir correções de segurança

Sempre seja detalhado nas correções sugeridas."""

    def invoke(code: str, context: dict = None) -> str:
        messages = [
            ("system", system_prompt),
            ("user", f"Analise o seguinte código para vulnerabilidades:\n\n{code}")
        ]
        
        response = llm.invoke(messages)
        return response.content
    
    return {"invoke": invoke, "system": system_prompt}