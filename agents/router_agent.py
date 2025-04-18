from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict, Any
from logging import getLogger
import openai
import config

logger = getLogger(__name__)  # corrected logger initialization

router_model = ChatOpenAI(
    model="gpt-3.5-turbo",  # switch to a cheaper model if you're using gpt-4
    temperature=0,
    openai_api_key=config.OPENAI_API_KEY
)


def route_query(state: Dict[str, Any]) -> Dict[str, Any]:
    """Route the user query to the appropriate agent"""
    query = state.get("query", "")
    has_image = state.get("image") is not None

    # Default to TENANCY_FAQ if no image and query is text-based
    if not has_image and isinstance(query, str) and len(query.strip()) > 0:
        state["agent_type"] = "TENANCY_FAQ"
        return state

    # Only use LLM routing for ambiguous cases
    router_prompt = f"""
    {config.ROUTER_BASE_PROMPT}
    User query: "{query}"
    Has image attachment: {has_image}
    """

    try:
        response = router_model.invoke(router_prompt)
        response_text = response.content.upper()

        if "ISSUE_DETECTION" in response_text and has_image:
            state["agent_type"] = "ISSUE_DETECTION"
        else:
            state["agent_type"] = "TENANCY_FAQ"

    except openai.error.RateLimitError as e:
        logger.error(f"OpenAI quota exceeded: {e}")
        state["agent_type"] = "TENANCY_FAQ"  # fallback route

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI error: {e}")
        state["agent_type"] = "TENANCY_FAQ"  # fallback route

    except Exception as e:
        logger.error(f"Router failed: {str(e)}")
        state["agent_type"] = "TENANCY_FAQ"  # fallback route

    return state
