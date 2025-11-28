"""
Quick test script for Web Search Agent
Tests Google Custom Search API integration
"""
import os
import sys

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Check if API keys are set
api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")

if not api_key:
    sys.exit(1)

if not search_engine_id:
    sys.exit(1)

try:
    from src.agents.web_search_agent import WebSearchAgent
    from src.agents.base import AgentContext
except Exception as e:
    sys.exit(1)

try:
    context = AgentContext(
        config={}, 
        data_store={}, 
        vector_store=None
    )
    agent = WebSearchAgent(context)
except Exception as e:
    sys.exit(1)

test_profile = {
    "interests": ["Artificial Intelligence"],
    "target_level": "degree"
}

try:
    result = agent.run(test_profile)
    
    if result.get("enabled") == False:
        pass
    else:
        search_results = result.get("search_results", [])
        if search_results:
            for i, res in enumerate(search_results[:3], 1):
                pass
    
except Exception as e:
    sys.exit(1)