#!/bin/bash

# Set the path to your virtual environment
VENV_PATH="linkShortner/bin/activate"

# Check if the virtual environment exists
if [ -f "$VENV_PATH" ]; then
    # Activate the virtual environment
    source "$VENV_PATH"

    # Start three instances of uvicorn with different ports
    docker run -p 7000:8080 -v ./data/:/app/data/ link-shortener-devops &
    docker run -p 7001:8080 -v ./data/:/app/data/ link-shortener-devops &
    docker run -p 7002:8080 -v ./data/:/app/data/ link-shortener-devops &

    # Wait for all instances to finish
    wait
else
    echo "Virtual environment not found at $VENV_PATH. Please verify the path."
fi


