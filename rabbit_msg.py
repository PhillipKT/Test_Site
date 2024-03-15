import pika

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_queue = 'hello'

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue)

# Message to send
message = "Hello from RabbitMQ!"

# Publish the message to the queue
channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message)

print("Message sent:", message)

# Close the connection
connection.close()
