#!/bin/bash

SERVICE_NAME="logpipeline.service" # Replace with the actual service name

echo "Attempting to start $SERVICE_NAME..."

# Check if the service is already running
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "$SERVICE_NAME is already running."
else

    # Create SymLink
    sudo ln -s /var/www/sysadmin-toolkit/setup/logpipeline.service /etc/systemd/system/logpipeline.service

    sudo systemctl daemon-reload
    # Enable the service
    sudo systemctl enable "$SERVICE_NAME"
    # Start the service
    sudo systemctl start "$SERVICE_NAME"

    # Check if the service started successfully
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo "$SERVICE_NAME started successfully."
    else
        echo "Failed to start $SERVICE_NAME. Check logs for details."
    fi
fi