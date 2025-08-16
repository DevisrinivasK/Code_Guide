from . import db

class CodeOptLog(db.Model):
    __tablename__ = 'code_opt_logs'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), nullable=False)
    original_code = db.Column(db.Text, nullable=False)
    optimized_code = db.Column(db.Text, nullable=False)
    debug_info = db.Column(db.Text, nullable=False)
    exec_time = db.Column(db.Float)
    opt_level = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())