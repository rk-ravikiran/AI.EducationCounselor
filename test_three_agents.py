"""
Test the 3 core AI-powered agents: Programs, Career, Financial Aid
This validates LLM reasoning quality in the transformed architecture
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.profile import StudentProfile
from src.services.orchestrator import Orchestrator
from src.services.genai_client import GenAIClient
from src.services.vector_store import VectorStore
from src.services.session_manager import SessionManager

def test_three_agent_system():
    """Test end-to-end flow with 3 AI-powered agents"""
    
    # Initialize services
    import yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    data_store = {}  # No need for preloaded data, agents load from JSON files
    
    # Create test student profile
    profile = StudentProfile(
        name="Test Student",
        interests=["artificial intelligence", "healthcare", "research"],
        strengths=["mathematics", "problem solving", "Python programming"],
        budget_category="moderate",
        target_level="degree",
        constraints=["Singapore Citizen", "prefer university over polytechnic"]
    )
    
    # Initialize orchestrator with simple approach
    orchestrator = Orchestrator(config, data_store)
    pass
    
    # Run orchestrator
    try:
        result = orchestrator.run(profile)
        
        pass
        pass
        pass
        
        # Check Programs Agent
        programs = result.get("institutional_data", {}).get("programs", [])
        pass
        if programs:
            pass
            if programs[0].get("reasoning_type") == "ai_counselor_reasoning":
                pass
                pass
            else:
                pass
        
        # Check Career Agent
        career = result.get("career_guidance", {})
        careers = career.get("recommended_careers", [])
        pass
        if careers:
            pass
            if "fit_analysis" in careers[0]:
                pass
                pass
            else:
                pass
        
        # Check Financial Aid Agent
        aid = result.get("financial_aid", {})
        aid_options = aid.get("aid_options", [])
        pass
        if aid_options:
            pass
            if aid_options[0].get("reasoning_type") == "ai_financial_counseling":
                pass
                pass
                pass
            else:
                pass
        
        # Overall assessment
        pass
        pass
        pass
        
        ai_reasoning_count = 0
        if programs and programs[0].get("reasoning_type") == "ai_counselor_reasoning":
            ai_reasoning_count += 1
        if careers and "fit_analysis" in careers[0]:
            ai_reasoning_count += 1
        if aid_options and aid_options[0].get("reasoning_type") == "ai_financial_counseling":
            ai_reasoning_count += 1
        
        pass
        
        if ai_reasoning_count == 3:
            pass
        elif ai_reasoning_count >= 2:
            pass
        else:
            pass
        
        # Summary check
        summary = result.get("orchestrator_summary", "")
        if summary:
            pass
            pass
        
        pass
        pass
        pass
        
        return result
        
    except Exception as e:
        pass
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_three_agent_system()
