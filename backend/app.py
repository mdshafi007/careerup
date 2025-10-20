"""
CareerUp Flask Backend
Handles resume upload, parsing, AI analysis, and job matching.
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from resume_parser import extract_text_from_pdf
from ai_analyzer import analyze_resume
from job_fetcher import fetch_jobs_by_skills
from job_fetcher_adzuna import fetch_jobs_adzuna

# Load environment variables
load_dotenv()

app = Flask(__name__)

# CORS Configuration for production
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://*.vercel.app",
            "https://careerup.vercel.app"  # Update this with your actual Vercel domain
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
JSEARCH_API_KEY = os.getenv('JSEARCH_API_KEY')
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.getenv('ADZUNA_APP_KEY')


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'CareerUp Backend',
        'gemini_configured': bool(GEMINI_API_KEY),
        'adzuna_configured': bool(ADZUNA_APP_ID and ADZUNA_APP_KEY),
        'jsearch_configured': bool(JSEARCH_API_KEY)
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_resume_endpoint():
    """
    Main endpoint to upload resume, analyze it, and fetch matching jobs.
    
    Expects:
        - 'resume' file in multipart/form-data
        
    Returns:
        - JSON with analysis (skills, weaknesses, suitable_roles) and job matches
    """
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Step 1: Extract text from PDF
            resume_text = extract_text_from_pdf(filepath)
            
            if not resume_text or len(resume_text) < 50:
                return jsonify({'error': 'Resume appears to be empty or unreadable'}), 400
            
            # Step 2: Analyze resume with AI
            analysis = analyze_resume(resume_text, GEMINI_API_KEY)
            
            # Step 3: Fetch matching jobs - use Adzuna API (real apply links for India)
            jobs = []
            if analysis.get('skills') and len(analysis['skills']) > 0:
                # Use Adzuna as PRIMARY source (real apply links)
                if ADZUNA_APP_ID and ADZUNA_APP_KEY:
                    try:
                        print("🔍 Fetching jobs from Adzuna API (India)...")
                        jobs = fetch_jobs_adzuna(
                            analysis['skills'],
                            ADZUNA_APP_ID,
                            ADZUNA_APP_KEY,
                            max_results=15,
                            job_roles=analysis.get('suitable_roles')
                        )
                    except Exception as adzuna_error:
                        print(f"❌ Adzuna API failed: {adzuna_error}")
                        # Fallback to JSearch if Adzuna fails
                        if JSEARCH_API_KEY:
                            try:
                                print("🔄 Trying JSearch API as backup...")
                                jobs = fetch_jobs_by_skills(
                                    analysis['skills'], 
                                    JSEARCH_API_KEY,
                                    job_roles=analysis.get('suitable_roles')
                                )
                            except Exception as jsearch_error:
                                print(f"⚠️  JSearch also failed: {jsearch_error}")
                else:
                    print("⚠️  Adzuna credentials not configured, trying JSearch...")
                    if JSEARCH_API_KEY:
                        try:
                            jobs = fetch_jobs_by_skills(
                                analysis['skills'], 
                                JSEARCH_API_KEY,
                                job_roles=analysis.get('suitable_roles')
                            )
                        except Exception as job_error:
                            print(f"⚠️  JSearch failed: {job_error}")
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Return combined response
            return jsonify({
                'success': True,
                'analysis': {
                    'skills': analysis.get('skills', []),
                    'weaknesses': analysis.get('weaknesses', []),
                    'suitable_roles': analysis.get('suitable_roles', []),
                    'experience_level': analysis.get('experience_level', 'unknown')
                },
                'jobs': jobs,
                'resume_preview': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text
            })
        
        except Exception as e:
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 CareerUp Backend Starting...")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"🔑 Gemini API configured: {bool(GEMINI_API_KEY)}")
    print(f"🔑 Adzuna API configured: {bool(ADZUNA_APP_ID and ADZUNA_APP_KEY)} (PRIMARY)")
    print(f"🔑 JSearch API configured: {bool(JSEARCH_API_KEY)} (Backup)")
    print(f"🇮🇳 Focus: Indian Jobs & Internships with REAL apply links")
    
    # Use PORT from environment variable for Railway deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
