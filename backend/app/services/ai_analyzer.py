from __future__ import annotations

import json
from typing import Dict, List, Optional, Any

from openai import OpenAI

# ✅ FIX: correct import path inside backend/app/services
# Your config.py is in backend/app/config.py
from ..config import settings


class AIAnalyzer:
    """
    Centralized AI analysis utility for resume review and ATS keyword suggestions.

    Notes:
    - Uses OpenAI SDK v1.x (you installed openai==1.3.0)
    - Expects settings to provide:
        - OPENAI_API_KEY
        - OPENAI_MODEL
    """

    def __init__(self) -> None:
        # Create client once per instance (better than module-global in many cases)
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def _strip_code_fences(text: str) -> str:
        """Remove ```json / ``` wrappers if model returns code fenced output."""
        t = text.strip()
        if t.startswith("```json"):
            t = t[7:].strip()
        if t.startswith("```"):
            t = t[3:].strip()
        if t.endswith("```"):
            t = t[:-3].strip()
        return t

    @staticmethod
    def _safe_json_loads(text: str) -> Any:
        """
        Parse JSON safely with cleanup.
        Raises json.JSONDecodeError if parsing fails.
        """
        cleaned = AIAnalyzer._strip_code_fences(text)
        return json.loads(cleaned)

    def _chat_json(self, prompt: str, *, max_tokens: int = 1500, temperature: float = 0.7) -> str:
        """
        Call OpenAI and return raw content string.
        Keeps one place for request settings.
        """
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON. No markdown, no explanations."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (response.choices[0].message.content or "").strip()

    def analyze_resume_content(
        self,
        resume_text: str,
        job_title: Optional[str] = None,
        job_description: Optional[str] = None,
    ) -> Dict:
        """
        Use AI to deeply analyze resume content.
        Returns a dict matching the schema described in the prompt.
        """

        context_parts = [f"Resume Text:\n{resume_text}\n"]
        if job_title:
            context_parts.append(f"Target Job Title: {job_title}\n")
        if job_description:
            context_parts.append(f"Job Description: {job_description}\n")

        context = "\n".join(context_parts)

        prompt = f"""
You are an expert resume reviewer and career coach. Analyze this resume and provide detailed feedback.

{context}

Return JSON in this exact format:
{{
  "strengths": ["3-5 key strengths"],
  "improvement_suggestions": [
    {{
      "category": "Content/Formatting/Keywords/Impact",
      "priority": "High/Medium/Low",
      "issue": "specific issue found",
      "suggestion": "actionable suggestion",
      "example": "optional example of improvement"
    }}
  ],
  "missing_elements": ["missing important elements"],
  "overall_feedback": "2-3 sentences overall assessment"
}}

Focus on:
1) Impact and quantifiable achievements
2) ATS-friendly keywords for the target role
3) Action verbs and strong language
4) Formatting and structure
5) Relevance to target position
""".strip()

        try:
            raw = self._chat_json(prompt, max_tokens=2000, temperature=0.7)
            result = self._safe_json_loads(raw)

            # Defensive: ensure it's a dict
            if not isinstance(result, dict):
                raise ValueError("AI returned JSON but not an object/dict.")

            return result

        except json.JSONDecodeError:
            return {
                "strengths": ["Resume received"],
                "improvement_suggestions": [
                    {
                        "category": "General",
                        "priority": "Medium",
                        "issue": "AI response was not valid JSON",
                        "suggestion": "Try again (shorter resume text) or check model settings",
                        "example": None,
                    }
                ],
                "missing_elements": [],
                "overall_feedback": "Analysis could not be completed due to formatting issues. Please try again.",
            }
        except Exception as e:
            raise Exception(f"AI analysis error: {str(e)}") from e

    def analyze_sections(self, resume_text: str) -> List[Dict]:
        """
        Analyze resume section by section.
        Returns list[dict].
        """

        prompt = f"""
Analyze this resume section by section. Identify each major section and provide specific feedback.

Resume:
{resume_text}

Return ONLY a JSON array in this format:
[
  {{
    "section_name": "Section name (e.g., Experience, Education)",
    "content": "Brief summary of what's in this section",
    "issues": ["issues in this section"],
    "suggestions": ["improvements for this section"]
  }}
]
""".strip()

        try:
            raw = self._chat_json(prompt, max_tokens=1500, temperature=0.7)
            result = self._safe_json_loads(raw)

            if not isinstance(result, list):
                raise ValueError("AI returned JSON but not an array/list.")

            return result

        except Exception:
            return [
                {
                    "section_name": "General",
                    "content": "Resume content detected",
                    "issues": ["Detailed section analysis unavailable"],
                    "suggestions": ["Ensure clear section headers", "Use consistent formatting"],
                }
            ]

    def get_keyword_suggestions(
        self,
        resume_text: str,
        job_title: str,
        job_description: Optional[str] = None,
    ) -> List[str]:
        """
        Get AI suggested missing keywords to add.
        Returns list[str].
        """

        context_parts = [f"Job Title: {job_title}"]
        if job_description:
            context_parts.append(f"Job Description: {job_description}")
        context_parts.append(f"Current Resume:\n{resume_text}")

        context = "\n\n".join(context_parts)

        prompt = f"""
Based on the job title/description, suggest 5-8 important keywords/skills that are missing from the resume but should be included.

{context}

Return ONLY a JSON array of strings like:
["keyword1", "keyword2", "keyword3"]
""".strip()

        try:
            raw = self._chat_json(prompt, max_tokens=300, temperature=0.4)
            result = self._safe_json_loads(raw)

            if not isinstance(result, list):
                raise ValueError("AI returned JSON but not an array/list.")

            # Ensure list[str]
            keywords: List[str] = []
            for item in result:
                if isinstance(item, str):
                    keywords.append(item.strip())
            return keywords if keywords else ["No keywords returned"]

        except Exception:
            return ["Unable to generate keyword suggestions"]
