import json
import os
from typing import Dict, Any, List
from .base import BaseAgent



class InstitutionalDataAgent(BaseAgent):
    name = "institutional_data"
    description = "Uses AI reasoning with curated program database to provide intelligent, personalized program recommendations"

    def __init__(self, context):
        super().__init__(context)
        self.genai_client = context.genai_client  # Access to LLM for reasoning
        # Create our own vector store for curated programs (don't use orchestrator's)
        from src.services.vector_store import VectorStore
        self.vector_store = VectorStore()
        
        # Load curated programs on initialization
        self._load_curated_programs()

    def _load_curated_programs(self):
        """Load curated Singapore programs into vector store"""
        if len(self.vector_store._items) > 0:
            # Already loaded
            pass
            return
        
        try:
            programs_path = os.path.join(os.getcwd(), 'singapore_programs.json')
            pass
            
            if not os.path.exists(programs_path):
                pass
                pass
                pass
                return
            
            with open(programs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                programs_data = data['programs']
            
            pass
            
            # Convert to searchable format
            searchable_programs = []
            for prog in programs_data:
                searchable_text = f"""
                Program: {prog['program_name']}
                Institution: {prog['institution']}
                Level: {prog['level']}
                Field: {prog['field']}
                Description: {prog['description']}
                Topics: {', '.join(prog['key_topics'])}
                Career Outcomes: {prog['career_outcomes']}
                Unique Features: {prog['unique_features']}
                Singapore Context: {prog['singapore_context']}
                """.strip()
                
                searchable_programs.append({
                    'id': prog['id'],
                    'program': prog['program_name'],
                    'institution': prog['institution'],
                    'level': prog['level'],
                    'field': prog['field'],
                    'keywords': prog['key_topics'],
                    'searchable_text': searchable_text,
                    'full_data': prog
                })
            
            # Generate embeddings
            texts = [p['searchable_text'] for p in searchable_programs]
            pass
            
            try:
                embeddings = self.vector_store.embedding_client.embed(texts)
                self.vector_store._items = searchable_programs
                self.vector_store._embeddings = embeddings
                pass
            except Exception:
                pass
                pass
                self.vector_store._items = searchable_programs
                self.vector_store._embeddings = None
            
        except FileNotFoundError:
            pass
            pass
            pass
        except Exception:
            pass
            import traceback
            traceback.print_exc()

    def handle(self, profile: Any) -> Dict[str, Any]:
        """Main handler - uses vector search + LLM reasoning for recommendations"""
        interests = profile.get("interests", []) if isinstance(profile, dict) else (profile.interests or [])
        strengths = profile.get("strengths", []) if isinstance(profile, dict) else (profile.strengths or [])
        target_level = profile.get("target_level", "degree") if isinstance(profile, dict) else profile.target_level
        constraints = profile.get("constraints", []) if isinstance(profile, dict) else (profile.constraints or [])
        budget_category = profile.get("budget_category", "moderate") if isinstance(profile, dict) else "moderate"
        
        pass
        pass
        
        
        
        
        pass
        
        # Check if programs are loaded
        if not self.vector_store._items:
            pass
            return {
                "programs": [],
                "data_source": "error",
                "message": "Program database failed to load. Check logs for singapore_programs.json."
            }
        
        # Step 1: Semantic search to find relevant programs
        relevant_programs = self._semantic_search_programs(interests, strengths, target_level, constraints)
        
        if not relevant_programs:
            pass
            return {
                "programs": [],
                "data_source": "curated_database",
                "message": "No programs match the specified criteria"
            }
        
        pass
        
        # Step 2: Use LLM to REASON about fit and provide counselor-level insights
        recommendations = self._generate_ai_counselor_insights(
            relevant_programs, 
            interests, 
            strengths, 
            target_level,
            constraints,
            budget_category
        )
        
        return {
            "programs": recommendations[:5],  # UI expects "programs"
            "data_source": "ai_counselor_reasoning" if recommendations else "fallback_simple_ranking",
            "total_programs_analyzed": len(relevant_programs)
        }
    
    def _semantic_search_programs(
        self, 
        interests: List[str], 
        strengths: List[str], 
        target_level: str,
        constraints: List[str]
    ) -> List[Dict]:
        """Use vector search to find semantically relevant programs"""
        
        if not self.vector_store:
            pass
            return []
        
        # Build rich query that captures student profile
        query_parts = []
        if interests:
            query_parts.append(f"Student interested in: {', '.join(interests)}")
        if strengths:
            query_parts.append(f"Student strengths: {', '.join(strengths)}")
        if target_level:
            level_map = {"diploma": "polytechnic diploma", "degree": "bachelor degree", "postgrad": "master postgraduate"}
            query_parts.append(f"Looking for {level_map.get(target_level, target_level)} programs")
        if constraints:
            query_parts.append(f"Constraints: {', '.join(constraints[:3])}")  # Top 3 constraints
        
        search_query = " ".join(query_parts)
        
        pass
        
        # Search vector store
        results = self.vector_store.search(search_query, top_k=10)
        
        # Filter by level if specified
        filtered_results = []
        for result in results:
            prog_data = result['program']['full_data']
            
            # Level filtering
            prog_level = prog_data.get('level', 'degree')
            if target_level == "diploma" and prog_level != "diploma":
                continue
            if target_level == "degree" and prog_level == "diploma":
                continue  # Skip diplomas if looking for degrees
            
            filtered_results.append(result)
        
        pass
        
        return filtered_results[:8]  # Top 8 for LLM analysis
    
    def _generate_ai_counselor_insights(
        self,
        program_results: List[Dict],
        interests: List[str],
        strengths: List[str],
        target_level: str,
        constraints: List[str],
        budget_category: str
    ) -> List[Dict]:
        """
        Use LLM to reason like an education counselor.
        This is where REAL AI intelligence happens - understanding context, 
        reasoning about fit, providing insights.
        """
        
        if not self.genai_client:
            pass
            return self._fallback_simple_ranking(program_results)
        
        # Prepare comprehensive program data for LLM
        programs_for_analysis = []
        for result in program_results:
            prog_data = result['program']['full_data']
            programs_for_analysis.append({
                "program_name": prog_data['program_name'],
                "institution": prog_data['institution'],
                "field": prog_data['field'],
                "description": prog_data['description'],
                "key_topics": prog_data['key_topics'],
                "requirements": prog_data['requirements'],
                "tuition_fees": prog_data['tuition_fees'],
                "career_outcomes": prog_data['career_outcomes'],
                "unique_features": prog_data['unique_features'],
                "singapore_context": prog_data['singapore_context'],
                "url": prog_data['url'],
                "semantic_match_score": result['score']
            })
        
        # Build counselor-level reasoning prompt
        counselor_prompt = f"""You are an expert education counselor in Singapore with deep knowledge of the local education system, job market, and Smart Nation initiatives.

STUDENT PROFILE:
- Interests: {', '.join(interests)}
- Strengths: {', '.join(strengths)}
- Target Level: {target_level}
- Budget Category: {budget_category}
- Constraints: {', '.join(constraints) if constraints else 'None specified'}

AVAILABLE PROGRAMS (already pre-filtered by semantic relevance):
{json.dumps(programs_for_analysis, indent=2)}

YOUR TASK AS AN EDUCATION COUNSELOR:
Analyze each program and provide counselor-level insights. For each program, reason about:

1. **Fit Analysis**: How well does this program match the student's interests and strengths?
2. **Career Alignment**: Does this lead to careers the student would find fulfilling?
3. **Singapore Context**: How does this program position the student in Singapore's job market and Smart Nation goals?
4. **Financial Fit**: Consider the budget category and available tuition options
5. **Requirements Match**: Can this student reasonably meet the admission requirements given their profile?
6. **Unique Value**: What makes this program special for THIS PARTICULAR STUDENT?

Return a JSON array of recommendations, sorted by overall fit (best first):

[
  {{
    "program_name": "exact program name",
    "institution": "institution name",
    "fit_score": 0.0-1.0,
    "counselor_reasoning": "2-3 sentences explaining WHY this matches the student's unique situation. Be specific about their interests and strengths.",
    "career_insights": "What career paths this opens and why they align with student's goals",
    "singapore_advantage": "How this program positions student in Singapore's context",
    "financial_note": "Brief note about affordability based on budget category",
    "what_student_should_know": "Important information about requirements, challenges, or opportunities",
    "url": "program url"
  }}
]

BE SPECIFIC. Avoid generic statements like "this program is good". Instead: "Your strength in analytical thinking aligns perfectly with this program's emphasis on data-driven decision making, and your interest in AI finds direct application in..."

Consider Singapore-specific factors:
- Smart Nation AI/FinTech initiatives
- Local job market demand (tech sector, financial hub status)
- Government schemes (SkillsFuture, MOE grants)
- Regional MNC presence

Return ONLY valid JSON array, no explanations outside the JSON:"""

        try:
            pass
            
            response = self.genai_client.summarize(counselor_prompt)
            
            if not response:
                pass
                return self._fallback_simple_ranking(program_results)
            
            # Clean JSON response
            response = response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join([l for l in lines if not l.strip().startswith("```")])
            response = response.replace("```json", "").replace("```", "").strip()
            
            recommendations = json.loads(response)
            
            # Format for UI - flat structure
            formatted = []
            for rec in recommendations:
                # Find full program data
                full_prog = next((p for p in programs_for_analysis if p['program_name'] == rec['program_name']), None)
                
                formatted.append({
                    "title": rec['program_name'],
                    "institution": rec['institution'],
                    "level": target_level,
                    "duration": full_prog.get('duration', 'N/A') if full_prog else 'N/A',
                    "field": full_prog.get('field', '') if full_prog else '',
                    "fit_reasoning": rec['counselor_reasoning'],
                    "career_alignment": rec.get('career_insights', ''),
                    "singapore_context": rec.get('singapore_advantage', ''),
                    "financial_fit": rec.get('financial_note', ''),
                    "academic_requirements": full_prog.get('academic_requirements', '') if full_prog else '',
                    "tuition_fees": full_prog.get('tuition_fees', {}) if full_prog else {},
                    "career_outcomes": full_prog.get('career_outcomes', {}) if full_prog else {},
                    "reasoning_type": "ai_counselor_reasoning"
                })
            
            pass
            return formatted
            
        except json.JSONDecodeError:
            pass
            pass
            return self._fallback_simple_ranking(program_results)
        except Exception:
            pass
            return self._fallback_simple_ranking(program_results)
    
    def _fallback_simple_ranking(self, program_results: List[Dict]) -> List[Dict]:
        """Fallback if LLM reasoning fails - just return by semantic match score"""
        formatted = []
        for result in program_results[:5]:
            prog = result['program']
            prog_data = prog['full_data']
            formatted.append({
                "title": prog_data['program_name'],
                "institution": prog_data['institution'],
                "level": prog_data['level'],
                "duration": prog_data.get('duration', 'N/A'),
                "field": prog_data['field'],
                "fit_reasoning": f"Matched via semantic search (similarity: {result['score']:.0%})",
                "academic_requirements": prog_data.get('academic_requirements', ''),
                "tuition_fees": prog_data.get('tuition_fees', {}),
                "career_outcomes": prog_data.get('career_outcomes', {}),
                "reasoning_type": "fallback_simple_ranking"
            })
        return formatted
