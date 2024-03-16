#!/bin/bash

# Define the services and their corresponding SSH usernames in an associative array
declare -A SERVICE_USERS=(
    ["username1"]="service1 service2"
    ["username2"]="rabbitmq"
    ["username3"]="apache2"
)

# Loop through each username in the array
for SSH_USERNAME in "${!SERVICE_USERS[@]}"; do
    SERVICES="${SERVICE_USERS[$SSH_USERNAME]}"
    
    echo "Checking service status for user $SSH_USERNAME..."
    
    # Loop through each service associated with the current username
    for SERVICE_NAME in $SERVICES; do
        echo "Checking service status of $SERVICE_NAME for user $SSH_USERNAME..."
        #Iterate through map for services of current user
        if ssh "$SSH_USERNAME@your_remote_server" sudo systemctl is-active --quiet "$SERVICE_NAME"; then
            echo "Service $SERVICE_NAME is already running."
        else
            echo "Service $SERVICE_NAME is not running. Starting it..."
            ssh "$SSH_USERNAME@your_remote_server" sudo systemctl start "$SERVICE_NAME"
        fi

    done
done
