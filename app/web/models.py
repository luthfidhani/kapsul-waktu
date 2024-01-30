from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from web import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypted_message = db.Column(db.String(255), nullable=False)
    encryption_key = db.Column(db.String(255), nullable=False)
    url_hash = db.Column(db.String(64), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
