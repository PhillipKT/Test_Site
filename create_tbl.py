"""Script to create tables"""
from website import app, db 

# Import your models here
from website import Users

# Create all import tables
with app.app_context():
    db.create_all()
