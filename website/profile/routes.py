from flask import (Blueprint, render_template,
                    session, request, redirect, flash, url_for)
from ..extensions import db
from ..models import Users

#Blueprint Config
profile_bp = Blueprint(
    'profile_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@profile_bp.route('/login', methods=['POST', 'GET'])
def login():
    """Takes form data saves it into a session and redirects to user page"""
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
            return redirect(url_for("account"))
     
    return render_template("login.html")


@profile_bp.route("/logout")
def logout():
    return "<p>Log Out</p>"


@profile_bp.route("/")
def sign_up():
    return "<p>Sign Up</p>"


@profile_bp.route("/account")
def account():
    return "<p>My Account</p>"