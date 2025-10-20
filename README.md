# 🎯 CareerUp - AI Resume Analyzer & Job Matcher

CareerUp is a web application that analyzes student resumes using AI and recommends matching jobs/internships.

## 🚀 Features

- **PDF Resume Upload**: Drag & drop or browse to upload PDF resumes
- **AI Analysis**: Uses Google Gemini AI via LangChain to extract:
  - Skills (technical & soft)
  - Areas for improvement
  - Suitable job roles
  - Experience level
- **Job Matching**: Fetches real job/internship listings from JSearch API based on extracted skills
- **Modern UI**: Clean, responsive React interface

## 🛠️ Tech Stack

### Frontend
- React.js
- Axios for API calls
- Modern CSS with animations

### Backend
- Flask (Python)
- PyMuPDF (fitz) for PDF parsing
- LangChain + Google Gemini API for AI analysis
- JSearch API (RapidAPI) for job listings

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **API Keys**:
  - Google Gemini API key
  - RapidAPI JSearch API key

## 🔧 Installation & Setup

### 1. Backend Setup

```cmd
cd backend

REM Install Python dependencies
pip install -r requirements.txt
```

The `.env` file is already configured with your API keys.

### 2. Frontend Setup

```cmd
cd frontend

REM Install Node dependencies
npm install
```

## ▶️ Running the Application

### Start Backend (Terminal 1)

```cmd
cd backend
python app.py
```

Backend will run on `http://localhost:5000`

### Start Frontend (Terminal 2)

```cmd
cd frontend
npm start
```

Frontend will run on `http://localhost:3000`

## 📖 How to Use

1. Open `http://localhost:3000` in your browser
2. Upload a PDF resume (drag & drop or click to browse)
3. Click "Analyze Resume"
4. Wait for AI analysis and job matching (~10-20 seconds)
5. View results:
   - Identified skills
   - Areas to improve
   - Suitable job roles
   - Matching job listings with apply links

## 📁 Project Structure

```
careerup/
├── backend/
│   ├── app.py              # Flask main app
│   ├── resume_parser.py    # PDF text extraction (PyMuPDF)
│   ├── ai_analyzer.py      # LangChain + Gemini analysis
│   ├── job_fetcher.py      # JSearch API integration
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # API keys (configured)
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styles
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Global styles
│   ├── package.json       # Node dependencies
│   └── .gitignore
└── README.md
```

## 🔑 API Keys Configuration

API keys are stored in `backend/.env`:

```env
GEMINI_API_KEY=AIzaSyAZqdREs4qu_zwZhW1vgosqgzlAHz397Hk
JSEARCH_API_KEY=2c3d611c5cmsh6cf91b87ec1d26fp1abOb7jsn64a79d6e6df1
```

## 🧪 Testing the Backend

Test the health endpoint:

```cmd
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "CareerUp Backend",
  "gemini_configured": true,
  "jsearch_configured": true
}
```

## ⚠️ Troubleshooting

### Backend Issues

- **Module not found**: Run `pip install -r requirements.txt`
- **API key errors**: Check `.env` file has valid keys
- **PDF parsing fails**: Ensure uploaded file is a valid PDF

### Frontend Issues

- **npm install fails**: Try `npm install --legacy-peer-deps`
- **Proxy errors**: Ensure backend is running on port 5000
- **CORS errors**: Flask-CORS should handle this automatically

## 🎨 UI Features

- Gradient purple background
- Drag & drop file upload
- Loading spinner during analysis
- Animated result cards
- Responsive grid layout
- Hover effects on job cards
- Direct "Apply Now" links

## 📊 How It Works

1. **Upload**: User uploads PDF resume via React frontend
2. **Parse**: Backend extracts text using PyMuPDF
3. **Analyze**: LangChain sends resume text to Gemini AI with structured prompt
4. **Extract**: AI returns JSON with skills, weaknesses, suitable roles
5. **Search**: Backend queries JSearch API with top 3 skills
6. **Display**: Frontend shows analysis + job listings

## 🚀 Future Enhancements

- User authentication & profile storage
- Resume improvement suggestions
- PDF resume generation
- Job application tracking
- Email alerts for new matching jobs
- LinkedIn integration
- Multi-language support

## 📝 Notes

- PDF files are automatically deleted after processing
- Maximum file size: 10MB
- Only PDF format supported
- Jobs are searched based on top 3 skills for relevance

## 🤝 Contributing

This is an MVP. Feel free to extend with:
- Unit tests
- Docker setup
- CI/CD pipeline
- Database for user history
- Advanced filtering options

---

**Made with ❤️ using React, Flask, LangChain, and Gemini AI**
