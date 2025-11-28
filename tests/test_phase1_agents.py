from src.services.orchestrator import Orchestrator
from src.models.profile import StudentProfile

CONFIG = {
    "agents": {"enabled": [
        "skill_gap", "scholarship_matcher", "interview_prep", "learning_path", "multilang"
    ]},
    "orchestrator": {"summarizer": False},
    "models": {"llm": "gemini-2.5-flash-lite"},
    "i18n": {"language": "en"},
}

PROFILE = StudentProfile(
    name="Demo", interests=["AI", "Finance"], strengths=["Python"], constraints=[], budget_category="low"
)

def test_skill_gap_agent():
    orch = Orchestrator(CONFIG, {"programs": []})
    result = orch.run(PROFILE)
    gaps = result["agents"]["skill_gap"]["skill_gaps"]
    assert gaps, "Expected skill gaps for missing skills"
    assert any(g["skill"] == "Statistics" for g in gaps)


def test_scholarship_matcher_agent():
    orch = Orchestrator(CONFIG, {"programs": []})
    result = orch.run(PROFILE)
    recs = result["agents"]["scholarship_matcher"]["scholarship_recommendations"]
    assert recs, "Expected scholarship recommendations"
    assert recs[0]["score"] >= recs[-1]["score"]


def test_interview_prep_agent():
    orch = Orchestrator(CONFIG, {"programs": []})
    result = orch.run(PROFILE)
    qs = result["agents"]["interview_prep"]["interview_questions"]
    assert qs, "Expected interview questions"
    assert any(q["interest"] == "AI" for q in qs)


def test_learning_path_agent():
    orch = Orchestrator(CONFIG, {"programs": []})
    result = orch.run(PROFILE)
    paths = result["agents"]["learning_path"]["learning_paths"]
    assert "AI" in paths
    ai_seq = paths["AI"]
    # First topic should have status ready (no prereqs)
    assert ai_seq[0]["status"] == "ready"


def test_multilang_agent_default_en():
    orch = Orchestrator(CONFIG, {"programs": []})
    result = orch.run(PROFILE)
    ml = result["agents"]["multilang"]
    assert ml["language"] == "en"
    assert ml["translation"] is None
