#!/bin/bash
set -e

# Ensure virtual environment is activated if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if server flag is provided
if [ "$1" = "--server" ]; then
    echo "Starting the server..."
    python src/run_server.py
else
    # Run the CLI application
    python src/main.py "$@"
fi
