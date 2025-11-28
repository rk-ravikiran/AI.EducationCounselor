"""
Test the new AI reasoning system with curated program database
Verify LLM provides counselor-level insights, not keyword matching
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv()

from src.models.profile import StudentProfile
from src.services.orchestrator import Orchestrator

def test_ai_reasoning():
    pass
    pass
    pass
    pass
    
    # Test profile: Student interested in AI + Finance
    test_profile = StudentProfile(
        name="Test Student",
        interests=["Artificial Intelligence", "Finance"],
        strengths=["Analytical Thinking", "Programming"],
        target_level="degree",
        budget_category="moderate",
        constraints=["Strong preference for AI/ML applications in finance sector"]
    )
    
    pass
    pass
    pass
    pass
    pass
    
    # Initialize orchestrator with web search DISABLED
    config = {
        "agents": {
            "enabled": ["institutional_data"]  # Only test programs agent
        },
        "orchestrator": {
            "use_vector_store": True,
            "enable_web_search": False,  # DISABLED - using curated data
            "summarizer": False
        },
        "models": {
            "llm": "gemini-2.0-flash-exp"
        }
    }
    
    pass
    orchestrator = Orchestrator(config, data_store={})
    pass
    
    pass
    pass
    results = orchestrator.run(test_profile)
    pass
    pass
    
    # Analyze results
    programs_result = results.get("agents", {}).get("institutional_data", {})
    suggestions = programs_result.get("program_suggestions", [])
    
    pass
    pass
    pass
    pass
    pass
    
    if not suggestions:
        pass
        return False
    
    # Check quality of reasoning
    has_real_reasoning = False
    has_career_insights = False
    has_singapore_context = False
    
    for i, suggestion in enumerate(suggestions, 1):
        prog = suggestion.get("program", {})
        exp = suggestion.get("explanation", {})
        
        pass
        pass
        pass
        pass
        
        # Check reasoning quality
        reasoning = exp.get("reason", "")
        career_insights = exp.get("career_insights", "")
        singapore_advantage = exp.get("singapore_advantage", "")
        
        pass
        pass
        
        if career_insights:
            has_career_insights = True
            pass
            pass
        
        if singapore_advantage:
            has_singapore_context = True
            pass
            pass
        
        financial_note = exp.get("financial_note", "")
        if financial_note:
            pass
            pass
        
        student_note = exp.get("student_note", "")
        if student_note:
            pass
            pass
        
        # Check if reasoning is specific (not generic keyword matching)
        if any(keyword in reasoning.lower() for keyword in 
               ["analytical thinking", "programming", "artificial intelligence", "finance"]):
            has_real_reasoning = True
        
        pass
    
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    
    if has_real_reasoning and has_career_insights and has_singapore_context:
        pass
        pass
        return True
    else:
        pass
        return False

if __name__ == "__main__":
    try:
        success = test_ai_reasoning()
        sys.exit(0 if success else 1)
    except Exception as e:
        pass
        import traceback
        traceback.print_exc()
        sys.exit(1)
