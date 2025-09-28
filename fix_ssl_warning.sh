#!/bin/bash

# Deactivate any active virtual environment first
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Deactivating current virtual environment..."
    deactivate
fi

# Navigate to project directory
cd "$(dirname "$0")"

echo "Current directory: $(pwd)"

# Option 1: Just fix urllib3 in the current environment
if [[ "$1" == "--quick" ]]; then
    echo "Performing quick fix (just updating urllib3)..."
    source .venv/bin/activate
    pip install urllib3==1.26.18
    echo "Done! urllib3 has been downgraded to a version compatible with LibreSSL."
    exit 0
fi

# Option 2: Full rebuild of virtual environment
echo "Rebuilding virtual environment completely..."

# Remove the old virtual environment
echo "Removing old virtual environment..."
rm -rf .venv

# Create a new virtual environment with the correct Python version
echo "Creating new virtual environment..."
python3 -m venv .venv

# Activate the new virtual environment
echo "Activating new virtual environment..."
source .venv/bin/activate

# Update pip and setuptools
echo "Updating pip and setuptools..."
pip install --upgrade pip setuptools

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Double-check urllib3 version
echo "Verifying urllib3 version..."
pip show urllib3

echo "Installation complete! The SSL warning should be resolved."
echo "You can now run your application: python src/python/kairos_ai.py"