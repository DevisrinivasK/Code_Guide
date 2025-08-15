from flask import render_template, request, send_file
from .views import (
    fix_errors_view,
    optimize_view,
    check_plagiarism_view,
    document_view
)

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/fix-errors', methods=['GET', 'POST'])
    def fix_errors():
        return fix_errors_view(request)

    @app.route('/optimize', methods=['GET', 'POST'])
    def optimize():
        return optimize_view(request)

    @app.route('/check-plagiarism', methods=['GET', 'POST'])
    def check_plagiarism():
        return check_plagiarism_view(request)

    @app.route('/document', methods=['GET', 'POST'])
    def document():
        return document_view(request, send_file)