from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
#     email = db.Column(db.String(345), unique=True)
#     password = db.Column(db.Text, nullable=False)

class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True, unique=True, default=get_uuid)
    code = db.Column(db.String(345), unique=True)
    name = db.Column(db.String(345), unique=True)

def __repr__(self):
    return f' <Country {self.name}>'
    
    