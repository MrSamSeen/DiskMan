#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import time
import itertools
from pathlib import Path

# Check if required packages are installed
try:
    import humanize
except ImportError:
    print("The 'humanize' package is required. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "humanize"])
    import humanize

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Initialize colorama
except ImportError:
    print("The 'colorama' package is required for colored output. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Initialize colorama

# Global variable to control the spinner
spinner_running = False

def show_spinner(message):
    """Display a spinner with a message while a task is running."""
    global spinner_running
    spinner_running = True
    spinner_chars = itertools.cycle(['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'])

    # Clear line and show initial message
    sys.stdout.write('\r' + ' ' * 80)  # Clear line
    sys.stdout.write(f"\r{Fore.CYAN}{message} {Fore.YELLOW}")
    sys.stdout.flush()

    while spinner_running:
        char = next(spinner_chars)
        sys.stdout.write(f"\r{Fore.CYAN}{message} {Fore.YELLOW}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)

    # Clear spinner when done
    sys.stdout.write('\r' + ' ' * 80)
    sys.stdout.write(f"\r{Fore.GREEN}✓ {message} completed!{Style.RESET_ALL}\n")
    sys.stdout.flush()

def get_size(path):
    """Calculate the size of a file or directory."""
    if os.path.isfile(path):
        return os.path.getsize(path)

    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):  # Skip symbolic links
                try:
                    total_size += os.path.getsize(fp)
                except (OSError, PermissionError):
                    pass  # Skip files that can't be accessed
    return total_size

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
                is_hidden = item.startswith('.') or (os.name == 'nt' and os.stat(item_path).st_file_attributes & 2)
                items.append((item, size, is_dir, is_hidden))
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
    os.system('cls' if os.name == 'nt' else 'clear')

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
            name_color = Fore.CYAN # Cyan for hidden directories (more readable than dimmed blue)
            type_color = Fore.MAGENTA
        elif is_dir:
            item_type = "Directory"
            name_color = Fore.CYAN + Style.BRIGHT  # Bright blue for normal directories
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

        # Add a visual indicator for hidden files/folders
        hidden_indicator = " " if is_hidden else ""

        # Print item with colors
        print(f"{Fore.YELLOW}{i:<4} {name_color}{hidden_indicator}{display_name:<38} {size_color}{size_str:<15} {percentage_color}{percentage_str:<8} {type_color}{item_type:<10}{Style.RESET_ALL}")

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

def show_welcome_message():
    """Display a welcome message when the program starts."""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

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

def main():
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

        # Show navigation options with colors
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
                try:
                    # Use the appropriate command based on the OS
                    if sys.platform == 'darwin':  # macOS
                        # On macOS, we can use the -R flag to reveal the item in Finder
                        subprocess.run(['open', '-R', item_path])
                        print(f"\n{Fore.GREEN}Opened parent folder with {Fore.YELLOW}{name}{Fore.GREEN} highlighted in Finder{Style.RESET_ALL}")
                    elif sys.platform == 'win32':  # Windows
                        # On Windows, we can use explorer /select to highlight the item
                        subprocess.run(['explorer', '/select,', item_path])
                        print(f"\n{Fore.GREEN}Opened parent folder with {Fore.YELLOW}{name}{Fore.GREEN} highlighted in Explorer{Style.RESET_ALL}")
                    else:  # Linux and others
                        # For Linux, we'll just open the parent directory
                        # Most file managers don't have a standard way to highlight items
                        parent_dir = os.path.dirname(item_path)
                        subprocess.run(['xdg-open', parent_dir])
                        print(f"\n{Fore.GREEN}Opened parent folder of {Fore.YELLOW}{name}{Fore.GREEN} in file manager{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}Note: {Fore.WHITE}You'll need to locate {Fore.YELLOW}{name}{Fore.WHITE} manually{Style.RESET_ALL}")

                    # Add a small delay to make sure the file/folder opens
                    print(f"{Fore.CYAN}The file explorer should now be open.{Style.RESET_ALL}")
                    input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"\n{Fore.RED}Error opening parent folder: {e}{Style.RESET_ALL}")
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
