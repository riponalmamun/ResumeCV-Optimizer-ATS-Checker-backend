from ..utils.pdf_extractor import PDFExtractor
from ..utils.docx_extractor import DOCXExtractor
from .ats_checker import ATSChecker
from .ai_analyzer import AIAnalyzer
from ..models.schemas import ResumeAnalysis, ATSScore, ResumeSection, ImprovementSuggestion
from typing import Optional

class ResumeParser:
    @staticmethod
    async def parse_and_analyze(
        file_content: bytes,
        filename: str,
        job_title: Optional[str] = None,
        job_description: Optional[str] = None,
        target_industry: Optional[str] = None
    ) -> ResumeAnalysis:
        """Main function to parse and analyze resume"""
        
        # Step 1: Extract text based on file type
        file_extension = filename.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            resume_text = PDFExtractor.extract_text(file_content)
            formatting_issues = PDFExtractor.check_formatting_issues(file_content)
        elif file_extension in ['docx', 'doc']:
            resume_text = DOCXExtractor.extract_text(file_content)
            formatting_issues = DOCXExtractor.check_formatting_issues(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        if not resume_text.strip():
            raise ValueError("Could not extract text from resume. Please ensure the file is not empty or corrupted.")
        
        # Step 2: Calculate ATS Score
        ats_result = ATSChecker.calculate_ats_score(
            resume_text, 
            formatting_issues,
            job_description
        )
        
        ats_score = ATSScore(**ats_result)
        
        # Step 3: AI-powered content analysis
        ai_analysis = AIAnalyzer.analyze_resume_content(
            resume_text,
            job_title,
            job_description
        )
        
        # Step 4: Section-by-section analysis
        sections_data = AIAnalyzer.analyze_sections(resume_text)
        sections_analysis = [ResumeSection(**section) for section in sections_data]
        
        # Step 5: Compile improvement suggestions
        improvement_suggestions = [
            ImprovementSuggestion(**suggestion) 
            for suggestion in ai_analysis.get('improvement_suggestions', [])
        ]
        
        # Add formatting issues as suggestions
        for issue in formatting_issues:
            improvement_suggestions.append(
                ImprovementSuggestion(
                    category="Formatting",
                    priority="High",
                    issue=issue,
                    suggestion="Fix this formatting issue for better ATS compatibility",
                    example=None
                )
            )
        
        # Step 6: Check for missing sections
        missing_sections = ATSChecker.get_missing_sections(resume_text)
        missing_elements = ai_analysis.get('missing_elements', []) + missing_sections
        
        # Step 7: Get keyword suggestions if job info provided
        if job_title and ats_result['keyword_score'] < 70:
            keyword_suggestions = AIAnalyzer.get_keyword_suggestions(
                resume_text, 
                job_title, 
                job_description
            )
            if keyword_suggestions:
                improvement_suggestions.append(
                    ImprovementSuggestion(
                        category="Keywords",
                        priority="High",
                        issue="Missing important keywords for the target role",
                        suggestion=f"Consider adding these relevant keywords: {', '.join(keyword_suggestions[:5])}",
                        example=None
                    )
                )
        
        # Step 8: Compile final analysis
        analysis = ResumeAnalysis(
            ats_score=ats_score,
            sections_analysis=sections_analysis,
            improvement_suggestions=improvement_suggestions,
            strengths=ai_analysis.get('strengths', []),
            missing_elements=list(set(missing_elements)),  # Remove duplicates
            overall_feedback=ai_analysis.get('overall_feedback', '')
        )
        
        return analysis
