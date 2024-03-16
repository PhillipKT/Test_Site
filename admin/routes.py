from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from pika import BlockingConnection, ConnectionParameters, BasicProperties
from ..extensions import db
from ..models import Users


#Blueprint Config
admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_queue = 'hello'


def send_message_to_rabbitmq(message):
    """Takes message from client to send to rabbit exchange"""
    connection = BlockingConnection(ConnectionParameters(rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue)
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)
    connection.close()

@admin_bp.route("/")
def home():
    return render_template("admin.html")

@admin_bp.route("/test")
def test():
    return "<h1>Test</h1>"


@admin_bp.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())

@admin_bp.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    if not message:
        # TODO Flash message instead
        return jsonify({'error': 'Message is required'}), 400
    send_message_to_rabbitmq(message)
    # TODO flash message and return to admin home
    return jsonify({'status': 'Message sent successfully'}), 200


@admin_bp.route('/receive-message', methods=['GET'])
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
       return redirect(url_for("home"))
    
@admin_bp.route("/delete", methods=['POST'])
def delete(user):
    found_user = Users.query.filter_by(name=user).delete()
    for user in found_user:
        user.delete()
    return redirect("home")