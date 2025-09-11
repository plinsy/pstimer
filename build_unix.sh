#!/bin/bash

echo "PSTimer Build Script for macOS/Linux"
echo "===================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.7 or higher."
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the PSTimer directory."
    exit 1
fi

# Check if PyInstaller is available, install if not
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Run the build script
echo "Running build script..."
python3 build_dist.py

echo
echo "Build complete! Check the generated files."

# Make executable on Unix systems
if [ -f "dist/PSTimer" ]; then
    chmod +x "dist/PSTimer"
    echo "Made PSTimer executable."
fi
