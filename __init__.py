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
    # config for Blueprints
    app.config.from_object('config.Config')
    # required secret key for data transfer to backend
    app.secret_key = "Team7"
    # session timeout
    app.permanent_session_lifetime = timedelta(minutes=3)

    with app.app_context():
        #Import the parts of the application
        from .home import routes
        from .admin import routes
        from .user import routes

        #Register Blueprints
        app.register_blueprint(routes.home_bp)
        app.register_blueprint(routes.admin_bp)
        app.register_blueprint(routes.user_bp)

        return app
    
app = create_app
db.init_app(app)


app.run(host='127.0.0.1', port=5000, debug=True)