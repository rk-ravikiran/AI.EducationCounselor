import os, time, csv, uuid
from datetime import datetime
from src.services.orchestrator import Orchestrator
from src.models.profile import StudentProfile

# Simple batch profiles for evaluation
PROFILES = [
    StudentProfile(name="EvalAI", interests=["AI"], strengths=["Math"], constraints=[], budget_category="low"),
    StudentProfile(name="EvalFinance", interests=["Finance"], strengths=["Excel"], constraints=["time"], budget_category="low"),
    StudentProfile(name="EvalDesign", interests=["Design"], strengths=["Creativity"], constraints=[], budget_category="medium"),
    StudentProfile(name="EvalRobotics", interests=["Robotics"], strengths=["Python"], constraints=["budget"], budget_category="low"),
]

CONFIG = {
    "agents": {"enabled": [
        "institutional_data", "career_guidance", "skill_gap", "scholarship_matcher", "learning_path", "interview_prep"
    ]},
    "orchestrator": {"summarizer": False, "max_program_results": 5, "use_vector_store": True},
    "models": {"llm": os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")},
}

def run_evaluation():
    data_store = {"programs": []}  # main load_programs will fallback to enriched inline
    # We call load_programs from main for consistency without importing yaml
    from main import load_programs
    data_store["programs"] = load_programs()
    orch = Orchestrator(CONFIG, data_store)
    rows = []
    for profile in PROFILES:
        start = time.time()
        result = orch.run(profile)
        latency_ms = int((time.time() - start) * 1000)
        prog_suggestions = result["agents"].get("institutional_data", {}).get("program_suggestions", [])
        scholarships = result["agents"].get("scholarship_matcher", {}).get("scholarship_recommendations", [])
        skill_gaps = result["agents"].get("skill_gap", {}).get("skill_gaps", [])
        learning_paths = result["agents"].get("learning_path", {}).get("learning_paths", {})
        rows.append({
            "profile": profile.name,
            "interests": ";".join(profile.interests or []),
            "suggestion_count": len(prog_suggestions),
            "scholarship_count": len(scholarships),
            "skill_gap_count": len(skill_gaps),
            "learning_path_topics": sum(len(v) for v in learning_paths.values()),
            "latency_ms": latency_ms,
        })
    out_dir = "exports"
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(out_dir, f"eval_results_{ts}.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    run_evaluation()
