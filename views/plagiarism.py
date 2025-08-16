import logging
import google.generativeai as genai
import re
from hashlib import md5
from flask import render_template
from project.models.code_plag_log import CodePlagLog
from project.models import db

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuration
GEMINI_API_KEY = "AIzaSyCfZzpfygluvpTyqGANIgdRpiilug9xur4"
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Initialize Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    logger.info("Gemini initialized successfully")
except Exception as e:
    logger.error(f"Gemini initialization failed: {e}")

def init_db():
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS code_plag_logs (
                id SERIAL PRIMARY KEY,
                language VARCHAR(20) NOT NULL,
                original_code TEXT NOT NULL,
                cleaned_code TEXT NOT NULL,
                debug_info TEXT NOT NULL,
                plagiarism_score FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );""")
        conn.commit()
        logger.info("code_plag_logs table already exists")
        return True
    except Error as e:
        logger.error(f"Database initialization failed: {e}")
        return False
    finally:
        if conn:
            conn.close()

def save_to_db(language, original_code, cleaned_code, debug_info, plagiarism_score):
    try:
        log = CodePlagLog(
            language=language,
            original_code=original_code,
            cleaned_code=cleaned_code,
            debug_info=debug_info,
            plagiarism_score=plagiarism_score
        )
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database save failed: {e}")
        return False

def call_gemini_for_plagiarism(code, language):
    try:
        prompt = (
            f"Check this {language} code for plagiarism. "
            "If plagiarism is detected, rewrite the code to be original. "
            "Provide:\n"
            "1. Cleaned code\n"
            "2. Debug info (what was changed and why)\n"
            "3. Plagiarism score (0-100)\n\n"
            f"{language} Code:\n{code}\n\n"
            "Format your response as:\n"
            "### Cleaned Code:\n[code here]\n\n"
            "### Debug Info:\n[debug info]\n\n"
            "### Plagiarism Score:\n[score]\n"
        )
        response = model.generate_content(prompt)
        result = response.text

        cleaned = re.search(r"### Cleaned Code:\s*(.*?)(?=\n###|\Z)", result, re.DOTALL)
        debug_info = re.search(r"### Debug Info:\s*(.*?)(?=\n###|\Z)", result, re.DOTALL)
        score = re.search(r"### Plagiarism Score:\s*(.*?)(?=\n###|\Z)", result, re.DOTALL)

        cleaned_code = cleaned.group(1).strip() if cleaned else code
        debug_info_text = debug_info.group(1).strip() if debug_info else "No debug info"
        plagiarism_score = float(score.group(1).strip()) if score else 0.0

        return cleaned_code, debug_info_text, plagiarism_score
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return code, f"API Error: {str(e)}", 0.0

def check_plagiarism_and_fix(code, language):
    if not code.strip():
        return code, "No code provided", 0.0

    cleaned_code, debug_info, plagiarism_score = call_gemini_for_plagiarism(code, language)

    # Save to database
    init_db()
    save_to_db(language, code, cleaned_code, debug_info, plagiarism_score)

    return cleaned_code, debug_info, plagiarism_score

def check_plagiarism_view(request):
    if request.method == 'POST':
        code = request.form['code']
        language = request.form['language'].lower()
        cleaned_code, debug_info, plagiarism_score = check_plagiarism_and_fix(code, language)
        return render_template(
            'plagiarism.html',
            code=code,
            result=cleaned_code,
            report=debug_info,
            score=plagiarism_score,
            language=language
        )
    return render_template('plagiarism.html', code=None, result=None, report=None, score=None)