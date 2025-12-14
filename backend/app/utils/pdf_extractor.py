import PyPDF2
from io import BytesIO
from typing import List

class PDFExtractor:
    @staticmethod
    def extract_text(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    @staticmethod
    def check_formatting_issues(file_content: bytes) -> List[str]:
        """Check for common ATS-unfriendly formatting"""
        issues = []
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Check for images
            for page in pdf_reader.pages:
                if '/XObject' in page['/Resources']:
                    issues.append("Contains images/graphics - may not be ATS-friendly")
                    break
            
            # Check for multiple columns (simplified check)
            text = PDFExtractor.extract_text(file_content)
            lines = text.split('\n')
            avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
            
            if avg_line_length < 40:
                issues.append("Possible multi-column layout detected - use single column")
            
            return issues
        except:
            return []
