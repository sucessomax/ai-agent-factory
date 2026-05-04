from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage, SystemMessage

from agents import (
    create_supervisor_agent,
    create_researcher_agent,
    create_executor_agent,
    create_reviewer_agent
)


class AgentState(TypedDict):
    messages: list
    current_agent: str
    intent: str
    research_context: list
    tool_results: dict
    final_response: str
    review: str
    error: str


def supervisor_node(state: AgentState) -> AgentState:
    """Supervisor decide qual agente deve atuar."""
    supervisor = create_supervisor_agent()
    
    messages = [
        SystemMessage(content=supervisor["system"]),
        HumanMessage(content=state["messages"][-1].content)
    ]
    
    decision = supervisor["invoke"](messages)
    
    # Parse decisão simples
    if "researcher" in decision.lower():
        intent = "research"
    elif "executor" in decision.lower():
        intent = "execute"
    else:
        intent = "research"  # default
    
    return {
        **state,
        "current_agent": "supervisor",
        "intent": intent
    }


def researcher_node(state: AgentState) -> AgentState:
    """Researcher busca informações."""
    researcher = create_researcher_agent()
    
    context = state.get("research_context", [])
    result = researcher.invoke(state["messages"][-1].content, context)
    
    return {
        **state,
        "current_agent": "researcher",
        "research_context": context + [result]
    }


def executor_node(state: AgentState) -> AgentState:
    """Executor executa ações."""
    executor = create_executor_agent()
    
    tool_results = state.get("tool_results", {})
    result = executor.invoke(state["messages"][-1].content, tool_results)
    
    return {
        **state,
        "current_agent": "executor",
        "tool_results": {**tool_results, "executor_result": result}
    }


def reviewer_node(state: AgentState) -> AgentState:
    """Reviewer valida resposta."""
    reviewer = create_reviewer_agent()
    
    response = state.get("final_response", "")
    original = state["messages"][-1].content
    
    review = reviewer.invoke(response, original)
    
    return {
        **state,
        "current_agent": "reviewer",
        "review": review
    }


def should_research(state: AgentState) -> Literal["researcher", "executor"]:
    """Decide próximo agente."""
    if state.get("intent") == "execute":
        return "executor"
    return "researcher"


def should_finish(state: AgentState) -> Literal["reviewer", END]:
    """Decide se precisa de review."""
    return "reviewer"


def create_workflow():
    """Cria o stategraph de agentes."""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("reviewer", reviewer_node)
    
    workflow.set_entry_point("supervisor")
    
    workflow.add_conditional_edges(
        "supervisor",
        should_research,
        {"researcher": "researcher", "executor": "executor"}
    )
    
    workflow.add_edge("researcher", "reviewer")
    workflow.add_edge("executor", "reviewer")
    
    workflow.add_conditional_edges(
        "reviewer",
        should_finish,
        {"reviewer": END, END: END}
    )
    
    return workflow.compile()


async def run_agent_workflow(user_message: str) -> dict:
    """Executa o workflow de agentes."""
    workflow = create_workflow()
    
    initial_state = {
        "messages": [HumanMessage(content=user_message)],
        "current_agent": "supervisor",
        "intent": "",
        "research_context": [],
        "tool_results": {},
        "final_response": "",
        "review": "",
        "error": ""
    }
    
    result = await workflow.ainvoke(initial_state)
    
    return {
        "response": result.get("final_response", result.get("research_context", [""])[-1] if result.get("research_context") else ""),
        "agent": result.get("current_agent", "unknown"),
        "intent": result.get("intent", ""),
        "review": result.get("review", "")
    }