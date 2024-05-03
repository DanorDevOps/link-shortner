#!/bin/bash

# Set the path to your virtual environment
VENV_PATH="link-shortner/bin/activate"

# Check if the virtual environment exists
if [ -f "$VENV_PATH" ]; then
    # Activate the virtual environment
    source "$VENV_PATH"

    # Start three instances of uvicorn with different ports
    uvicorn main:app --port 8000 &
    uvicorn main:app --port 8001 &
    uvicorn main:app --port 8002 &

    # Wait for all instances to finish
    wait
else
    echo "Virtual environment not found at $VENV_PATH. Please verify the path."
fi


