# 📄 ResumeCV Optimizer & ATS Checker

> 🚀 A powerful AI-driven application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and specific job descriptions. Built with FastAPI backend and modern web technologies.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 🎯 **ATS Score Analysis**: Get detailed compatibility scores between your resume and job descriptions
- 🤖 **AI-Powered Optimization**: Receive intelligent suggestions to improve your resume
- 📊 **Resume Parsing**: Extract and analyze key information from your resume
- 🔍 **Job Description Matching**: Compare your skills and experience against job requirements
- 📑 **PDF Support**: Upload and process PDF resumes seamlessly
- ⚡ **Real-time Feedback**: Instant analysis and recommendations

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.8+** - Core programming language
- **OpenAI GPT** - AI-powered resume analysis and optimization
- **PyPDF2** - PDF parsing and text extraction
- **Pydantic** - Data validation and settings management
- **CORS Middleware** - Cross-origin resource sharing support

### Frontend
- 🎨 Modern web interface for seamless user experience
- 📱 Responsive design for desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

- ✅ Python 3.8 or higher
- ✅ OpenAI API key
- ✅ pip (Python package manager)

### 📦 Installation

1️⃣ **Clone the repository:**
```bash
git clone https://github.com/riponalmamun/ResumeCV-Optimizer-ATS-Checker-backend.git
cd ResumeCV-Optimizer-ATS-Checker-backend
```

2️⃣ **Create a virtual environment:**
```bash
python -m venv venv
```

3️⃣ **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

5️⃣ **Create a `.env` file in the root directory:**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### ▶️ Running the Application

Start the FastAPI server:
```bash
uvicorn backend.app.main:app --reload
```

🎉 The API will be available at `http://localhost:8000`

### 📚 API Documentation

Once the server is running, visit:
- 📖 **Swagger UI**: `http://localhost:8000/docs`
- 📘 **ReDoc**: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### 🏥 Health Check
```
GET /
```
Returns API status and version information.

### 🔍 Analyze Resume
```
POST /analyze
```
Upload a resume (PDF) and job description to receive:
- ✅ ATS compatibility score
- 🔑 Keyword matching analysis
- 📊 Skills gap identification
- 💡 Optimization recommendations

**Request Body:**
- `resume`: PDF file
- `job_description`: Text describing the job requirements

**Response:**
```json
{
  "ats_score": 85,
  "matched_keywords": [...],
  "missing_keywords": [...],
  "recommendations": [...],
  "summary": "..."
}
```

## 📂 Project Structure

```
ResumeCV-Optimizer-ATS-Checker-backend/
├── 📁 backend/
│   └── 📁 app/
│       ├── 📄 main.py              # FastAPI application entry point
│       ├── ⚙️ config.py            # Configuration management
│       ├── 📋 models.py            # Pydantic models
│       ├── 📁 services/            # Business logic
│       └── 📁 utils/               # Helper functions
├── 🔒 .env                         # Environment variables (not tracked)
├── 🚫 .gitignore                   # Git ignore rules
├── 📦 requirements.txt             # Python dependencies
└── 📖 README.md                    # Project documentation
```

## 🔐 Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=pdf
```

## 🔒 Security

- 🔑 API keys and sensitive data are stored in environment variables
- 📏 File upload size limits are enforced
- 📄 Only PDF files are accepted for resume uploads
- ✅ Input validation using Pydantic models

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔀 Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- 🤖 OpenAI for GPT API
- ⚡ FastAPI community
- 👥 All contributors and users

## 💬 Support

For issues, questions, or suggestions:
- 🐛 Open an issue on GitHub
- 📧 Contact: [Your Email]

## 🗺️ Roadmap

- [ ] 📝 Add support for multiple resume formats (DOCX, TXT)
- [ ] 🔐 Implement user authentication
- [ ] 🎨 Add resume templates
- [ ] 🌐 Create browser extension
- [ ] 📦 Add batch processing for multiple resumes
- [ ] 🔗 Integrate with job boards APIs
- [ ] 📊 Advanced analytics dashboard
- [ ] 🌍 Multi-language support

## 📸 Screenshots

_Coming soon..._

## 🌟 Star History

If you find this project helpful, please give it a ⭐ on GitHub!

---

**⚠️ Note**: Remember to keep your OpenAI API key secure and never commit it to version control.

Made with ❤️ by [Ripon Al Mamun](https://github.com/riponalmamun)
