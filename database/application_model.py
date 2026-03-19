from database.db import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_no = db.Column(db.String(30), unique=True)
    full_name = db.Column(db.String(150))
    aadhaar_number = db.Column(db.String(12))
    pan_number = db.Column(db.String(10))
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(10))
    data_json = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)