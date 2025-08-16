import logging
import google.generativeai as genai
import re
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from flask import render_template

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
            CREATE TABLE IF NOT EXISTS code_doc_logs (
                id SERIAL PRIMARY KEY,
                language VARCHAR(20) NOT NULL,
                original_code TEXT NOT NULL,
                documentation TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );""")
        conn.commit()
        logger.info("code_doc_logs table already exists")
        return True
    except Error as e:
        logger.error(f"Database initialization failed: {e}")
        return False
    finally:
        if conn:
            conn.close()

def save_to_db(language, original_code, documentation):
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO code_doc_logs 
            (language, original_code, documentation) 
            VALUES (%s, %s, %s)
            """, 
            (language, original_code, documentation))
        conn.commit()
        logger.info("Saved to database")
        return True
    except Error as e:
        logger.error(f"Database save failed: {e}")
        return False
    finally:
        if conn:
            conn.close()

def call_gemini_for_documentation(code, language):
    try:
        prompt = (
            f"Generate detailed documentation for this {language} code. "
            "Include:\n"
            "1. Overview\n"
            "2. Function/class descriptions\n"
            "3. Usage examples\n\n"
            f"{language} Code:\n{code}\n\n"
            "Format your response as:\n"
            "### Documentation:\n[documentation here]\n"
        )
        response = model.generate_content(prompt)
        result = response.text

        documentation = re.search(r"### Documentation:\s*(.*)", result, re.DOTALL)
        documentation_text = documentation.group(1).strip() if documentation else "No documentation generated."

        return documentation_text
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return f"API Error: {str(e)}"

def generate_pdf(documentation):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Code Documentation", styles['Title']))
    story.append(Spacer(1, 0.2 * inch))
    for section in documentation.split('\n\n'):
        story.append(Paragraph(section, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_documentation(code, language):
    documentation = call_gemini_for_documentation(code, language)
    pdf_buffer = generate_pdf(documentation)

    # Save to database
    init_db()
    save_to_db(language, code, documentation)

    return documentation, pdf_buffer

def document_view(request, send_file):
    if request.method == 'POST':
        code = request.form['code']
        language = request.form['language']
        documentation, pdf_buffer = generate_documentation(code, language)
        if request.form.get('download') == 'pdf' and pdf_buffer:
            pdf_buffer.seek(0)
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name='code_documentation.pdf',
                mimetype='application/pdf'
            )
        return render_template(
            'document.html',
            code=code,
            result=documentation,
            language=language
        )
    return render_template('document.html', code=None, result=None)