from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask import current_app as app
from pika import BlockingConnection, ConnectionParameters, BasicProperties


#Blueprint Config
admin_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

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

@app.route("/")
def home():
    return render_template("admin.html")

@app.route("/test")
def test():
    return "<h1>Test</h1>"


@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())

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
       return redirect(url_for("home"))
    
# @app.route("/delete", methods=['POST'])
# def delete():
#     found_user = Users.query.filter_by(name=user).delete()
#     for user in found_user:
#         user.delete()
#     return redirect("home")