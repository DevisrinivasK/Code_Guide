import logging
import google.generativeai as genai
import re
import time
from flask import render_template
from project.models.code_opt_log import CodeOptLog
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
            CREATE TABLE IF NOT EXISTS code_opt_logs (
                id SERIAL PRIMARY KEY,
                language VARCHAR(20) NOT NULL,
                original_code TEXT NOT NULL,
                optimized_code TEXT NOT NULL,
                debug_info TEXT NOT NULL,
                exec_time FLOAT,
                opt_level VARCHAR(10),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );""")
        conn.commit()
        logger.info("code_opt_logs table already exists")
        return True
    except Error as e:
        logger.error(f"Database initialization failed: {e}")
        return False
    finally:
        if conn:
            conn.close()

def save_to_db(language, original_code, optimized_code, debug_info, exec_time, opt_level):
    try:
        log = CodeOptLog(
            language=language,
            original_code=original_code,
            optimized_code=optimized_code,
            debug_info=debug_info,
            exec_time=exec_time,
            opt_level=opt_level
        )
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database save failed: {e}")
        return False

def call_gemini_for_optimization(code, language):
    try:
        prompt = (
            f"Optimize this {language} code for performance, readability, and maintainability. "
            "Provide:\n"
            "1. Optimized code\n"
            "2. Debug info (what was changed and why)\n"
            "3. Estimated execution time improvement\n"
            "4. Optimization level applied\n\n"
            f"{language} Code:\n{code}\n\n"
            "Format your response as:\n"
            "### Optimized Code:\n[code here]\n\n"
            "### Debug Info:\n[debug info]\n\n"
            "### Execution Time:\n[time]\n\n"
            "### Optimization Level:\n[level]\n"
        )
        response = model.generate_content(prompt)
        result = response.text

        optimized = re.search(r"### Optimized Code:\s*(.*?)(?=\n###|\Z)", result, re.DOTALL)
        debug_info = re.search(r"### Debug Info:\s*(.*?)(?=\n###|\Z)", result, re.DOTALL)
        exec_time = re.search(r"### Execution Time:\s*(.*?)(?=\n###|\Z)", result, re.DOTALL)
        opt_level = re.search(r"### Optimization Level:\s*(.*?)(?=\n###|\Z)", result, re.DOTALL)

        optimized_code = optimized.group(1).strip() if optimized else code
        debug_info_text = debug_info.group(1).strip() if debug_info else "No debug info"
        exec_time_val = float(exec_time.group(1).strip()) if exec_time else 0.0
        opt_level_val = opt_level.group(1).strip() if opt_level else "O1"

        return optimized_code, debug_info_text, exec_time_val, opt_level_val
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return code, f"API Error: {str(e)}", 0.0, "O0"

def optimize_code(code, language):
    if not code.strip():
        return code, "No code provided", 0.0, "O0"

    start_time = time.time()
    optimized_code, debug_info, exec_time, opt_level = call_gemini_for_optimization(code, language)
    end_time = time.time()
    measured_exec_time = round(end_time - start_time, 4)

    # Save to database
    init_db()
    save_to_db(language, code, optimized_code, debug_info, measured_exec_time, opt_level)

    return optimized_code, debug_info, measured_exec_time, opt_level

def optimize_view(request):
    if request.method == 'POST':
        code = request.form['code']
        language = request.form['language']
        optimized_code, debug_info, exec_time, opt_level = optimize_code(code, language)
        return render_template(
            'optimize.html',
            code=code,
            result=optimized_code,
            report=debug_info,
            exec_time=exec_time,
            opt_level=opt_level,
            language=language
        )
    return render_template('optimize.html', code=None, result=None, report=None, exec_time=None, opt_level=None)