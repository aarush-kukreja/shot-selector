#!/bin/bash
set -e

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS system"
    
    # Check if homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        exit 1
    fi
    
    # Install Python 3.9 if not already installed
    if ! command -v python3.9 &> /dev/null; then
        echo "Installing Python 3.9 via Homebrew..."
        brew install python@3.9
    fi
fi

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment with Python 3.9
echo "Creating new virtual environment..."
python3.9 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip within the virtual environment
echo "Upgrading pip..."
python3.9 -m pip install --upgrade pip

# Install basic requirements first
echo "Installing basic requirements..."
python3.9 -m pip install wheel setuptools numpy

# Install package in development mode with all dependencies
echo "Installing package and dependencies..."
python3.9 -m pip install -e ".[dev]"

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models
mkdir -p logs

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/*.sh

# Create sample training data with more examples
echo "Creating sample training data..."
echo "prompt_text,optimal_strategy
What is the capital of France?,zero-shot
Translate 'hello' to Spanish,zero-shot
What is 2+2?,zero-shot
What color is the sky?,zero-shot
What is the chemical symbol for gold?,zero-shot
Who wrote Romeo and Juliet?,zero-shot
What is the speed of light?,zero-shot
What is the largest planet in our solar system?,zero-shot
Generate a recipe for chocolate chip cookies,one-shot
Write a formal email requesting time off,one-shot
Create a marketing tagline for a coffee shop,one-shot
Write a haiku about nature,one-shot
Compose a tweet about AI technology,one-shot
Write a product description for headphones,one-shot
Create a job posting for a software developer,one-shot
Write a movie review for an action film,one-shot
Design a workout routine for beginners,two-shot
Write a business proposal for a startup,two-shot
Create a lesson plan for teaching math,two-shot
Write a technical documentation for an API,two-shot
Develop a social media content calendar,two-shot
Create a financial budget template,two-shot
Design a customer survey questionnaire,two-shot
Write a research paper outline,two-shot
Create a comprehensive marketing strategy,three-shot
Develop a project management plan,three-shot
Write a detailed business case study,three-shot
Create an employee training program,three-shot
Design a complex software architecture,three-shot
Develop a crisis management protocol,three-shot
Create a strategic five-year business plan,three-shot
Write a comprehensive research methodology,three-shot" > data/raw/training_data.csv

# Download required NLTK data
echo "Downloading NLTK data..."
python3.9 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

echo "Setup completed successfully!"
