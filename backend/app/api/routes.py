from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from ..services.resume_parser import ResumeParser
from ..config import settings
from typing import Optional
import os

router = APIRouter()

@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Resume Optimizer & ATS Checker API",
        "status": "active",
        "version": "1.0.0"
    }

@router.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_title: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
    target_industry: Optional[str] = Form(None)
):
    """
    Main endpoint to analyze resume
    
    Parameters:
    - file: Resume file (PDF or DOCX)
    - job_title: Optional - target job title
    - job_description: Optional - job description to match against
    - target_industry: Optional - target industry
    
    Returns:
    - Complete resume analysis with ATS score and suggestions
    """
    
    # Validate file extension
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Check file size
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Parse and analyze
        analysis = await ResumeParser.parse_and_analyze(
            file_content=file_content,
            filename=file.filename,
            job_title=job_title,
            job_description=job_description,
            target_industry=target_industry
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "filename": file.filename,
                "analysis": analysis.model_dump()
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Check if API and OpenAI are working"""
    try:
        # Test OpenAI connection
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Simple test
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        
        return {
            "status": "healthy",
            "openai_connection": "active",
            "model": settings.OPENAI_MODEL
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
