# DiskMan - Disk Space Management Tool

![DiskMan Logo](https://img.shields.io/badge/DiskMan-Disk%20Space%20Management-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

**DiskMan** is a powerful, interactive disk space analyzer and management tool that helps you visualize and manage your storage usage. With its colorful, user-friendly interface, DiskMan makes it easy to identify large files and folders that are consuming your valuable disk space.

## 🔍 Features

- **Visual Disk Space Analysis**: Quickly identify which files and folders are taking up the most space
- **Size-Based Sorting**: Files and folders are automatically sorted by size (largest first)
- **Color-Coded Interface**: Different colors for directories, files, and size percentages
- **Hidden File Support**: Includes hidden files and folders in the analysis
- **Interactive Navigation**: Browse through your file system directly from the application
- **File Explorer Integration**: Open files and folders in your system's file explorer
- **Smart File Management**: Delete files and folders with user-friendly confirmation (case-insensitive, ignores spaces and special characters)
- **Pagination**: Navigate through large directories with ease using pagination
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.6 or higher
- Required Python packages (automatically installed if missing):
  - colorama
  - humanize

## 🚀 Installation

### Option 1: Clone the Repository

```bash
git clone https://github.com/mrsamseen/DiskMan.git
cd DiskMan
```

### Option 2: Download ZIP

1. Download the ZIP file from the [GitHub repository](https://github.com/mrsamseen/DiskMan)
2. Extract the contents to a folder of your choice
3. Open a terminal/command prompt and navigate to the extracted folder

## 💻 Usage

### Windows

Double-click on `DiskMan.bat` or run from Command Prompt:

```bash
DiskMan.bat
```

### macOS/Linux

First, make the shell script executable:

```bash
chmod +x DiskMan.sh
```

Then run the shell script:

```bash
./DiskMan.sh
```

Or make the Python script executable and run it directly:

```bash
chmod +x DiskMan.py
./DiskMan.py
```

Alternatively, run with Python:

```bash
python3 DiskMan.py
```

### Navigation Commands

- **number**: Navigate to item by number (e.g., `1`, `2`, `3`)
- **o number**: Open parent folder and highlight item (e.g., `o 1`)
- **d number**: Delete file or folder with smart confirmation (e.g., `d 1`)
- **g path**: Go to specific directory (e.g., `g /Users/Documents`)
- **..**: Go up one level
- **p**: Previous page (when pagination is active)
- **n**: Next page (when pagination is active)
- **q**: Quit the program

## 🖼️ Screenshots

![Screenshot 1](src/Screenshot%201.jpg)

![Screenshot 2](src/Screenshot%202.jpg)

![Screenshot 3](src/Screenshot%203.jpg)

## 🗑️ Smart Deletion Confirmation

DiskMan includes a user-friendly file deletion system with smart confirmation:

1. When you select a file/folder to delete (using `d number`), you'll see detailed information about the item
2. A confirmation prompt will show the text you need to type to confirm deletion
3. The confirmation text is:
   - Automatically converted to lowercase
   - Spaces and special characters are removed
   - Based on the first 10 characters of the file/folder name
4. Your input is processed the same way, making confirmation easier and more forgiving
5. Type `c` to cancel the deletion at any time

For example:

- For a file named "My Document.txt", you can type "mydocument" (lowercase, no spaces)
- For a file named "Report-2023_final.pdf", you can type "report2023" (lowercase, no special characters)

This makes the deletion process more convenient while still requiring deliberate confirmation.

## 🔧 Customization

You can customize DiskMan by modifying the following files:

- `lib/ui.py`: Change colors, layout, and display options
- `DiskMan.py`: Modify core functionality and behavior
- `lib/utils.py`: Adjust utility functions and helpers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [colorama](https://pypi.org/project/colorama/) for cross-platform colored terminal text
- [humanize](https://pypi.org/project/humanize/) for human-readable file sizes

## 🔍 Keywords

disk space analyzer, storage management, file size visualization, disk cleanup tool, python disk utility, storage analyzer, disk space management, file explorer, directory browser, large file finder, disk usage, storage optimization, file management, disk space visualization, python utility, cross-platform disk analyzer, smart deletion, user-friendly file deletion, safe file management

---

Created with ❤️ by [SamSeen](https://github.com/MrSamSeen/)
