from pydantic import BaseModel, Field
from typing import List, Optional

class StudentProfile(BaseModel):
    name: str = Field(..., description="Student name")
    interests: List[str] = Field(default_factory=list, description="Academic or career interests")
    strengths: List[str] = Field(default_factory=list, description="Academic strengths or subjects")
    constraints: List[str] = Field(default_factory=list, description="Constraints like budget, location, scores")
    target_level: Optional[str] = Field(None, description="Education level target e.g., diploma, bachelor")
    budget_category: Optional[str] = Field(None, description="low|medium|high budget band")
