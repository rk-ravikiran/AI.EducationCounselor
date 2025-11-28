import json
import logging
from typing import Dict, Any, List
from .base import BaseAgent

logger = logging.getLogger(__name__)

class CareerGuidanceAgent(BaseAgent):
    name = "career_guidance"
    description = "Uses AI reasoning to provide personalized career guidance based on student profile and Singapore's job market"

    def __init__(self, context):
        super().__init__(context)
        self.genai_client = context.genai_client

    def handle(self, profile: Any) -> Dict[str, Any]:
        """Provide intelligent career guidance using LLM reasoning"""
        
        interests = profile.get("interests", []) if isinstance(profile, dict) else (profile.interests or [])
        strengths = profile.get("strengths", []) if isinstance(profile, dict) else (profile.strengths or [])
        target_level = profile.get("target_level", "degree") if isinstance(profile, dict) else profile.target_level
        constraints = profile.get("constraints", []) if isinstance(profile, dict) else (profile.constraints or [])
        
        # Get programs they're considering (if institutional_data ran before)
        program_suggestions = profile.get("program_suggestions", [])
        
        pass", interests, strengths)
        
        if not interests:
            return {
                "career_suggestions": [],
                "message": "No interests provided for career guidance"
            }
        
        # Use LLM to reason about career paths
        career_paths = self._generate_career_insights(
            interests, 
            strengths, 
            target_level,
            constraints,
            program_suggestions
        )
        
        return {
            "career_suggestions": career_paths[:5],
            "data_source": "ai_career_counseling",
            "reasoning_quality": "contextual_understanding"
        }
    
    def _generate_career_insights(
        self,
        interests: List[str],
        strengths: List[str],
        target_level: str,
        constraints: List[str],
        program_suggestions: List[Dict]
    ) -> List[Dict]:
        """Use LLM to provide career counselor-level insights"""
        
        if not self.genai_client:
            pass
            return self._fallback_career_suggestions(interests)
        
        # Build context about programs if available
        programs_context = ""
        if program_suggestions:
            programs_list = [p.get("program", {}).get("program", "") for p in program_suggestions[:3]]
            programs_context = f"\nStudent is considering these programs: {', '.join(programs_list)}"
        
        career_prompt = f"""You are an expert career counselor specializing in Singapore's job market and education pathways.

STUDENT PROFILE:
- Interests: {', '.join(interests)}
- Strengths: {', '.join(strengths)}
- Education Level: {target_level}
- Constraints: {', '.join(constraints) if constraints else 'None'}
{programs_context}

YOUR TASK AS A CAREER COUNSELOR:
Analyze this student's profile and suggest 5 career paths that:
1. Align with their interests and strengths
2. Are realistic given their education level
3. Consider Singapore's job market (demand, growth, opportunities)
4. Leverage Singapore's Smart Nation, FinTech hub, and tech sector strengths

For each career path, provide:
- **Career Title**: Specific job role (e.g., "AI Engineer" not just "Tech")
- **Why It Fits**: 2-3 sentences explaining how their interests and strengths align
- **Singapore Demand**: Current job market reality (high/medium demand, growing/stable)
- **Typical Path**: How they get there (what degree → entry role → senior role)
- **Salary Expectations**: Realistic Singapore salary ranges (starting → 5 years experience)
- **Key Skills Needed**: 3-4 specific skills they should develop
- **Companies/Sectors**: Where they'd work (specific Singapore companies, sectors, or government agencies)

SINGAPORE CONTEXT TO CONSIDER:
- Smart Nation initiatives (AI, data, digital transformation)
- Financial hub status (banking, insurance, FinTech)
- Regional MNC headquarters (Google, Meta, Microsoft, JP Morgan)
- Tech unicorns (Grab, Sea Group, Shopee)
- Government agencies (GovTech, MAS, DSTA, A*STAR)
- Startups ecosystem
- Healthcare, logistics, education sectors undergoing digital transformation

IMPORTANT:
- Be SPECIFIC. Don't say "good career prospects" - say "High demand: 500+ job openings monthly on LinkedIn for Data Scientists in Singapore"
- Mention ACTUAL companies/agencies where possible
- Give REALISTIC salary ranges (Singapore context: fresh grad vs 5 years)
- Explain WHY their strengths matter for each career

Return ONLY valid JSON array:
[
  {{
    "title": "Specific Job Title",
    "fit_reasoning": "Why this career matches their interests and strengths specifically",
    "singapore_demand": "High/Medium demand explanation with context",
    "career_path": "Degree → Entry role → Mid-level → Senior progression",
    "salary_range": {{
      "starting": "S$X,XXX - S$X,XXX/month",
      "five_years": "S$X,XXX - S$X,XXX/month"
    }},
    "key_skills": ["skill1", "skill2", "skill3", "skill4"],
    "where_to_work": "Specific companies/sectors in Singapore",
    "growth_potential": "Career advancement opportunities and trends"
  }}
]

JSON only, no explanations outside JSON:"""

        try:
            pass
            
            response = self.genai_client.summarize(career_prompt)
            
            if not response:
                pass
                return self._fallback_career_suggestions(interests)
            
            # Clean JSON response
            response = response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join([l for l in lines if not l.strip().startswith("```")])
            response = response.replace("```json", "").replace("```", "").strip()
            
            career_paths = json.loads(response)
            
            # Format for UI
            formatted = []
            for career in career_paths:
                formatted.append({
                    "title": career["title"],
                    "description": career["fit_reasoning"],
                    "required_skills": career.get("key_skills", []),
                    "outlook": {
                        "demand": career.get("singapore_demand", ""),
                        "salary_range": f"{career.get('salary_range', {}).get('starting', '')} (starting) → {career.get('salary_range', {}).get('five_years', '')} (5 years)",
                        "where_to_work": career.get("where_to_work", ""),
                        "growth_potential": career.get("growth_potential", "")
                    },
                    "career_path": career.get("career_path", ""),
                    "reasoning_type": "ai_career_counseling"
                })
            
            pass)
            return formatted
            
        except json.JSONDecodeError:
            pass
            pass
            return self._fallback_career_suggestions(interests)
        except Exception:
            pass
            return self._fallback_career_suggestions(interests)
    
    def _fallback_career_suggestions(self, interests: List[str]) -> List[Dict]:
        """Simple fallback if LLM fails"""
        
        # Basic mapping
        career_map = {
            "artificial intelligence": {
                "title": "AI Engineer / Machine Learning Specialist",
                "salary": "S$5,000 - S$7,000/month (starting)",
                "skills": ["Python", "Machine Learning", "Deep Learning", "Data Analysis"]
            },
            "data science": {
                "title": "Data Scientist",
                "salary": "S$4,500 - S$6,500/month (starting)",
                "skills": ["Python", "Statistics", "SQL", "Data Visualization"]
            },
            "finance": {
                "title": "Financial Analyst / FinTech Specialist",
                "salary": "S$4,000 - S$6,000/month (starting)",
                "skills": ["Financial Modeling", "Excel", "SQL", "Business Analysis"]
            },
            "business": {
                "title": "Business Analyst / Consultant",
                "salary": "S$3,800 - S$5,500/month (starting)",
                "skills": ["Business Analysis", "Project Management", "Stakeholder Management", "Data Analysis"]
            },
            "engineering": {
                "title": "Software Engineer / Engineer",
                "salary": "S$4,000 - S$6,000/month (starting)",
                "skills": ["Programming", "System Design", "Problem Solving", "Technical Skills"]
            }
        }
        
        suggestions = []
        for interest in interests[:3]:
            interest_lower = interest.lower()
            
            # Find matching career
            match = None
            for key, value in career_map.items():
                if key in interest_lower:
                    match = value
                    break
            
            if not match:
                match = {
                    "title": f"{interest} Professional",
                    "salary": "S$3,500 - S$5,000/month (starting)",
                    "skills": ["Critical Thinking", "Communication", "Problem Solving", "Technical Skills"]
                }
            
            suggestions.append({
                "title": match["title"],
                "description": f"Career path related to {interest} (fallback - basic suggestion)",
                "required_skills": match["skills"],
                "outlook": {
                    "demand": "Refer to Singapore job market data",
                    "salary_range": match["salary"]
                },
                "reasoning_type": "fallback_basic"
            })
        
        return suggestions
