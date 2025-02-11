#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo ‘Python3 not found! Please install Python3 first.’
    exit 1
fi

# Create a virtual environment
echo ‘Creating a virtual environment...’
python3 -m venv venv

# Activate the virtual environment
echo ‘Activating the virtual environment...’
source venv/bin/activate

# Update pip
echo ‘Updating pip...’
pip install --upgrade pip

# Install dependencies from requirements.txt
echo ‘Installing dependencies...’
pip install -r requirements.txt

echo ‘Installation complete! Use ‘source venv/bin/activate’ to activate the virtual environment.’
