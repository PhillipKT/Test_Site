from ..extensions import (Blueprint, render_template, 
                   session, request, redirect, flash, url_for)
from extensions import db
from models import Users

#Blueprint Config
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/')
def home():
    return render_template("index.html")


@home_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session ["user"] = user

        #query database for existing users
        found_user = Users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash(f"Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
    return render_template("login.html")