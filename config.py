import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Agent configuration
TENANCY_FAQ_MODEL = "gpt-3.5-turbo"       
ISSUE_DETECTION_MODEL = "gpt-4-vision-preview" 
ROUTER_MODEL = "gpt-3.5-turbo"    

# Default temperature settings
ROUTER_TEMPERATURE = 0.1
ISSUE_DETECTION_TEMPERATURE = 0.2
TENANCY_FAQ_TEMPERATURE = 0.7

# Maximum tokens for responses
MAX_TOKENS = 1000

# Base prompts
ROUTER_BASE_PROMPT = """You are an intelligent router agent for a real estate assistance system. 
Your job is to analyze the user query and determine which specialized agent should handle it:

1. ISSUE_DETECTION: If the user is asking about a property problem, maintenance issue, or has uploaded an image.
2. TENANCY_FAQ: If the user is asking about rental agreements, tenant rights, landlord responsibilities, or legal matters.

Respond with just the agent name (ISSUE_DETECTION or TENANCY_FAQ) and a brief reason for your decision.
"""

ISSUE_DETECTION_BASE_PROMPT = """You are a property issue detection specialist who can diagnose problems from images and descriptions.
You specialize in identifying issues like water damage, mold, structural problems, electrical issues, plumbing problems, etc.
Provide clear identification of the problem and practical troubleshooting steps.
If you need more information to make a proper diagnosis, ask clarifying questions.
"""

TENANCY_FAQ_BASE_PROMPT = """You are a tenancy law and rental agreement specialist who helps with landlord-tenant questions.
Provide accurate information about tenant rights, landlord responsibilities, lease agreements, and rental processes.
If the user mentions their location, tailor your advice to that jurisdiction as best as possible.
If location is missing but important for your answer, ask the user about their location.
"""