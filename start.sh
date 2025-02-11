#!/bin/bash

# Enable virtual environment
echo ‘Activating the virtual environment...’
source venv/bin/activate

# Run the main programme
echo ‘Running the application...’
python3 run.py # Replace ‘main.py’ with your project's main file

# Disable the virtual environment after completion (optional)
deactivate
