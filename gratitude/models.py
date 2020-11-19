from flask_sqlalchemy import SQLAlchemy
from gratitude import db


class Dataentry(db.Model):
    __tablename__ = "dataentry"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())

    def __init__ (self, data):
        self.data = data



class Adhkarentry(db.Model):
    __tablename__ = "adhkar"
    id = db.Column(db.Integer, primary_key=True)
    arabic = db.Column(db.Text())
    english = db.Column(db.Text())
    secondsToRecite = db.Column(db.Integer)
    minutesToRecite = db.Column(db.Integer)
    shortDescription = db.Column(db.Text())

    def __init__ (self, arabic, english, secondsToRecite,    minutesToRecite, shortDescription):
        self.arabic = arabic
        self.english = english
        self.secondsToRecite = secondsToRecite
        self.minutesToRecite = minutesToRecite
        self.shortDescription = shortDescription

