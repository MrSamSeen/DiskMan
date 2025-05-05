#!/usr/bin/env python3
"""
File operations for DiskMan.
"""
import os
from .utils import get_size, is_hidden, start_spinner, stop_spinner
from colorama import Fore, Style

def list_directory(directory):
    """List all files and directories in the given directory with their sizes."""
    try:
        # Start spinner
        start_spinner(f"Calculating sizes in {os.path.basename(directory)}...")

        # Get all items in the directory
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                size = get_size(item_path)
                is_dir = os.path.isdir(item_path)
                is_hidden_item = is_hidden(item_path)
                items.append((item, size, is_dir, is_hidden_item))
            except (OSError, PermissionError):
                # Skip items that can't be accessed
                pass

        # Sort by size (largest first)
        items.sort(key=lambda x: x[1], reverse=True)

        # Stop spinner
        stop_spinner()

        return items
    except (OSError, PermissionError) as e:
        # Stop spinner if there's an error
        stop_spinner()

        print(f"{Fore.RED}Error accessing directory: {e}{Style.RESET_ALL}")
        return []
