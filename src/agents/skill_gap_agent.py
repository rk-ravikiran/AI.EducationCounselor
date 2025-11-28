from typing import Any, Dict, List
from .base import BaseAgent

_SKILL_MATRIX = {
    "AI": {
        "required_skills": ["Python", "Statistics", "Machine Learning", "Data Handling"],
        "resources": {
            "Python": ["https://docs.python.org", "https://realpython.com/", "https://www.skillsfuture.gov.sg/"],
            "Statistics": ["https://www.khanacademy.org/math/statistics-probability"],
            "Machine Learning": ["https://coursera.org/machine-learning", "https://fast.ai"],
            "Data Handling": ["https://pandas.pydata.org/docs/"],
        },
        "local_notes": "Consider NTU and NUS AI focus tracks; leverage SkillsFuture credits for foundational courses.",
    },
    "Finance": {
        "required_skills": ["Accounting Basics", "Financial Modeling", "Excel", "Data Analysis"],
        "resources": {
            "Accounting Basics": ["https://www.investopedia.com/accounting"],
            "Financial Modeling": ["https://corporatefinanceinstitute.com/"],
            "Excel": ["https://exceljet.net"],
            "Data Analysis": ["https://mode.com/sql-tutorial"],
        },
        "local_notes": "NUS and SMU offer strong finance & FinTech modules; explore MAS FinTech sandbox insights.",
    },
    "Robotics": {
        "required_skills": ["Python", "Embedded Systems", "Control Theory", "Electronics"],
        "resources": {
            "Embedded Systems": ["https://embedded.fm/", "https://docs.arduino.cc"],
            "Control Theory": ["https://www.khanacademy.org/science/physics"],
            "Electronics": ["https://learn.sparkfun.com/tutorials"],
        },
        "local_notes": "SIT and polytechnics (RP, SP) have hands-on robotics labs; look for industry internship tie-ups.",
    },
}

class SkillGapAgent(BaseAgent):
    name = "skill_gap"
    description = "Identifies missing skills from real program requirements and suggests resources"

    def handle(self, profile: Any) -> Dict[str, Any]:
        interests: List[str] = profile.get("interests", []) if isinstance(profile, dict) else (profile.interests or [])
        strengths = profile.get("strengths", []) if isinstance(profile, dict) else (profile.strengths or [])
        web_search_data = profile.get("web_search_data", []) if isinstance(profile, dict) else []
        strengths_lower = {s.lower() for s in strengths}
        
        gaps: List[Dict[str, Any]] = []
        current_skills = list(strengths)
        
        # Extract skill requirements from web search results
        if web_search_data:
            pass} web search results for skill requirements")
            all_required_skills = set()
            
            for result in web_search_data[:5]:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                text = (title + " " + snippet).lower()
                
                # Extract skills from program descriptions
                skills = self._extract_skills_from_text(text)
                all_required_skills.update(skills)
            
            # Identify gaps
            for skill in all_required_skills:
                if skill.lower() not in strengths_lower:
                    gap = {
                        "skill": skill.capitalize(),
                        "importance": "High" if any(i.lower() in skill.lower() for i in interests) else "Medium",
                        "resources": self._get_resources_for_skill(skill),
                        "local_note": "Available through SkillsFuture courses in Singapore",
                        "source": "extracted from program requirements"
                    }
                    gaps.append(gap)
        
        # If no web results, use interest-based defaults
        if len(gaps) < 3:
            for interest in interests:
                default_skills = self._get_default_skills_for_interest(interest)
                for skill in default_skills:
                    if skill.lower() not in strengths_lower and not any(g["skill"].lower() == skill.lower() for g in gaps):
                        gaps.append({
                            "skill": skill,
                            "importance": "High",
                            "resources": self._get_resources_for_skill(skill),
                            "local_note": "Fundamental skill for this field",
                            "source": "domain knowledge"
                        })
        
        return {
            "skill_gaps": gaps[:5],  # Top 5 gaps
            "current_skills": current_skills,
            "data_source": "real-time web search" if web_search_data else "static database"
        }
    
    def _extract_skills_from_text(self, text: str) -> set:
        """Extract skill keywords from program text"""
        skills = set()
        
        # Common skill keywords to look for
        skill_keywords = [
            "python", "java", "javascript", "c++", "programming",
            "statistics", "mathematics", "calculus", "linear algebra",
            "machine learning", "data science", "ai", "deep learning",
            "communication", "teamwork", "leadership",
            "excel", "sql", "database",
            "financial modeling", "accounting", "finance",
            "design thinking", "problem solving", "critical thinking",
            "research", "analysis", "analytical"
        ]
        
        for keyword in skill_keywords:
            if keyword in text:
                skills.add(keyword)
        
        return skills
    
    def _get_resources_for_skill(self, skill: str) -> List[str]:
        """Get learning resources for a skill"""
        skill_lower = skill.lower()
        
        resource_map = {
            "python": ["Python.org", "Real Python", "SkillsFuture Python courses"],
            "java": ["Oracle Java Tutorials", "Java Programming at Coursera"],
            "statistics": ["Khan Academy Statistics", "Statistics courses on edX"],
            "machine learning": ["Coursera ML", "Fast.ai", "NUS AI courses"],
            "data science": ["DataCamp", "Kaggle", "SkillsFuture Data Analytics"],
            "excel": ["Excel Jet", "Microsoft Learn"],
            "sql": ["SQLZoo", "Mode Analytics SQL Tutorial"],
            "communication": ["Toastmasters Singapore", "Communication workshops"],
            "leadership": ["SMU Leadership programs", "MOE Leadership courses"]
        }
        
        # Check for skill match
        for key in resource_map:
            if key in skill_lower:
                return resource_map[key]
        
        return ["SkillsFuture courses", "Online learning platforms", "University workshops"]
    
    def _get_default_skills_for_interest(self, interest: str) -> List[str]:
        """Get default required skills for an interest"""
        interest_lower = interest.lower()
        
        if any(keyword in interest_lower for keyword in ["ai", "artificial", "machine", "data"]):
            return ["Python", "Statistics", "Machine Learning", "Data Analysis"]
        elif any(keyword in interest_lower for keyword in ["finance", "business", "economics"]):
            return ["Excel", "Financial Modeling", "Data Analysis", "Accounting Basics"]
        elif any(keyword in interest_lower for keyword in ["engineering", "robotics"]):
            return ["Mathematics", "Programming", "Problem Solving"]
        else:
            return ["Critical Thinking", "Communication", "Research Methods"]
