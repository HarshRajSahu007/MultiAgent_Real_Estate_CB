from langchain_openai import ChatOpenAI
from typing import Dict, Any
import json

import config
from utils.image_processor import prepare_image_for_api

def process_issue(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process property issues using image analysis and user query
    
    Args:
        state: Current state including user query, image data, and message history
        
    Returns:
        Dict: Updated state with issue detection response
    """
    query = state["query"]
    image = state["image"]
    
    # Initialize OpenAI vision model
    issue_model = ChatOpenAI(
        temperature=config.ISSUE_DETECTION_TEMPERATURE,
        model=config.ISSUE_DETECTION_MODEL,
        max_tokens=config.MAX_TOKENS,
        api_key=config.OPENAI_API_KEY
    )
    
    # Prepare messages with image if available
    messages = []
    
    # System message with instructions
    messages.append({
        "role": "system", 
        "content": config.ISSUE_DETECTION_BASE_PROMPT
    })
    
    # User message with query and image
    if image:
        # Prepare image for API
        image_data = prepare_image_for_api(image)
        
        # Add user message with text and image
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                image_data
            ]
        })
    else:
        # Text-only query
        messages.append({
            "role": "user",
            "content": query
        })
    
    # Get response from the model
    response = issue_model.invoke(messages)
    
    # Structure the response
    issue_response = {
        "agent": "Issue Detection Agent",
        "analysis": response.content
    }
    
    # Update state with response
    state["response"] = issue_response
    
    return state