#!/bin/bash

# Update package list and install dependencies
echo "Updating package list..."
sudo apt update -y

# Install Python 3 and pip (if not already installed)
echo "Installing Python 3 and pip..."
sudo apt install python3 python3-pip -y

# Install required system dependencies (e.g., for Flask and gunicorn)
echo "Installing system dependencies..."
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y

# Install dependencies from requirements.txt
echo "Installing Python dependencies from requirements.txt..."
pip3 install -r requirements.txt

# Set up directories and files for WAF
echo "Setting up directories and files..."

# Create the directories if they don't exist
mkdir -p app logs

# Create empty JSON files if they don't exist
touch waf_logs.json
touch waf_rules.json

# Set up file permissions (optional)
echo "Setting file permissions..."
chmod 755 setup.sh
chmod 755 app/

# Give feedback to the user
echo "Setup completed successfully."
echo "You can now run the WAF application using 'python3 app.py'."

# Start the Flask app (optional - you can comment this out if you don't want it to start automatically)
# echo "Starting Flask app..."
# python3 app.py
