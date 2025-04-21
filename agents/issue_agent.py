from langchain_openai import ChatOpenAI
from typing import Dict, Any
import logging
import config
from utils.image_processor import prepare_image_for_api

logger = logging.getLogger(__name__)

def process_issue(state: Dict[str, Any]) -> Dict[str, Any]:
    """Process property issues with guaranteed response"""
    try:
        query = state.get("query", "Please analyze this image")
        image = state.get("image")
        print("Inside Process issue function")
        if not image:
            raise ValueError("No image provided for analysis")
            
        # Prepare the model with fallback configuration
        model_config = {
            "temperature": getattr(config, "ISSUE_DETECTION_TEMPERATURE", 0.2),
            "model": getattr(config, "ISSUE_DETECTION_MODEL", "gpt-4-vision-preview"),
            "max_tokens": getattr(config, "MAX_TOKENS", 1000),
            "api_key": getattr(config, "OPENAI_API_KEY", "")
        }
        
        # Prepare the prompt
        base_prompt = getattr(config, "ISSUE_DETECTION_BASE_PROMPT", 
                            "Analyze this property issue image and describe any problems:")
        
        # Create messages
        messages = [{
            "role": "system",
            "content": base_prompt
        }]
        
        try:
            image_data = prepare_image_for_api(image)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    image_data
                ]
            })
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise ValueError("Failed to process image") from e
            
        # Get response
        try:
            model = ChatOpenAI(**model_config)
            response = model.invoke(messages)
            
            if not response or not hasattr(response, 'content'):
                raise ValueError("Invalid response from model")
                
            analysis = response.content.strip()
            if not analysis:
                raise ValueError("Empty analysis response")
                
            state["response"] = {
                "agent": "Issue Detection Agent",
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise ValueError("Failed to analyze image") from e
            
    except Exception as e:
        logger.error(f"Issue detection failed: {str(e)}")
        state["response"] = {
            "agent": "Issue Detection Agent",
            "analysis": f"Unable to analyze the image: {str(e)}"
        }
        
    return state

class IssueDetectionAgent:
    def run(self, image_bytes, query):
        state = {
            "query": query,
            "image": image_bytes
        }
        result_state = process_issue(state)
        return result_state.get("response")
