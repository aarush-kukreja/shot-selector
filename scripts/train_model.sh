#!/bin/bash
set -e

# Ensure virtual environment is activated if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the training script
python src/models/train.py
