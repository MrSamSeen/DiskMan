#!/bin/bash
# DiskMan - Disk Manager by SamSeen
# macOS/Linux launcher script

# Check if the script has executable permissions
if [ ! -x "$0" ]; then
    echo "This script doesn't have executable permissions."
    echo "Please run: chmod +x DiskMan.sh"
    echo "Then try again."
    read -p "Press Enter to continue..."
    exit 1
fi

echo "Starting DiskMan..."
python3 DiskMan.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error running DiskMan. Please make sure Python 3 is installed."
    echo "You can download Python from https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to continue..."
fi
