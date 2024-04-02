# models.py
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) 
    active_sessions = db.Column(db.Integer, default=0)
    email = db.Column(db.String(120), unique=True, nullable=True)  
    otp = db.Column(db.Integer)

