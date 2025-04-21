from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,END
from typing import Literal,TypedDict,List,Dict,Any,Optional
import json

from agents.router_agent import route_query
from agents.issue_agent import process_issue
from agents.tenancy_agent import answer_tenancy_question

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
    
    # Add nodes
    workflow.add_node("router", route_query)
    workflow.add_node("issue_detection", process_issue)
    workflow.add_node("tenancy_faq", answer_tenancy_question)
    
    # Define condition functions
    def route_to_issue_detection(state):
        return state["agent_type"] == "ISSUE_DETECTION"
    
    def route_to_tenancy_faq(state):
        return state["agent_type"] == "TENANCY_FAQ"
    
    # Add conditional edges with string keys
    workflow.add_conditional_edges(
        "router",route_to_issue_detection,
        {
            True: "issue_detection",
            False: "tenancy_faq",
        }
    )
    
    # Add terminal edges
    workflow.add_edge("issue_detection", END)
    workflow.add_edge("tenancy_faq", END)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    return workflow
def initialize_state(query: str, image=None, location=None):
    """
    Initialize the agent state
    
    Args:
        query: User's text query
        image: Optional image file
        location: Optional location information
        
    Returns:
        AgentState: The initialized state
    """
    return {
        "messages": [{"role": "user", "content": query}],
        "agent_type": "ROUTER",  # Start with the router
        "image": image,
        "location": location,
        "query": query,
        "response": None
    }

def execute_workflow(workflow, state):
    """
    Execute the agent workflow
    
    Args:
        workflow: The LangGraph workflow
        state: The initial state
        
    Returns:
        AgentState: The final state after workflow execution
    """
    # Create a compiled workflow for better performance
    app = workflow.compile()
    
    # Execute the workflow and get the final state
    result = app.invoke(state)
    
    return result