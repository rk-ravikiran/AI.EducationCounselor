import json
import logging
import os
from typing import Dict, Any, List
from .base import BaseAgent

logger = logging.getLogger(__name__)
class FinancialAidAgent(BaseAgent):
    name = "financial_aid"
    description = "Uses AI reasoning with curated financial aid database to provide personalized scholarship and funding recommendations"

    def __init__(self, context):
        super().__init__(context)
        self.genai_client = context.genai_client
        self.vector_store = None  # Could use vector store, but simpler to filter directly
        self._load_financial_aid_data()

    def _load_financial_aid_data(self):
        """Load curated financial aid options"""
        try:
            aid_path = os.path.join(os.getcwd(), 'singapore_financial_aid.json')
            with open(aid_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.aid_options = data['financial_aid_options']
            pass)
        except Exception:
            pass
            self.aid_options = []

    def handle(self, profile: Any) -> Dict[str, Any]:
        """Provide intelligent financial aid recommendations using LLM reasoning"""
        
        budget_category = profile.get("budget_category", "moderate") if isinstance(profile, dict) else profile.budget_category
        interests = profile.get("interests", []) if isinstance(profile, dict) else (profile.interests or [])
        target_level = profile.get("target_level", "degree") if isinstance(profile, dict) else profile.target_level
        constraints = profile.get("constraints", []) if isinstance(profile, dict) else (profile.constraints or [])
        
        # Extract citizenship if available from constraints/profile
        citizenship = self._extract_citizenship(constraints, profile)
        
        pass",
            budget_category,
            citizenship,
            target_level,
        )
        
        if not self.aid_options:
            return {
                "aid_options": [],
                "message": "Financial aid database not available"
            }
        
        # Filter aid options by eligibility
        eligible_options = self._filter_by_eligibility(citizenship, target_level, budget_category)
        
        if not eligible_options:
            return {
                "aid_options": [],
                "message": "No matching financial aid options found for your profile"
            }
        
        pass)
        
        # Use LLM to reason about which options best fit the student
        recommendations = self._generate_aid_recommendations(
            eligible_options,
            budget_category,
            citizenship,
            target_level,
            interests,
            constraints
        )
        
        return {
            "aid_options": recommendations[:6],  # Top 6 recommendations
            "data_source": "ai_financial_counseling",
            "total_eligible": len(eligible_options)
        }
    
    def _extract_citizenship(self, constraints: List[str], profile: Dict) -> str:
        """Extract citizenship status from profile"""
        # Check if citizenship mentioned in constraints
        for constraint in constraints:
            constraint_lower = constraint.lower()
            if "citizen" in constraint_lower:
                return "Singapore Citizen"
            elif "pr" in constraint_lower or "permanent resident" in constraint_lower:
                return "Permanent Resident"
            elif "international" in constraint_lower:
                return "International"
        
        # Default assumption for Singapore education system
        return "Singapore Citizen"
    
    def _filter_by_eligibility(
        self, 
        citizenship: str, 
        target_level: str,
        budget_category: str
    ) -> List[Dict]:
        """Filter aid options by basic eligibility criteria"""
        
        eligible = []
        
        for aid in self.aid_options:
            eligibility = aid.get("eligibility", {})
            
            # Check citizenship
            allowed_citizenship = eligibility.get("citizenship", [])
            if citizenship not in allowed_citizenship and "any" not in [c.lower() for c in allowed_citizenship]:
                continue
            
            # Check level
            allowed_levels = eligibility.get("level", [])
            if target_level not in allowed_levels and "any" not in allowed_levels:
                continue
            
            eligible.append(aid)
        
        return eligible
    
    def _generate_aid_recommendations(
        self,
        eligible_options: List[Dict],
        budget_category: str,
        citizenship: str,
        target_level: str,
        interests: List[str],
        constraints: List[str]
    ) -> List[Dict]:
        """Use LLM to provide counselor-level insights about financial aid"""
        
        if not self.genai_client:
            pass
            return self._fallback_ranking(eligible_options, budget_category)
        
        # Prepare aid options for LLM
        aid_summaries = []
        for aid in eligible_options:
            aid_summaries.append({
                "name": aid["name"],
                "type": aid["type"],
                "category": aid["category"],
                "amount": aid["amount"],
                "description": aid["description"],
                "application_process": aid.get("application_process", ""),
                "bond_requirement": aid.get("bond_requirement", "None"),
                "singapore_context": aid.get("singapore_context", "")
            })
        
        aid_prompt = f"""You are an expert financial aid counselor in Singapore, helping students understand and access education funding.

STUDENT PROFILE:
- Budget Category: {budget_category}
- Citizenship: {citizenship}
- Education Level: {target_level}
- Interests: {', '.join(interests)}
- Constraints: {', '.join(constraints) if constraints else 'None'}

AVAILABLE FINANCIAL AID OPTIONS:
{json.dumps(aid_summaries, indent=2)}

YOUR TASK AS A FINANCIAL AID COUNSELOR:
Analyze these financial aid options and recommend the best ones for this student. For each recommendation:

1. **Priority Ranking**: Which should they apply for FIRST (highest impact, easiest to get)
2. **Why It Fits**: Explain why this aid option matches their situation
3. **Expected Benefit**: How much money this saves them (be specific)
4. **Application Strategy**: Practical advice on applying
5. **Combination Strategy**: Can they stack this with other aid?

IMPORTANT CONSIDERATIONS:
- Budget category indicates financial need level
- Some aid can be combined (e.g., MOE Bursary + University Bursary)
- Some aid is automatic (like MOE Tuition Grant for citizens)
- Some require extensive applications (scholarships)
- Bond requirements matter for career planning
- Loans should be last resort, mention alternatives first

PRIORITIZATION RULES:
1. Free money (grants/bursaries) > Loans
2. Automatic/easy to get > Complex applications
3. No bond > Bond requirements
4. Higher amounts > Lower amounts (when effort is similar)
5. Need-based for tight budget, merit-based for others

Return ONLY valid JSON array, sorted by priority (most important first):
[
  {{
    "name": "Aid option name",
    "priority": "High/Medium/Low",
    "fit_reasoning": "Why this matches their situation specifically",
    "expected_benefit": "Specific amount saved or received (S$X,XXX)",
    "application_difficulty": "Easy/Moderate/Challenging",
    "application_advice": "Practical steps to apply successfully",
    "combination_strategy": "Can stack with [other aid names] for total of S$X,XXX",
    "important_notes": "Any critical information (deadlines, bond, requirements)"
  }}
]

JSON only, no explanations outside JSON:"""

        try:
            pass
            
            response = self.genai_client.summarize(aid_prompt)
            
            if not response:
                pass
                return self._fallback_ranking(eligible_options, budget_category)
            
            # Clean JSON response
            response = response.strip()
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join([l for l in lines if not l.strip().startswith("```")])
            response = response.replace("```json", "").replace("```", "").strip()
            
            recommendations = json.loads(response)
            
            # Enrich with full aid data
            formatted = []
            for rec in recommendations:
                # Find the full aid data
                full_aid = next((a for a in eligible_options if a["name"] == rec["name"]), None)
                if not full_aid:
                    continue
                
                formatted.append({
                    "name": rec["name"],
                    "type": full_aid["type"],
                    "amount": full_aid["amount"],
                    "priority": rec.get("priority", "Medium"),
                    "fit_reasoning": rec.get("fit_reasoning", ""),
                    "expected_benefit": rec.get("expected_benefit", ""),
                    "application_difficulty": rec.get("application_difficulty", ""),
                    "application_process": full_aid.get("application_process", ""),
                    "application_advice": rec.get("application_advice", ""),
                    "combination_strategy": rec.get("combination_strategy", ""),
                    "important_notes": rec.get("important_notes", ""),
                    "website": full_aid.get("website", ""),
                    "bond_requirement": full_aid.get("bond_requirement", "None"),
                    "reasoning_type": "ai_financial_counseling"
                })
            
            pass)
            return formatted
            
        except json.JSONDecodeError:
            pass
            pass
            return self._fallback_ranking(eligible_options, budget_category)
        except Exception:
            pass
            return self._fallback_ranking(eligible_options, budget_category)
    
    def _fallback_ranking(self, eligible_options: List[Dict], budget_category: str) -> List[Dict]:
        """Simple ranking if LLM fails"""
        
        # Prioritize by category and budget fit
        prioritized = []
        
        for aid in eligible_options:
            priority_score = 0
            
            # Need-based aid for tight budget
            if budget_category in ["tight", "low"] and aid["category"] == "need-based":
                priority_score += 3
            
            # Universal aid for everyone
            if aid["category"] == "universal":
                priority_score += 2
            
            # Government schemes over community (broader access)
            if "government" in aid["type"].lower():
                priority_score += 2
            
            # No bond is better
            if aid.get("bond_requirement", "None") == "None":
                priority_score += 1
            
            prioritized.append({
                "name": aid["name"],
                "type": aid["type"],
                "amount": aid["amount"],
                "eligibility": aid.get("description", ""),
                "application_process": aid.get("application_process", ""),
                "bond_requirement": aid.get("bond_requirement", "None"),
                "website": aid.get("website", ""),
                "_priority_score": priority_score,
                "reasoning_type": "fallback_simple_ranking"
            })
        
        # Sort by priority score
        prioritized.sort(key=lambda x: x["_priority_score"], reverse=True)
        
        # Remove score from output
        for item in prioritized:
            del item["_priority_score"]
        
        return prioritized
