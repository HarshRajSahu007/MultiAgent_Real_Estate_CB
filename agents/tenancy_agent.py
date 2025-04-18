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
  
    country_pattern = r'in\s+([A-Z][a-z]+|USA|UK|US|EU|UAE)'
    city_state_pattern = r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    
 
    country_match = re.search(country_pattern, text)
    if country_match:
        return country_match.group(1)
    

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
    

    regional_info = get_region_info(location) if location else None
    general_info = get_general_tenancy_info()
    

    context = "General tenancy information:\n"
    context += json.dumps(general_info, indent=2) + "\n\n"
    
    if regional_info:
        context += f"Region-specific information for {location}:\n"
        context += json.dumps(regional_info, indent=2) + "\n\n"
    

    tenancy_prompt = f"""
    {config.TENANCY_FAQ_BASE_PROMPT}
    
    Knowledge base context:
    {context}
    
    User location: {location if location else "Unknown"}
    
    User query: "{query}"
    
    Provide helpful, accurate information based on common tenancy laws and regulations.
    If location-specific details would be important, mention this in your response.
    """
    

    tenancy_model = ChatOpenAI(
        temperature=config.TENANCY_FAQ_TEMPERATURE,
        model=config.TENANCY_FAQ_MODEL,
        max_tokens=config.MAX_TOKENS,
        api_key=config.OPENAI_API_KEY
    )
    

    response = tenancy_model.invoke(tenancy_prompt)
    

    tenancy_response = {
        "agent": "Tenancy FAQ Agent",
        "answer": response.content,
        "location_used": location if location else "None specified"
    }
    

    state["response"] = tenancy_response
    
    return state