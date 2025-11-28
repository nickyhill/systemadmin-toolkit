#!/bin/bash

SERVICE_NAME="logpipeline.service" # Replace with the actual service name

echo "Attempting to start $SERVICE_NAME..."


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
