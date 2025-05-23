#!/usr/bin/env python3
"""
DiskMan - Disk Manager by SamSeen

A tool to visualize and manage disk space usage.
"""
import os
import sys
import time
from colorama import Fore, Style

# Import modules from lib directory
from lib.utils import open_file_explorer, set_terminal_size, clear_screen
from lib.file_operations import list_directory, delete_item, get_item_details
from lib.ui import display_directory, show_navigation_options, show_welcome_message, show_delete_confirmation

def main():
    """Main function for DiskMan."""
    # Set terminal size to 120x40
    if not set_terminal_size(120, 42):
        # If automatic resizing failed, print a message asking the user to resize manually
        print(f"{Fore.YELLOW}For the best experience, please resize your terminal window to at least 120x40 characters.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        input()
        clear_screen()

    # Add a small delay to give the terminal time to resize
    time.sleep(0.5)

    # Show welcome message and get starting directory
    current_dir = show_welcome_message()

    # Initialize page number
    current_page = 0
    items_per_page = 20

    while True:
        # Check if directory exists
        if not os.path.isdir(current_dir):
            print(f"{Fore.RED}Directory not found: {Fore.YELLOW}{current_dir}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Falling back to home directory...{Style.RESET_ALL}")
            current_dir = os.path.expanduser("~")  # Fallback to home directory
            current_page = 0  # Reset page when changing directory

        # List directory contents
        items = list_directory(current_dir)

        # Calculate total pages
        total_items = len(items)
        total_pages = (total_items + items_per_page - 1) // items_per_page

        # Ensure current_page is valid
        current_page = max(0, min(current_page, total_pages - 1)) if total_pages > 0 else 0

        # Display current page
        display_directory(current_dir, items, current_page, items_per_page)

        # Show navigation options
        show_navigation_options(current_page, total_pages)

        # Get user input
        choice = input(f"\n{Fore.CYAN}Enter your choice: {Fore.YELLOW}").strip().lower()
        print(f"{Style.RESET_ALL}", end="")  # Reset color after input

        if choice == 'q':
            break
        elif choice == '.' or choice == '..' or choice == '...':
            # Go up one level
            parent_dir = os.path.dirname(current_dir)
            if parent_dir != current_dir:  # Prevent getting stuck at root
                current_dir = parent_dir
                current_page = 0  # Reset page when changing directory
        elif choice.startswith('g '):
            # Go to specific directory
            target_dir = choice[2:].strip()
            if os.path.isdir(target_dir):
                current_dir = os.path.abspath(target_dir)
                current_page = 0  # Reset page when changing directory
            else:
                print(f"\n{Fore.RED}Directory not found: {Fore.YELLOW}{target_dir}{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == 'n' and current_page < total_pages - 1:
            # Go to next page
            current_page += 1
        elif choice == 'p' and current_page > 0:
            # Go to previous page
            current_page -= 1
        elif choice.startswith('o ') and choice[2:].strip().isdigit():
            # Open parent folder and highlight the selected item
            index = int(choice[2:].strip()) - 1
            if 0 <= index < total_items:
                name, _, _, _ = items[index]
                item_path = os.path.join(current_dir, name)
                open_file_explorer(item_path, name)
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        elif choice.startswith('d ') and choice[2:].strip().isdigit():
            # Delete file or folder
            index = int(choice[2:].strip()) - 1
            if 0 <= index < total_items:
                name, _, is_dir, _ = items[index]
                item_path = os.path.join(current_dir, name)

                # Get detailed information about the item
                item_details = get_item_details(item_path)

                if item_details:
                    # Show delete confirmation screen
                    if show_delete_confirmation(item_details):
                        # User confirmed deletion
                        if delete_item(item_path):
                            print(f"\n{Fore.GREEN}Successfully deleted {Fore.WHITE}{'directory' if is_dir else 'file'}{Fore.GREEN}: {Fore.YELLOW}{name}{Style.RESET_ALL}")
                        else:
                            print(f"\n{Fore.RED}Failed to delete {Fore.WHITE}{'directory' if is_dir else 'file'}{Fore.RED}: {Fore.YELLOW}{name}{Style.RESET_ALL}")

                        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}Error: Could not get details for {Fore.YELLOW}{name}{Style.RESET_ALL}")
                    input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        elif choice.isdigit():
            # Navigate to selected item
            index = int(choice) - 1
            if 0 <= index < total_items:
                name, _, is_dir, _ = items[index]
                if is_dir:
                    current_dir = os.path.join(current_dir, name)
                    current_page = 0  # Reset page when changing directory
                else:
                    print(f"\n{Fore.GREEN}Selected file: {Fore.YELLOW}{name}{Style.RESET_ALL}")
                    input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Invalid command.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program terminated by user.{Style.RESET_ALL}")
        sys.exit(0)
