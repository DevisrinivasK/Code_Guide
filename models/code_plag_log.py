from . import db

class CodePlagLog(db.Model):
    __tablename__ = 'code_plag_logs'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), nullable=False)
    original_code = db.Column(db.Text, nullable=False)
    cleaned_code = db.Column(db.Text, nullable=False)
    debug_info = db.Column(db.Text, nullable=False)
    plagiarism_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())