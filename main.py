import os
import json
import argparse
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from src.services.session_manager import SessionManager
from src.services.orchestrator import Orchestrator
from src.models.profile import StudentProfile

BASE_DIR = Path(__file__).resolve().parent
DOTENV_PATH = BASE_DIR / ".env"
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH, override=False)

def _resolve_workspace_path(path_str: str) -> Path:
    """Resolve a profile path and ensure it stays within the workspace."""
    candidate = Path(path_str)
    if not candidate.is_absolute():
        candidate = BASE_DIR / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(BASE_DIR)
    except ValueError:
        raise ValueError("Profile paths must reside within the project workspace.")
    return resolved

def load_config():
    import yaml
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_programs():
    # Attempt to read external catalog file; fall back to enriched inline dataset
    candidate_paths = [
        os.path.join("src", "data", "program_catalog.json"),
        os.path.join("src", "data", "sample_programs.json"),
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
            except Exception:
                pass
    # Inline enriched fallback dataset (diverse domains)
    enriched = [
        {"institution": "Nanyang Technological University", "program": "Bachelor of Engineering (Computer Science)", "level": "bachelor", "keywords": ["ai", "data", "software", "algorithms"], "duration_years": 4},
        {"institution": "National University of Singapore", "program": "Bachelor of Business Administration", "level": "bachelor", "keywords": ["finance", "management", "analytics"], "duration_years": 4},
        {"institution": "Singapore Management University", "program": "Bachelor of Accountancy", "level": "bachelor", "keywords": ["accounting", "finance", "audit"], "duration_years": 4},
        {"institution": "Temasek Polytechnic", "program": "Diploma in Data Science & AI", "level": "diploma", "keywords": ["data", "ai", "python"], "duration_years": 3},
        {"institution": "Republic Polytechnic", "program": "Diploma in Cybersecurity", "level": "diploma", "keywords": ["cybersecurity", "network", "security", "cloud"], "duration_years": 3},
        {"institution": "Singapore Institute of Technology", "program": "Bachelor in Robotics Systems", "level": "bachelor", "keywords": ["robotics", "automation", "embedded", "ai"], "duration_years": 4},
        {"institution": "National University of Singapore", "program": "Master of Finance (FinTech)", "level": "masters", "keywords": ["finance", "fintech", "data", "blockchain"], "duration_years": 2},
        {"institution": "National University of Singapore", "program": "Master of Environmental Sustainability", "level": "masters", "keywords": ["sustainability", "environment", "policy", "data"], "duration_years": 2},
        {"institution": "Lasalle College of the Arts", "program": "Diploma in Media Design", "level": "diploma", "keywords": ["design", "media", "creativity", "ux"], "duration_years": 3},
        {"institution": "Singapore Polytechnic", "program": "Diploma in Biotechnology", "level": "diploma", "keywords": ["biotech", "lab", "science", "health"], "duration_years": 3},
        {"institution": "Ngee Ann Polytechnic", "program": "Diploma in Digital Marketing Analytics", "level": "diploma", "keywords": ["marketing", "analytics", "data", "branding"], "duration_years": 3},
        {"institution": "National University of Singapore", "program": "Master of Education Technology", "level": "masters", "keywords": ["education", "technology", "learning", "design"], "duration_years": 2},
    ]
    return enriched

def build_profile_interactive() -> StudentProfile:
    name = input("Student name: ") or "Anonymous"
    interests = [i.strip() for i in input("Interests (comma separated): ").split(",") if i.strip()]
    strengths = [i.strip() for i in input("Strengths (comma separated): ").split(",") if i.strip()]
    constraints = [i.strip() for i in input("Constraints (comma separated): ").split(",") if i.strip()]
    target_level = input("Target level (diploma/bachelor/masters): ") or None
    budget = input("Budget category (low/medium/high): ") or None
    return StudentProfile(
        name=name,
        interests=interests,
        strengths=strengths,
        constraints=constraints,
        target_level=target_level,
        budget_category=budget,
    )

def parse_args():
    parser = argparse.ArgumentParser(description="Singapore Education Counselor")
    parser.add_argument("--interactive", action="store_true", help="Prompt for student profile inputs")
    parser.add_argument("--no-summary", action="store_true", help="Disable LLM summarization")
    parser.add_argument("--refine", type=str, default=None, help="Refinement feedback to adjust profile")
    parser.add_argument("--save-profile", type=str, help="Path to save profile JSON")
    parser.add_argument("--load-profile", type=str, help="Load profile from JSON path")
    return parser.parse_args()

def google_connectivity_check():
    """Lightweight Vertex AI connectivity check using environment variables.

    Skips if:
      - CONNECTIVITY_CHECK env var is explicitly set to '0'
      - vertexai SDK not installed
      - Required environment variables not set
    Prints status messages; does not raise to avoid breaking main flow.
    """
    if os.getenv("CONNECTIVITY_CHECK", "1") in ("0", "false", "False"):
        return
    
    project_id = os.getenv("GOOGLE_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        return
    try:
        from vertexai import init as vertexai_init
        from vertexai.generative_models import GenerativeModel
    except Exception:
        return
    location = os.getenv("VERTEX_LOCATION", "us-central1")
    model_name = os.getenv("CONNECTIVITY_MODEL", "gemini-2.5-flash-lite")
    try:
        if not project_id:
            pass
        vertexai_init(project=project_id, location=location)
        model = GenerativeModel(model_name)
        # Minimal test prompt; very short to reduce cost.
        resp = model.generate_content("ping")
        ok = False
        text = getattr(resp, "text", None)
        if text:
            ok = True
        elif getattr(resp, "candidates", None):
            # Attempt to extract any text parts
            try:
                for c in resp.candidates:
                    parts = getattr(c, "content", None)
                    if parts and getattr(parts, "parts", None):
                        for p in parts.parts:
                            t = getattr(p, "text", None)
                            if t:
                                ok = True
                                break
                    if ok:
                        break
            except Exception:
                pass
        if ok:
            pass
        else:
            pass
    except Exception:
        pass

def main():
    args = parse_args()
    pass
    # Optional corporate proxy support: if HTTP_PROXY env not preset but PROXY_URL provided, set it.
    proxy_url = os.getenv("PROXY_URL") or os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
    if proxy_url:
        # Force both protocols to use the same corporate proxy endpoint
        os.environ["HTTP_PROXY"] = proxy_url
        os.environ["HTTPS_PROXY"] = proxy_url
        pass
    else:
        # Example: to enable inside corporate network set PROXY_URL or HTTP_PROXY before running.
        # PowerShell:  $env:PROXY_URL = 'http://blrproxy.ad.infosys.com:80'
        pass
    # Proactive connectivity check (non-fatal)
    google_connectivity_check()
    config = load_config()
    if args.no_summary:
        config.setdefault("orchestrator", {})["summarizer"] = False
    data_store = {
        "programs": load_programs(),
        "financial_aid": [
            {"name": "Need-Based Bursary", "tags": ["need"], "approx_amount": 2000},
            {"name": "Merit Scholarship", "tags": ["merit"], "approx_amount": 5000},
        ],
    }
    if args.load_profile:
        try:
            load_path = _resolve_workspace_path(args.load_profile)
        except ValueError as exc:
            pass
            return
        if load_path.exists():
            with open(load_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            pass
            return
        profile = StudentProfile(**data)
    elif args.interactive:
        profile = build_profile_interactive()
    else:
        profile = StudentProfile(
            name="Hackathon Demo",
            interests=["AI", "Finance"],
            strengths=["Math", "Problem Solving"],
            constraints=["time"],
            target_level="bachelor",
            budget_category="low",
        )
    session = SessionManager()
    if args.refine:
        profile = session.refine_profile(profile, args.refine)
    orchestrator = Orchestrator(config, data_store)
    result = orchestrator.run(profile)
    session.add_turn(profile, result)
    if result.get("cached"):
        pass
    pass
    for agent_name, payload in result["agents"].items():
        pass
    if "summary" in result:
        pass
        # Indicate which backend was used for clarity
        backend = getattr(orchestrator.genai, "backend", None)
        if backend:
            pass
        else:
            pass
    if args.save_profile:
        try:
            save_path = _resolve_workspace_path(args.save_profile)
        except ValueError as exc:
            pass
            return
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(profile.model_dump(), f, indent=2)
        pass
    # Show simple session length
    pass

if __name__ == "__main__":
    main()
