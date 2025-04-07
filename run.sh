#!/bin/bash

# Exit immediately if any command fails
set -e

# Activate the Python virtual environment
source .venv_shoeprint/bin/activate

# Start the FastAPI backend using uvicorn in the background
echo "Starting backend..."
uvicorn backend.main:app --reload &

# Capture backend process PID so we can manage it if needed
BACKEND_PID=$!

# Wait a couple seconds to ensure backend is ready
sleep 2

# Start the PyQt frontend
echo "Starting frontend..."
python src/app.py

# Optional: Kill backend when frontend exits
echo "Frontend closed. Stopping backend..."
kill $BACKEND_PID
