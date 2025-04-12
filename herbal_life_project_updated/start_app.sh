#!/bin/bash

echo "Herbal Life - Ayurvedic Wellness Platform"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please make sure Python 3 is installed."
        read -p "Press Enter to continue..."
        exit 1
    fi
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install flask flask-login flask-sqlalchemy flask-wtf email-validator
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    read -p "Press Enter to continue..."
    exit 1
fi

# Run the application
echo "Starting the application..."
python run.py
if [ $? -ne 0 ]; then
    echo "Application exited with an error."
    read -p "Press Enter to continue..."
    exit 1
fi

read -p "Press Enter to continue..."