#!/usr/bin/env python3
"""
S-Parameter Plotting Tool
Main entry point for the application.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_window import MainWindow


def main():
    """Main application entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("S-Parameter Plotting Tool")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("RF Visualization")
    
    # Enable high DPI scaling (PyQt6 handles this automatically)
    # Note: AA_EnableHighDpiScaling is deprecated in PyQt6
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
