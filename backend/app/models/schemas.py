from pydantic import BaseModel
from typing import List, Optional

class ResumeSection(BaseModel):
    section_name: str
    content: str
    issues: List[str]
    suggestions: List[str]

class ATSScore(BaseModel):
    overall_score: int  # 0-100
    keyword_score: int
    formatting_score: int
    content_score: int
    details: str

class ImprovementSuggestion(BaseModel):
    category: str
    priority: str  # High, Medium, Low
    issue: str
    suggestion: str
    example: Optional[str] = None

class ResumeAnalysis(BaseModel):
    ats_score: ATSScore
    sections_analysis: List[ResumeSection]
    improvement_suggestions: List[ImprovementSuggestion]
    strengths: List[str]
    missing_elements: List[str]
    overall_feedback: str

class AnalyzeRequest(BaseModel):
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    target_industry: Optional[str] = None