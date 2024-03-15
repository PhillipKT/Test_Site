import requests

# URL of your Flask application
flask_url = "http://localhost:5000/info"

# Message to send
message = "Hello from sender script!"

# Send a POST request to the Flask application
response = requests.post(flask_url, json={"message": message})

# Check if the request was successful
if response.status_code == 200:
    print("Message sent successfully.")
else:
    print("Failed to send message.")
