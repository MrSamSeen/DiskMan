#!/usr/bin/env python3
"""
User interface functions for DiskMan.
"""
import os
import sys
import time
import humanize
from colorama import Fore, Style
from .utils import clear_screen

def display_directory(directory, items, page=0, items_per_page=20):
    """Display the directory contents with sizes, paginated."""
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # Ceiling division

    # Ensure page is within valid range
    page = max(0, min(page, total_pages - 1)) if total_pages > 0 else 0

    # Calculate start and end indices for current page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)

    # Get items for current page
    page_items = items[start_idx:end_idx]

    # Clear screen
    clear_screen()

    # Display header with colors
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Current directory: {Fore.YELLOW}{directory}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Showing items {Fore.WHITE}{start_idx + 1}-{end_idx} {Fore.CYAN}of {Fore.WHITE}{total_items} {Fore.CYAN}(Page {Fore.WHITE}{page + 1} {Fore.CYAN}of {Fore.WHITE}{total_pages or 1}{Fore.CYAN}){Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'-' * 100}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}{'#':<4} {'Name':<40} {'Size':<15} {'%':<8} {'Type':<10}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'-' * 100}{Style.RESET_ALL}")

    total_size = sum(item[1] for item in items) if items else 0

    for i, (name, size, is_dir, is_hidden) in enumerate(page_items, start_idx + 1):
        # Truncate long filenames
        if len(name) > 37:
            display_name = name[:34] + "..."
        else:
            display_name = name

        size_str = humanize.naturalsize(size)

        # Set colors based on item type and if it's hidden
        if is_dir and is_hidden:
            item_type = "Directory"
            name_color = Fore.CYAN  # Cyan for hidden directories (more readable than dimmed blue)
            type_color = Fore.MAGENTA
        elif is_dir:
            item_type = "Directory"
            name_color = Fore.CYAN + Style.BRIGHT  # Bright cyan for normal directories
            type_color = Fore.MAGENTA
        elif is_hidden:
            item_type = "File"
            name_color = Fore.WHITE  # White for hidden files (more readable than dimmed)
            type_color = Fore.YELLOW + Style.DIM  # Slightly dimmed type indicator instead
        else:
            item_type = "File"
            name_color = Fore.WHITE + Style.BRIGHT  # Bright white for normal files
            type_color = Fore.YELLOW

        # Calculate percentage of total size and set color based on percentage
        percentage = (size / total_size * 100) if total_size > 0 else 0
        if percentage > 10:
            percentage_color = Fore.RED
            size_color = Fore.RED
        elif percentage > 5:
            percentage_color = Fore.YELLOW
            size_color = Fore.YELLOW
        else:
            percentage_color = Fore.GREEN
            size_color = Fore.GREEN
        percentage_str = f"{percentage:.1f}%"

        # Print item with colors
        print(f"{Fore.YELLOW}{i:<4} {name_color}{display_name:<40} {size_color}{size_str:<15} {percentage_color}{percentage_str:<8} {type_color}{item_type:<10}{Style.RESET_ALL}")

    print(f"{Fore.BLUE}{'-' * 100}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total size: {Fore.YELLOW}{humanize.naturalsize(total_size)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total items: {Fore.YELLOW}{total_items}{Style.RESET_ALL}")

    # Show pagination info if there are multiple pages
    if total_pages > 1:
        print(f"{Fore.CYAN}Viewing page {Fore.WHITE}{page + 1} {Fore.CYAN}of {Fore.WHITE}{total_pages}{Style.RESET_ALL}")
        if page > 0:
            print(f"{Fore.CYAN}Use '{Fore.WHITE}p{Fore.CYAN}' for previous page{Style.RESET_ALL}")
        if page < total_pages - 1:
            print(f"{Fore.CYAN}Use '{Fore.WHITE}n{Fore.CYAN}' for next page{Style.RESET_ALL}")

def show_navigation_options(current_page, total_pages):
    """Display navigation options."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Navigation options:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}number{Fore.CYAN}: Navigate to item by number (1, 2, 3, ...){Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}o number{Fore.CYAN}: Open parent folder and highlight item (e.g., 'o 1'){Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}g path{Fore.CYAN} : Go to specific directory (e.g., 'g /Users/Documents'){Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}..{Fore.CYAN}    : Go up one level{Style.RESET_ALL}")
    if current_page > 0:
        print(f"  {Fore.YELLOW}p{Fore.CYAN}     : Previous page{Style.RESET_ALL}")
    if current_page < total_pages - 1:
        print(f"  {Fore.YELLOW}n{Fore.CYAN}     : Next page{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}q{Fore.CYAN}     : Quit{Style.RESET_ALL}")

def show_welcome_message():
    """Display a welcome message when the program starts."""
    # Clear screen
    clear_screen()

    # Get current directory
    current_dir = os.getcwd()

    # Display welcome message
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'Welcome to DiskMan (Disk Manager) by SamSeen':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}DiskMan helps you visualize and manage disk space usage.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Features:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• {Fore.WHITE}View file and folder sizes sorted by largest first{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• {Fore.WHITE}Navigate through directories and explore your file system{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• {Fore.WHITE}Open files and folders directly from the program{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• {Fore.WHITE}Paginated display for better navigation{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}{Style.RESET_ALL}")

    # Ask for starting directory
    print(f"\n{Fore.CYAN}Enter a directory path to start, or press Enter to use current directory:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Current directory: {Fore.YELLOW}{current_dir}{Style.RESET_ALL}")
    user_dir = input(f"{Fore.YELLOW}> {Style.RESET_ALL}").strip()

    if user_dir:
        # User provided a directory
        if os.path.isdir(user_dir):
            return os.path.abspath(user_dir)
        else:
            print(f"\n{Fore.RED}Directory not found: {user_dir}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Using current directory instead.{Style.RESET_ALL}")
            time.sleep(1.5)  # Give user time to read the message
            return current_dir
    else:
        # Use current directory
        return current_dir
