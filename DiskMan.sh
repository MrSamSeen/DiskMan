#!/bin/bash
# DiskMan - Disk Manager by SamSeen
# macOS/Linux launcher script

echo "Starting DiskMan..."
python3 DiskMan.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error running DiskMan. Please make sure Python 3 is installed."
    echo "You can download Python from https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to continue..."
fi
