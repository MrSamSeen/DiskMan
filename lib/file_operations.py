#!/usr/bin/env python3
"""
File operations for DiskMan.
"""
import os
import shutil
import datetime
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

def delete_item(item_path):
    """Delete a file or directory.

    Args:
        item_path (str): Path to the file or directory to delete

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        if os.path.isdir(item_path):
            # Delete directory and all its contents
            start_spinner(f"Deleting directory: {os.path.basename(item_path)}...")
            shutil.rmtree(item_path)
        else:
            # Delete file
            start_spinner(f"Deleting file: {os.path.basename(item_path)}...")
            os.remove(item_path)

        stop_spinner()
        return True
    except (OSError, PermissionError) as e:
        stop_spinner()
        print(f"{Fore.RED}Error deleting item: {e}{Style.RESET_ALL}")
        return False

def get_item_details(item_path):
    """Get detailed information about a file or directory.

    Args:
        item_path (str): Path to the file or directory

    Returns:
        dict: Dictionary containing item details
    """
    try:
        # Get basic file information
        name = os.path.basename(item_path)
        size = get_size(item_path)
        is_dir = os.path.isdir(item_path)

        # Get file stats
        stats = os.stat(item_path)
        created_time = datetime.datetime.fromtimestamp(stats.st_ctime)
        modified_time = datetime.datetime.fromtimestamp(stats.st_mtime)
        accessed_time = datetime.datetime.fromtimestamp(stats.st_atime)

        details = {
            'name': name,
            'path': item_path,
            'size': size,
            'is_dir': is_dir,
            'created': created_time,
            'modified': modified_time,
            'accessed': accessed_time
        }

        # If it's a directory, get its contents
        if is_dir:
            try:
                contents = []
                for i, item in enumerate(os.listdir(item_path)):
                    if i >= 20:  # Limit to first 20 items
                        contents.append("... (more items not shown)")
                        break

                    sub_path = os.path.join(item_path, item)
                    sub_is_dir = os.path.isdir(sub_path)
                    sub_size = get_size(sub_path)

                    contents.append({
                        'name': item,
                        'is_dir': sub_is_dir,
                        'size': sub_size
                    })

                details['contents'] = contents
                details['item_count'] = len(os.listdir(item_path))
            except (OSError, PermissionError):
                details['contents'] = ["Error: Unable to access directory contents"]

        return details
    except (OSError, PermissionError) as e:
        print(f"{Fore.RED}Error getting item details: {e}{Style.RESET_ALL}")
        return None
