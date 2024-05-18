from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    runners = db.relationship('Runner')

class Runner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    jockey= db.Column(db.String(50))
    trainer = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))