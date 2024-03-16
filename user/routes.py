from flask import (Blueprint, render_template,
                    session, request, redirect, flash, url_for)
from ..extensions import db
from ..models import Users

#Blueprint Config
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@user_bp.route('/user', methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved.")
        else:
            if "email" in session:
                email = session["email"]
                flash(f"Welcome Back!")                

        return render_template("user.html", email=email)
    else:
        flash(f"You are not logged in.")
        return redirect(url_for("home.login"))
    
    # message = receive_message()
    # return render_template('index.html', message=message)

@user_bp.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out!")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))