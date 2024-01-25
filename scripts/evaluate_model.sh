#!/bin/bash
set -e

# Ensure virtual environment is activated if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the evaluation script
python src/models/evaluate.py
