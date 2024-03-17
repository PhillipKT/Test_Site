"""Script to create tables"""
from ..Test_Site import app, db 

# Import your models here
from ..Test_Site.models import Users

# Create all import tables
with app.app_context():
    db.create_all()
