#!/usr/bin/env python3
"""
File operations for DiskMan.
"""
import os
import threading
from .utils import get_size, spinner_running, show_spinner, is_hidden
from colorama import Fore, Style

def list_directory(directory):
    """List all files and directories in the given directory with their sizes."""
    global spinner_running
    
    try:
        # Start spinner in a separate thread
        spinner_thread = threading.Thread(target=show_spinner, args=(f"Calculating sizes in {os.path.basename(directory)}...",))
        spinner_thread.daemon = True
        spinner_thread.start()
        
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
        spinner_running = False
        spinner_thread.join()
        
        return items
    except (OSError, PermissionError) as e:
        # Stop spinner if there's an error
        spinner_running = False
        if 'spinner_thread' in locals() and spinner_thread.is_alive():
            spinner_thread.join()
        
        print(f"{Fore.RED}Error accessing directory: {e}{Style.RESET_ALL}")
        return []
