from .extensions import db

class Users(db.Model):
    """Template table for user in database"""
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))