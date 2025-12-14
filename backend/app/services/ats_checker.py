import re
from typing import List, Dict

class ATSChecker:
    # Common ATS-friendly section headers
    STANDARD_SECTIONS = [
        "experience", "work experience", "professional experience",
        "education", "skills", "technical skills",
        "summary", "professional summary", "objective",
        "certifications", "projects", "achievements"
    ]
    
    # Common action verbs for strong bullet points
    ACTION_VERBS = [
        "achieved", "improved", "increased", "decreased", "developed",
        "led", "managed", "created", "implemented", "designed",
        "optimized", "streamlined", "coordinated", "executed"
    ]
    
    @staticmethod
    def calculate_ats_score(resume_text: str, formatting_issues: List[str], 
                           job_description: str = None) -> Dict:
        """Calculate comprehensive ATS score"""
        
        # Keyword Score (40%)
        keyword_score = ATSChecker._calculate_keyword_score(resume_text, job_description)
        
        # Formatting Score (30%)
        formatting_score = ATSChecker._calculate_formatting_score(resume_text, formatting_issues)
        
        # Content Score (30%)
        content_score = ATSChecker._calculate_content_score(resume_text)
        
        # Overall weighted score
        overall_score = int(
            (keyword_score * 0.4) + 
            (formatting_score * 0.3) + 
            (content_score * 0.3)
        )
        
        return {
            "overall_score": overall_score,
            "keyword_score": keyword_score,
            "formatting_score": formatting_score,
            "content_score": content_score,
            "details": ATSChecker._get_score_details(overall_score)
        }
    
    @staticmethod
    def _calculate_keyword_score(resume_text: str, job_description: str = None) -> int:
        """Calculate keyword optimization score"""
        score = 50  # Base score
        
        resume_lower = resume_text.lower()
        
        # Check for action verbs
        action_verb_count = sum(1 for verb in ATSChecker.ACTION_VERBS if verb in resume_lower)
        score += min(action_verb_count * 2, 20)
        
        # Check for quantifiable achievements
        numbers = re.findall(r'\d+%|\$\d+|[\d,]+\+', resume_text)
        score += min(len(numbers) * 3, 15)
        
        # If job description provided, check keyword match
        if job_description:
            job_keywords = set(re.findall(r'\b\w+\b', job_description.lower()))
            resume_keywords = set(re.findall(r'\b\w+\b', resume_lower))
            
            # Remove common words
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
            job_keywords -= common_words
            
            if job_keywords:
                match_ratio = len(job_keywords & resume_keywords) / len(job_keywords)
                score += int(match_ratio * 15)
        
        return min(score, 100)
    
    @staticmethod
    def _calculate_formatting_score(resume_text: str, formatting_issues: List[str]) -> int:
        """Calculate formatting score"""
        score = 100
        
        # Deduct for each formatting issue
        score -= len(formatting_issues) * 15
        
        # Check for standard sections
        text_lower = resume_text.lower()
        sections_found = sum(1 for section in ATSChecker.STANDARD_SECTIONS if section in text_lower)
        
        if sections_found < 3:
            score -= 20
        
        # Check for contact information
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        if not re.search(email_pattern, resume_text):
            score -= 15
        if not re.search(phone_pattern, resume_text):
            score -= 10
        
        # Check for special characters that may cause issues
        problematic_chars = ['•', '◆', '►', '★']
        if any(char in resume_text for char in problematic_chars):
            score -= 5
        
        return max(score, 0)
    
    @staticmethod
    def _calculate_content_score(resume_text: str) -> int:
        """Calculate content quality score"""
        score = 60  # Base score
        
        # Check resume length (optimal: 400-800 words)
        word_count = len(resume_text.split())
        if 400 <= word_count <= 800:
            score += 20
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            score += 10
        elif word_count < 300:
            score -= 10
        
        # Check for bullet points (presence of dashes or similar)
        bullet_indicators = ['-', '•', '*']
        has_bullets = any(char in resume_text for char in bullet_indicators)
        if has_bullets:
            score += 10
        
        # Check for professional language (absence of first person pronouns in excess)
        first_person = len(re.findall(r'\b(I|me|my|mine)\b', resume_text, re.IGNORECASE))
        if first_person > 10:
            score -= 10
        
        return min(score, 100)
    
    @staticmethod
    def _get_score_details(score: int) -> str:
        """Get human-readable score interpretation"""
        if score >= 80:
            return "Excellent! Your resume is highly ATS-optimized."
        elif score >= 60:
            return "Good! Your resume should pass most ATS systems with minor improvements."
        elif score >= 40:
            return "Fair. Your resume needs optimization to improve ATS compatibility."
        else:
            return "Poor. Your resume may be rejected by ATS. Significant improvements needed."
    
    @staticmethod
    def get_missing_sections(resume_text: str) -> List[str]:
        """Identify missing standard sections"""
        text_lower = resume_text.lower()
        missing = []
        
        essential_sections = {
            "experience": ["experience", "work experience", "employment"],
            "education": ["education", "academic"],
            "skills": ["skills", "technical skills", "competencies"],
            "contact": ["email", "@", "phone"]
        }
        
        for section_type, keywords in essential_sections.items():
            if not any(keyword in text_lower for keyword in keywords):
                missing.append(section_type.title())
        
        return missing