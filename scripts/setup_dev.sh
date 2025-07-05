#!/bin/bash

# Development setup script for AsciiDoc Generator
# This script helps set up the development environment

set -e

echo "Setting up AsciiDoc Generator development environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is required but not installed."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

# Check for required external tools
echo "Checking for required external tools..."

missing_tools=()

if ! command -v asciidoctor &> /dev/null; then
    missing_tools+=("asciidoctor")
fi

if ! command -v pandoc &> /dev/null; then
    missing_tools+=("pandoc")
fi

if ! command -v libreoffice &> /dev/null && ! command -v loffice &> /dev/null; then
    missing_tools+=("libreoffice")
fi

if [ ${#missing_tools[@]} -ne 0 ]; then
    echo "Warning: The following required tools are missing:"
    for tool in "${missing_tools[@]}"; do
        echo "  - $tool"
    done
    echo ""
    echo "Please install these tools before using the AsciiDoc Generator."
    echo "See README.asc for installation instructions."
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/generate.sh
chmod +x scripts/clean_template.sh
chmod +x scripts/parse.py
chmod +x scripts/style.py
chmod +x scripts/template.py

# Test the installation
echo "Testing the installation..."
if make all; then
    echo ""
    echo "✅ Development environment setup completed successfully!"
    echo "You can now use the AsciiDoc Generator."
    echo ""
    echo "Try running: make all"
else
    echo ""
    echo "❌ Setup completed but test failed."
    echo "Please check the error messages above and ensure all dependencies are installed."
    exit 1
fi
