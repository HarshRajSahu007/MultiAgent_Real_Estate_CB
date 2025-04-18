from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,END
from typing import Literal,TypedDict,List,Dict,Any,Optional
import json

from agents.router_agent import route_query
from agents.issue_agent import process_issue
from MultiAgent_Real_Estate_CB.agents.tenancy_agent import answer_tenancy_question

class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    agent_type: Optional[Literal["ROUTER", "ISSUE_DETECTION", "TENANCY_FAQ"]]
    image: Optional[Any]
    location: Optional[str]
    query: str
    response: Optional[str]

def create_agent_workflow():
    """
    Create the LangGraph workflow for the multi-agent system
    
    Returns:
        StateGraph: The configured workflow graph
    """

    workflow = StateGraph(AgentState)
    

    workflow.add_node("router", route_query)
    workflow.add_node("issue_detection", process_issue)
    workflow.add_node("tenancy_faq", answer_tenancy_question)
    

    def should_route_to_issue_detection(state):
        return state["agent_type"] == "ISSUE_DETECTION"
    
    def should_route_to_tenancy_faq(state):
        return state["agent_type"] == "TENANCY_FAQ"
    

    workflow.add_conditional_edges(
        "router",
        {
            should_route_to_issue_detection: "issue_detection",
            should_route_to_tenancy_faq: "tenancy_faq",
        },
        default="router"  
    )
    

    workflow.add_edge("issue_detection", END)
    workflow.add_edge("tenancy_faq", END)
    

    workflow.set_entry_point("router")
    
    return workflow