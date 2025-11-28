import json
from src.services.orchestrator import Orchestrator
from src.models.profile import StudentProfile
from src.services.session_manager import SessionManager

CONFIG_BASE = {
    "agents": {"enabled": ["institutional_data", "career_guidance", "financial_aid", "admission_advisor"]},
    "orchestrator": {"summarizer": False, "max_program_results": 2, "use_vector_store": True},
    "models": {"llm": "gemini-2.5-flash-lite"},
}

PROGRAMS = [
    {"institution": "InstA", "program": "Diploma in AI", "keywords": ["ai", "data"], "duration_years": 3},
    {"institution": "InstB", "program": "Bachelor of Finance", "keywords": ["finance", "management"], "duration_years": 4},
    {"institution": "InstC", "program": "Certificate in Media Design", "keywords": ["design", "media"], "duration_months": 9},
    {"institution": "InstD", "program": "Advanced Data Analytics", "keywords": ["data", "analytics"], "duration_years": 1},
]


def build_orchestrator(extra_config=None):
    cfg = json.loads(json.dumps(CONFIG_BASE))  # deep copy
    if extra_config:
        # shallow merge for test simplicity
        for k, v in extra_config.items():
            if isinstance(v, dict) and k in cfg:
                cfg[k].update(v)
            else:
                cfg[k] = v
    data_store = {"programs": PROGRAMS, "financial_aid": [
        {"name": "Need-Based Bursary", "tags": ["need"], "approx_amount": 2000},
        {"name": "Merit Scholarship", "tags": ["merit"], "approx_amount": 5000},
    ]}
    return Orchestrator(cfg, data_store)


def test_program_explanations_present():
    orch = build_orchestrator()
    profile = StudentProfile(name="Test", interests=["AI", "Finance"], strengths=[], constraints=[], budget_category="low")
    result = orch.run(profile)
    agent_payload = result["agents"].get("institutional_data", {})
    assert "error" not in agent_payload, f"Agent error: {agent_payload.get('error')}"
    suggestions = agent_payload.get("program_suggestions", [])
    assert suggestions, "Expected at least one program suggestion"
    for s in suggestions:
        expl = s.get("explanation")
        assert expl, "Explanation missing"
        for key in ["matched_keywords", "similarity_score", "reason"]:
            assert key in expl, f"Explanation key {key} missing"


def test_vector_store_augmentation_increases_results():
    # Force low max_program_results to see augmentation add more
    orch = build_orchestrator({"orchestrator": {"max_program_results": 1}})
    profile = StudentProfile(name="VecTest", interests=["Design"], strengths=[], constraints=[], budget_category=None)
    result = orch.run(profile)
    suggestions = result["agents"]["institutional_data"]["program_suggestions"]
    assert len(suggestions) >= 2, "Expected augmentation to add extra suggestions beyond initial max"
    reasons = [s.get("explanation", {}).get("reason", "") for s in suggestions]
    assert any(r.startswith("VectorStore retrieval") for r in reasons), "No VectorStore retrieval reason found in augmented suggestions"


def test_profile_persistence_roundtrip():
    profile = StudentProfile(name="Persist", interests=["AI"], strengths=["Math"], constraints=["time"], target_level="bachelor", budget_category="low")
    as_json = json.dumps(profile.model_dump())
    data = json.loads(as_json)
    restored = StudentProfile(**data)
    assert restored.name == profile.name
    assert restored.interests == profile.interests
    assert restored.strengths == profile.strengths
    assert restored.constraints == profile.constraints
    assert restored.target_level == profile.target_level
    assert restored.budget_category == profile.budget_category


def test_session_refine_adds_interest_and_budget():
    sm = SessionManager()
    profile = StudentProfile(name="Refine", interests=["AI"], strengths=[], constraints=[], budget_category="medium")
    refined = sm.refine_profile(profile, "I want finance and budget low opportunities")
    assert any(i.lower() == "finance" for i in refined.interests), "Finance interest not added"
    assert refined.budget_category == "low", "Budget category not updated to low"