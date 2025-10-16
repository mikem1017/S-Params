#!/usr/bin/env python3
"""
S-Parameter Plotting Tool - Separate Windows Version
Main entry point with separate file manager and plot windows.
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_selector_dialog import FileSelectorDialog
from plot_window import PlotWindow


class SParamApp:
    """Main application class managing separate windows."""
    
    def __init__(self):
        self.app = None
        self.file_dialog = None
        self.plot_window = None
    
    def run(self):
        """Run the application."""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("S-Parameter Plotting Tool")
        self.app.setApplicationVersion("1.0")
        self.app.setOrganizationName("RF Visualization")
        
        # Create file selector dialog
        self.file_dialog = FileSelectorDialog()
        
        # Create plot window
        self.plot_window = PlotWindow(self.file_dialog)
        
        # Connect signals
        self.file_dialog.files_updated.connect(self.plot_window.update_plot)
        
        # Show both windows
        self.file_dialog.show()
        self.plot_window.show()
        
        # Set up window references for communication
        self.file_dialog.plot_window = self.plot_window
        self.plot_window.file_dialog = self.file_dialog
        
        # Start event loop
        sys.exit(self.app.exec())


def main():
    """Main application entry point."""
    try:
        app = SParamApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
