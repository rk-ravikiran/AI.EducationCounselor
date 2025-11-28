from typing import Dict, Any, List, Tuple
import time, json, hashlib, os
from src.agents.base import AgentContext
from src.services.vector_store import VectorStore
from src.agents.institutional_data_agent import InstitutionalDataAgent
from src.agents.career_guidance_agent import CareerGuidanceAgent
from src.agents.financial_aid_agent import FinancialAidAgent
# Removed: AdmissionAdvisorAgent (deleted)
from src.models.profile import StudentProfile
from .genai_client import GenAIClient
from .prompt_loader import load_prompt



class Orchestrator:
    def __init__(self, config: Dict[str, Any], data_store: Dict[str, Any]):
        self.config = config
        self.data_store = data_store
        
        # Initialize GenAI client first
        env_model = os.getenv("MODEL_NAME") or os.getenv("LLM_MODEL")
        config_model = config.get("models", {}).get("llm", "gemini-1.5-flash")
        chosen_model = env_model if env_model else config_model
        if env_model and env_model != config_model:
            pass
        self.genai = GenAIClient(model=chosen_model)
        
        # Optional vector store
        vector_store = None
        if config.get("orchestrator", {}).get("use_vector_store", True):
            vector_store = VectorStore()
            programs = data_store.get("programs", [])
            if programs:
                vector_store.add_programs(programs)
        
        # Create context with genai_client
        self.context = AgentContext(config, data_store, vector_store=vector_store, genai_client=self.genai)
        self.agents = self._initialize_agents()
        
        self._cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self._cache_ttl = config.get("orchestrator", {}).get("cache_ttl_seconds", 120)
        self._export_dir = "exports"
        os.makedirs(self._export_dir, exist_ok=True)

    def _initialize_agents(self) -> List:
        # Only core 3 agents remain
        mapping = {
            "institutional_data": InstitutionalDataAgent,
            "career_guidance": CareerGuidanceAgent,
            "financial_aid": FinancialAidAgent,
        }
        enabled = self.config.get("agents", {}).get("enabled", [])
        agents = []
        for key in enabled:
            cls = mapping.get(key)
            if cls:
                agents.append(cls(self.context))
            else:
                pass
        return agents

    def _profile_key(self, profile: StudentProfile) -> str:
        raw = json.dumps(profile.model_dump(), sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def run(self, profile: StudentProfile) -> Dict[str, Any]:
        key = self._profile_key(profile)
        now = time.time()
        if key in self._cache:
            ts, cached = self._cache[key]
            if now - ts < self._cache_ttl:
                cached_copy = dict(cached)
                cached_copy["cached"] = True
                return cached_copy
        
        # Convert profile to dict for agents
        profile_dict = profile.model_dump()
        
        results: Dict[str, Any] = {"student": profile_dict, "agents": {}}
        
        # Step 1: OPTIONAL web search (for supplementary context only, not primary data)
        # Programs agent now uses curated database with semantic search + LLM reasoning
        web_search_results = None
        web_search_enabled = self.config.get("orchestrator", {}).get("enable_web_search", False)
        
        if web_search_enabled:
            pass
            for agent in self.agents:
                if agent.name == "web_search":
                    try:
                        web_search_results = agent.handle(profile_dict)
                        results["agents"]["web_search"] = web_search_results
                        
                        # Add as supplementary context (optional)
                        if web_search_results and web_search_results.get("search_results"):
                            profile_dict["web_search_context"] = web_search_results.get("llm_summary", "")
                    except Exception as e:
                        results["agents"]["web_search"] = {"error": str(e)}
                    break
        else:
            pass
        
        # Step 2: Run all agents (they use curated data + LLM reasoning, not web search parsing)
        for agent in self.agents:
            if agent.name == "web_search":
                continue  # Already handled above if enabled
            try:
                results["agents"][agent.name] = agent.handle(profile_dict)
            except Exception as e:
                results["agents"][agent.name] = {"error": str(e)}
        
        if self.config.get("orchestrator", {}).get("summarizer", False):
            summary = self._summarize(results)
            if summary:
                results["summary"] = summary
                self._export_summary(results)
        self._cache[key] = (now, results)
        return results

    def _summarize(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive LLM summary using structured prompt template."""
        # Extract student profile
        student = results.get("student", {})
        
        # Format agent results as JSON strings for the prompt
        agents_data = results.get("agents", {})
        
        try:
            prompt = load_prompt(
                "orchestrator_summary",
                student_name=student.get("name", "Student"),
                interests=", ".join(student.get("interests") or []),
                strengths=", ".join(student.get("strengths") or []),
                target_level=student.get("target_level", "Bachelor"),
                budget_category=student.get("budget_category", "Medium"),
                constraints=student.get("constraints") or "None specified",
                career_data=json.dumps(agents_data.get("career_guidance", {}), indent=2),
                program_data=json.dumps(agents_data.get("institutional_data", {}), indent=2),
                financial_data=json.dumps(agents_data.get("financial_aid", {}), indent=2),
                skill_data=json.dumps(agents_data.get("skill_gap", {}), indent=2),
                scholarship_data=json.dumps(agents_data.get("scholarship_matcher", {}), indent=2),
                interview_data=json.dumps(agents_data.get("interview_prep", {}), indent=2),
                learning_data=json.dumps(agents_data.get("learning_path", {}), indent=2),
            )
            
            pass
            summary = self.genai.summarize(prompt)
            
            if summary:
                pass
                return summary
            else:
                pass
                return "(LLM summary unavailable - fill in manually)"
            
        except FileNotFoundError:
            # Fallback to simple prompt if template not found
            pass
            fallback_prompt = (
                "Summarize guidance for the student based on: "
                f"{agents_data.get('career_guidance', {})} and programs "
                f"{agents_data.get('institutional_data', {})}. Focus on actionable next steps."
            )
            summary = self.genai.summarize(fallback_prompt)
            return summary or "(LLM summary unavailable - fill in manually)"
        except Exception:
            pass
            return "(LLM summary unavailable - fill in manually)"

    def _export_summary(self, results: Dict[str, Any]) -> None:
        if "summary" not in results:
            return
        ts = int(time.time())
        path = os.path.join(self._export_dir, f"summary_{ts}.md")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Counseling Summary\n\n{results['summary']}\n\n")
                f.write("## Key Program Suggestions\n")
                prog_section = results["agents"].get("institutional_data", {}).get("program_suggestions", [])
                for item in prog_section:
                    prog = item.get("program", {}) if isinstance(item, dict) else item
                    name = prog.get("program", "Unknown")
                    inst = prog.get("institution", "?")
                    score = item.get("score") if isinstance(item, dict) else None
                    f.write(f"- **{name}** ({inst})" + (f" score={score}" if score is not None else "") + "\n")
        except Exception:
            pass
