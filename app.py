from flask import Flask, redirect, url_for, render_template, jsonify, request, session, flash
from pika import BlockingConnection, ConnectionParameters, BasicProperties
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
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

app.app_context().push()
db.create_all()


# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_queue = 'hello'


def send_message_to_rabbitmq(message):
    connection = BlockingConnection(ConnectionParameters(rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
    connection.close()

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    send_message_to_rabbitmq(message)
    return jsonify({'status': 'Message sent successfully'}), 200


@app.route('/receive-message', methods=['GET'])
def receive_message():
    connection = BlockingConnection(ConnectionParameters(rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    method_frame, header_frame, body = channel.basic_get(queue=rabbitmq_queue)
    messages = []
    if method_frame:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return render_template('receive_message.html', messages=messages)
    else:
        redirect(url_for("home"))
    

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        user = request.form["nm"]
        session ["user"] = user

        #query database for existing users
        found_user = Users.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users()
            db.session.add(usr)
            db.session.commit()

        flash(f"Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
    return render_template("login.html")


@app.route('/user', methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = db.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved.")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash(f"You are not logged in.")
        return redirect(url_for("login"))
    
    # message = receive_message()
    # return render_template('index.html', message=message)

@app.route("/logout")
def logout():
    flash(f"You have been logged out!")
    session.pop("user", None)
    session.pop("email", None)

if __name__ == "__main__":
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
