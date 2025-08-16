from . import db

class CodeDocLog(db.Model):
    __tablename__ = 'code_doc_logs'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), nullable=False)
    original_code = db.Column(db.Text, nullable=False)
    documentation = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())