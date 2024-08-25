from flask_login import UserMixin
from . import db
from datetime import date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    active_sessions = db.Column(db.Integer, default=0)
    email = db.Column(db.String(120), unique=True, nullable=True)
    otp = db.Column(db.Integer)
    stage = db.Column(db.String(50), nullable=True, default=3)
    type = db.Column(db.String(50), default="student")
    created_by = db.Column(db.String(50), nullable=True)
    logs = db.Column(db.Text, nullable=True, default='[]')  # Store logs as JSON string
    subscription_date = db.Column(db.Date, nullable=True)
    subscription_method = db.Column(db.String(50), default="None")
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
