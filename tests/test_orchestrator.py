from src.services.orchestrator import Orchestrator
from src.models.profile import StudentProfile

PROGRAMS = [
    {"institution": "Nanyang Technological University", "program": "Bachelor of Engineering (Computer Science)", "keywords": ["ai", "data", "software"], "duration_years": 4},
    {"institution": "National University of Singapore", "program": "Bachelor of Business Administration", "keywords": ["finance", "management"], "duration_years": 4},
    {"institution": "Temasek Polytechnic", "program": "Diploma in Data Science & AI", "keywords": ["data", "ai"], "duration_years": 3},
]

CONFIG = {
    "agents": {"enabled": ["institutional_data", "career_guidance"]},
    "orchestrator": {"summarizer": False, "max_program_results": 3},
    "models": {"llm": "gemini-1.5-flash"},
}

def test_orchestrator_basic():
    data_store = {"programs": PROGRAMS}
    orch = Orchestrator(CONFIG, data_store)
    profile = StudentProfile(name="Alex", interests=["AI"], strengths=["Math"], constraints=[], budget_category="low")
    result = orch.run(profile)
    assert "agents" in result
    assert "institutional_data" in result["agents"]
    assert len(result["agents"]["institutional_data"]["program_suggestions"]) >= 1
    assert result["agents"]["career_guidance"]["career_pathways"][0]["suggested_path"]
