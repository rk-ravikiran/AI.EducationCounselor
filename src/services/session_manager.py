from typing import List, Dict, Any
from src.models.profile import StudentProfile

class SessionManager:
    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def add_turn(self, profile: StudentProfile, result: Dict[str, Any]):
        self._history.append({"profile": profile.model_dump(), "result": result})

    def refine_profile(self, profile: StudentProfile, feedback: str) -> StudentProfile:
        # Simple refinement heuristic: if feedback contains new interests or constraints, append.
        lowered = feedback.lower()
        new_interests = []
        for token in lowered.split():
            if token in ["ai", "finance", "design", "media", "data"] and token not in [i.lower() for i in profile.interests]:
                new_interests.append(token.capitalize())
        if new_interests:
            profile.interests.extend(new_interests)
        if "budget" in lowered and "low" in lowered and profile.budget_category != "low":
            profile.budget_category = "low"
        return profile

    def history(self) -> List[Dict[str, Any]]:
        return list(self._history)
