from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
import re
import json
import logging
import config
from utils.knowledge_base import get_region_info, get_general_tenancy_info

logger = logging.getLogger(__name__)

def extract_location(text: str) -> Optional[str]:
    """Extract location from text with basic pattern matching"""
    try:
        if not text:
            return None
            
        patterns = [
            r'\bin\s+([A-Z][a-z]+|USA|UK|US|UAE)\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    except Exception as e:
        logger.error(f"Location extraction error: {str(e)}")
        return None

def answer_tenancy_question(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle tenancy questions with guaranteed response"""
    try:
        query = state.get("query", "")
        if not query:
            raise ValueError("Empty query")
            
        location = state.get("location") or extract_location(query) or ""
        
        # Get knowledge base info
        try:
            general_info = get_general_tenancy_info() or {}
            regional_info = get_region_info(location) if location else None
        except Exception as e:
            logger.error(f"Knowledge base error: {str(e)}")
            general_info = {}
            regional_info = None

        # Build context
        context = ["General tenancy information:"]
        try:
            context.append(json.dumps(general_info, indent=2))
        except:
            context.append(str(general_info))
            
        if regional_info:
            context.append(f"\nRegion-specific info for {location}:")
            try:
                context.append(json.dumps(regional_info, indent=2))
            except:
                context.append(str(regional_info))
                
        context_str = "\n".join(context)

        # Create prompt
        prompt = f"""
        {getattr(config, 'TENANCY_FAQ_BASE_PROMPT', 'Answer this tenancy question:')}
        
        Context:
        {context_str}
        
        Location: {location or 'Not specified'}
        Question: "{query}"
        
        Provide a helpful response about tenancy laws and rights.
        """
        
        # Get response
        try:
            model = ChatOpenAI(
                temperature=getattr(config, 'TENANCY_FAQ_TEMPERATURE', 0.7),
                model=getattr(config, 'TENANCY_FAQ_MODEL', 'gpt-3.5-turbo'),
                max_tokens=getattr(config, 'MAX_TOKENS', 500),
                api_key=getattr(config, 'OPENAI_API_KEY', '')
            )
            response = model.invoke(prompt)
            answer = response.content if response else "I couldn't generate a response."
        except Exception as e:
            logger.error(f"API error: {str(e)}")
            answer = "I'm having trouble answering right now. Please try again later."

        state["response"] = {
            "agent": "Tenancy FAQ Agent",
            "answer": answer,
            "location_used": location or "None specified"
        }
        
    except Exception as e:
        logger.error(f"Tenancy agent failed: {str(e)}")
        state["response"] = {
            "agent": "Tenancy FAQ Agent", 
            "answer": "I couldn't process your question. Please try again.",
            "location_used": "None specified"
        }
        
    return state
