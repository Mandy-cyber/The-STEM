from email.policy import default
from . import db 
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(16))
    eduLevel = db.Column(db.String(128)) #education level
    wildFactor = db.Column(db.String(32)) #some chosen identity (e.g queer)