from openai import OpenAI
from app.config import settings
from typing import Dict, List
import json

# Initialize the OpenAI client with the provided API key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class AIAnalyzer:
    @staticmethod
    def analyze_resume_content(resume_text: str, job_title: str = None, 
                               job_description: str = None) -> Dict:
        """Use AI to deeply analyze resume content"""
        
        # Prepare the context with resume, job title, and job description
        context = f"Resume Text:\n{resume_text}\n\n"
        if job_title:
            context += f"Target Job Title: {job_title}\n"
        if job_description:
            context += f"Job Description: {job_description}\n"
        
        prompt = f"""You are an expert resume reviewer and career coach. Analyze this resume and provide detailed feedback.

{context}

Provide your analysis in the following JSON format:
{{
    "strengths": ["list of 3-5 key strengths"],
    "improvement_suggestions": [
        {{
            "category": "Content/Formatting/Keywords/Impact",
            "priority": "High/Medium/Low",
            "issue": "specific issue found",
            "suggestion": "actionable suggestion",
            "example": "optional example of improvement"
        }}
    ],
    "missing_elements": ["list of missing important elements"],
    "overall_feedback": "2-3 sentences of overall assessment"
}}

Focus on:
1. Impact and quantifiable achievements
2. ATS-friendly keywords for the target role
3. Action verbs and strong language
4. Formatting and structure
5. Relevance to target position"""

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the response content and clean it up
            content = response.choices[0].message.content.strip()
            
            # Clean up any markdown if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Parse the cleaned response into JSON
            result = json.loads(content.strip())
            return result
        
        except json.JSONDecodeError as e:
            # Handle invalid JSON response and return a fallback structure
            return {
                "strengths": ["Resume submitted successfully"],
                "improvement_suggestions": [
                    {
                        "category": "General",
                        "priority": "Medium",
                        "issue": "Unable to parse detailed analysis",
                        "suggestion": "Please try again or contact support",
                        "example": None
                    }
                ],
                "missing_elements": [],
                "overall_feedback": "Analysis could not be completed. Please try again."
            }
        except Exception as e:
            # Raise a custom error if something else goes wrong
            raise Exception(f"AI analysis error: {str(e)}")

    @staticmethod
    def analyze_sections(resume_text: str) -> List[Dict]:
        """Analyze individual sections of the resume"""
        
        prompt = f"""Analyze this resume section by section. Identify each major section and provide specific feedback.

Resume:
{resume_text}

Return JSON array with this format:
[
    {{
        "section_name": "Section name (e.g., Experience, Education)",
        "content": "Brief summary of what's in this section",
        "issues": ["list of issues in this section"],
        "suggestions": ["list of improvements for this section"]
    }}
]

Analyze sections like: Professional Summary, Experience, Education, Skills, etc."""

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert resume reviewer. Always respond with valid JSON array."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Extract and clean the response content
            content = response.choices[0].message.content.strip()
            
            # Clean up any markdown code blocks
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Parse and return the response
            result = json.loads(content.strip())
            return result
        
        except Exception as e:
            # Return a fallback response in case of an error
            return [
                {
                    "section_name": "General",
                    "content": "Resume content detected",
                    "issues": ["Detailed section analysis unavailable"],
                    "suggestions": ["Ensure clear section headers", "Use consistent formatting"]
                }
            ]
    
    @staticmethod
    def get_keyword_suggestions(resume_text: str, job_title: str, 
                               job_description: str = None) -> List[str]:
        """Get AI-suggested keywords to add"""
        
        # Create context based on the resume and job details
        context = f"Job Title: {job_title}\n"
        if job_description:
            context += f"Job Description: {job_description}\n"
        context += f"\nCurrent Resume:\n{resume_text}"
        
        prompt = f"""Based on this job title and description, suggest 5-8 important keywords/skills that are missing from the resume but would be valuable to include.

{context}

Return ONLY a JSON array of strings: ["keyword1", "keyword2", ...]
Focus on technical skills, industry terms, and relevant qualifications."""

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a keyword optimization expert. Respond only with JSON array."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            # Extract and clean the response content
            content = response.choices[0].message.content.strip()
            
            # Clean up any markdown
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Parse and return the keywords
            keywords = json.loads(content.strip())
            return keywords
        
        except Exception as e:
            # Return a fallback response in case of an error
            return ["Unable to generate keyword suggestions"]
