from langchain_openai import ChatOpenAI
from typing import Dict, Any
import re
import json
import config
from utils.knowledge_base import get_region_info, get_general_tenancy_info, get_common_question_answer

def extract_location(text):
    """
    Extract potential location mentions from text
    
    Args:
        text: User query text
        
    Returns:
        str or None: Extracted location if found
    """
    # Common location patterns
    country_pattern = r'in\s+([A-Z][a-z]+|USA|UK|US|EU|UAE)'
    city_state_pattern = r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    
    # Try to find countries first
    country_match = re.search(country_pattern, text)
    if country_match:
        return country_match.group(1)
    
    # Try cities/states
    city_match = re.search(city_state_pattern, text)
    if city_match:
        return city_match.group(1)
    
    return None

def answer_tenancy_question(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Answer tenancy and rental agreement questions
    
    Args:
        state: Current state including user query and message history
        
    Returns:
        Dict: Updated state with tenancy answer
    """
    query = state["query"]
    location = state["location"] or extract_location(query)
    
    # Get relevant knowledge base information
    regional_info = get_region_info(location) if location else None
    general_info = get_general_tenancy_info()
    
    # Create context for the model
    context = "General tenancy information:\n"
    context += json.dumps(general_info, indent=2) + "\n\n"
    
    if regional_info:
        context += f"Region-specific information for {location}:\n"
        context += json.dumps(regional_info, indent=2) + "\n\n"
    
    # Create the full prompt
    tenancy_prompt = f"""
    {config.TENANCY_FAQ_BASE_PROMPT}
    
    Knowledge base context:
    {context}
    
    User location: {location if location else "Unknown"}
    
    User query: "{query}"
    
    Provide helpful, accurate information based on common tenancy laws and regulations.
    If location-specific details would be important, mention this in your response.
    """
    
    # Initialize OpenAI model
    tenancy_model = ChatOpenAI(
        temperature=config.TENANCY_FAQ_TEMPERATURE,
        model=config.TENANCY_FAQ_MODEL,
        max_tokens=config.MAX_TOKENS,
        api_key=config.OPENAI_API_KEY
    )
    
    # Get response from the model
    response = tenancy_model.invoke(tenancy_prompt)
    
    # Structure the response
    tenancy_response = {
        "agent": "Tenancy FAQ Agent",
        "answer": response.content,
        "location_used": location if location else "None specified"
    }
    
    # Update state with response
    state["response"] = tenancy_response
    
    return state