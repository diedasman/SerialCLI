#!/bin/bash
# install.sh - Unix/Linux/macOS installation script for SerialCLI
# Usage: bash install.sh

set -e  # Exit on any error

echo ""
echo "============================================================"
echo "SerialCLI - Unix/Linux/macOS Installation Script"
echo "============================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    echo ""
    echo "On Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "On macOS: brew install python3"
    echo "On Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

echo "Detected Python installation:"
python3 --version
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Installing pip..."
    python3 -m ensurepip --upgrade || {
        echo "Failed to install pip. Please install manually:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
        echo "  macOS: brew install python3"
        exit 1
    }
fi

# Upgrade pip, setuptools, and wheel
echo "Upgrading pip and related tools..."
pip3 install --upgrade pip setuptools wheel

# Install requirements
echo ""
echo "Installing required packages..."
pip3 install pyserial

# Install SerialCLI in development mode
echo ""
echo "Installing SerialCLI..."
pip3 install -e .

echo ""
echo "============================================================"
echo "✓ Installation completed successfully!"
echo "============================================================"
echo ""
echo "You can now run SerialCLI from anywhere in your terminal:"
echo "  SerialCLI"
echo ""
echo "For first-run help, use:"
echo "  SerialCLI"
echo "  SerialCLI> help"
echo ""
