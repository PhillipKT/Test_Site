from flask import (Blueprint, render_template, 
                   session, request, redirect, flash, url_for)
from ..extensions import db
from ..models import Users

#Blueprint Config
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/')
def home():
    """Returns home page"""
    return render_template("index.html")