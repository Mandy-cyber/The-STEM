from email.policy import default
from . import db 
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(128))
    username = db.Column(db.String(32))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(16))
    eduLevel = db.Column(db.String(128)) #education level
    wildFactor = db.Column(db.String(32)) #some chosen identity (e.g queer)
    similar_people = db.relationship('SimilarPeople')


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    message = db.Column(db.String(512))


class MailingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mailer_name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    res_name = db.Column(db.String(256))
    res_link = db.Column(db.String(1024))
    res_summary = db.Column(db.String(1024))
    res_type = db.Column(db.String(64))


class SimilarPeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lnk = db.Column(db.String())