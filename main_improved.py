#!/usr/bin/env python3
"""
S-Parameter Plotting Tool - Improved Workflow Version
Main entry point with the improved file management workflow.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_manager_window import FileManagerWindow


def main():
    """Main application entry point."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("S-Parameter Plotting Tool")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("RF Visualization")
    
    # Create and show main window
    window = FileManagerWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
