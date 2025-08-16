from . import db

class CodeAnalysisLog(db.Model):
    __tablename__ = 'code_analysis_logs'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), nullable=False)
    original_code = db.Column(db.Text, nullable=False)
    corrected_code = db.Column(db.Text, nullable=False)
    error_report = db.Column(db.Text, nullable=False)
    error_count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())