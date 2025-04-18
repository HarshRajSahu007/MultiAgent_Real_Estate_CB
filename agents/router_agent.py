from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict, Any

import config

def route_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route the user query to the appropriate agent
    
    Args:
        state: Current state including user query and message history
        
    Returns:
        Dict: Updated state with routing decision
    """
    query = state["query"]
    has_image = state["image"] is not None
    
    # Create routing prompt
    router_prompt = f"""
    {config.ROUTER_BASE_PROMPT}

    User query: "{query}"
    
    Has image attachment: {has_image}
    
    Determine the most appropriate agent to handle this query.
    """
    

    router_model = ChatOpenAI(
        temperature=config.ROUTER_TEMPERATURE,
        model=config.ROUTER_MODEL,
        api_key=config.OPENAI_API_KEY
    )
    
    response = router_model.invoke(router_prompt)
    response_text = response.content
    
    agent_type = None
    if "ISSUE_DETECTION" in response_text.upper():
        agent_type = "ISSUE_DETECTION"
    elif "TENANCY_FAQ" in response_text.upper():
        agent_type = "TENANCY_FAQ"
    else:
        agent_type = "ISSUE_DETECTION" if has_image else "TENANCY_FAQ"
    

    state["agent_type"] = agent_type
    
    return state