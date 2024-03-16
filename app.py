from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Team7"
app.permanent_session_lifetime = timedelta(minutes=3)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, name, email) -> None:
        super().__init__()
        self.name = name
        self.email = email

app.app_context().push()


if __name__ == "__main__":
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
