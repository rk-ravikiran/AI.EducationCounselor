from src.services.orchestrator import Orchestrator
from src.models.profile import StudentProfile
from src.services.embedding_client import EmbeddingClient
import json, os, time

CONFIG = {
    "agents": {"enabled": ["institutional_data"]},
    "orchestrator": {"summarizer": False, "max_program_results": 3, "cache_ttl_seconds": 5},
    "models": {"llm": "gemini-1.5-flash"},
}

PROGRAMS = [
    {"institution": "A", "program": "Diploma in AI", "keywords": ["ai", "data"]},
    {"institution": "B", "program": "Diploma in Business", "keywords": ["finance", "management"]},
]

def test_embedding_ordering():
    data_store = {"programs": PROGRAMS}
    orch = Orchestrator(CONFIG, data_store)
    profile = StudentProfile(name="S", interests=["AI"], strengths=[], constraints=[], budget_category=None)
    result = orch.run(profile)
    suggestions = result["agents"]["institutional_data"]["program_suggestions"]
    assert len(suggestions) >= 2
    # First suggestion should have highest or equal score
    scores = [s.get("score", 0) for s in suggestions]
    assert scores[0] >= scores[1]


def test_cache_behavior():
    data_store = {"programs": PROGRAMS}
    orch = Orchestrator(CONFIG, data_store)
    profile = StudentProfile(name="S", interests=["AI"], strengths=[], constraints=[], budget_category=None)
    first = orch.run(profile)
    second = orch.run(profile)
    assert second.get("cached") is True
    time.sleep(CONFIG["orchestrator"]["cache_ttl_seconds"] + 1)
    third = orch.run(profile)
    assert not third.get("cached")
