"""Initialize Flask app"""
from flask import Flask
from .extensions import db
from datetime import timedelta


def create_app():
    """Create Flask application"""
    app = Flask(__name__, instance_relative_config=False)
    # SQL configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # required secret key for data transfer to backend
    app.secret_key = "team7"
    # session timeout
    app.permanent_session_lifetime = timedelta(minutes=3)

    #Initialize SQLAlchemy object
    db.init_app(app)
    
    #Import the parts of the application
    from .home.routes import home_bp
    from .admin.routes import admin_bp
    from .user.routes import user_bp

    #Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    
    return app 