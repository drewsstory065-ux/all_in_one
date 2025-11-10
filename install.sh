#!/bin/bash

# Check if all required tools are already installed
if command -v python3 &> /dev/null && command -v pip3 &> /dev/null && python3 -c "import PyQt6" &> /dev/null; then
    echo "All required tools (Python3, pip3, PyQt6) are already installed."
    exit 0
fi

# Update package list once at the beginning to avoid redundant updates
sudo apt update

# Check for Python3
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Installing Python3..."
    sudo apt install -y python3
else
    echo "Python3 is already installed."
fi

# Check for pip3
if ! command -v pip3 &> /dev/null; then
    echo "pip3 could not be found. Installing pip3..."
    sudo apt install -y python3-pip
else
    echo "pip3 is already installed."
fi

# Check for PyQt6
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo "PyQt6 is not installed. Installing PyQt6..."
    pip3 install PyQt6
else
    echo "PyQt6 is already installed."
fi

