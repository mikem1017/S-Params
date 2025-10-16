"""
Plot Window for displaying S-parameter plots.
"""
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QMenuBar, QStatusBar, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence
import matplotlib
matplotlib.use('QtAgg')

from plot_engine import PlotEngine
from plot_controls import PlotControlsWidget


class PlotWindow(QMainWindow):
    """Dedicated window for displaying plots."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plot_engine = PlotEngine()
        
        self.init_ui()
        
        # Set window properties
        self.setWindowTitle("S-Parameter Plot")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Use default Qt styling - no custom colors
        pass
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left side - Plot area
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.plot_engine.canvas)
        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        main_layout.addWidget(plot_widget, 3)  # 75% of space
        
        # Right side - Controls
        self.plot_controls = PlotControlsWidget()
        main_layout.addWidget(self.plot_controls, 1)  # 25% of space
        
        # Connect signals
        self.plot_controls.plot_type_changed.connect(self.on_plot_type_changed)
        self.plot_controls.config_changed.connect(self.on_config_changed)
        
        # NOTE: Export buttons removed from plot controls to prevent double save dialogs
        # Use File menu for saving instead
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Load files from File Manager")
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Export actions
        export_png_action = QAction('Export PNG...', self)
        export_png_action.triggered.connect(self.export_png)
        file_menu.addAction(export_png_action)
        
        export_pdf_action = QAction('Export PDF...', self)
        export_pdf_action.triggered.connect(self.export_pdf)
        file_menu.addAction(export_pdf_action)
        
        export_svg_action = QAction('Export SVG...', self)
        export_svg_action.triggered.connect(self.export_svg)
        file_menu.addAction(export_svg_action)
        
        file_menu.addSeparator()
        
        # Close action
        close_action = QAction('Close', self)
        close_action.setShortcut(QKeySequence.StandardKey.Close)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def update_plot(self, traces, plot_type=None):
        """Update the plot with new trace data."""
        if plot_type is None:
            plot_type = self.plot_controls.get_plot_type()
        
        self.plot_engine.plot(plot_type, traces)
        if traces:
            self.status_bar.showMessage(f"Plot updated with {len(traces)} traces")
        else:
            self.status_bar.showMessage("No traces to plot")
    
    def on_plot_type_changed(self, plot_type):
        """Handle plot type change."""
        # Re-plot with current data (traces should be stored in plot_engine)
        self.plot_engine.plot(plot_type, getattr(self.plot_engine, 'last_traces', []))
    
    def on_config_changed(self, config):
        """Handle plot configuration change."""
        self.plot_engine.update_config(config)
        # Re-plot with current data
        plot_type = self.plot_controls.get_plot_type()
        self.plot_engine.plot(plot_type, getattr(self.plot_engine, 'last_traces', []))
    
    def export_png(self):
        """Export plot as PNG."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Plot as PNG", "s_parameter_plot.png", "PNG Files (*.png)"
        )
        if filepath:
            try:
                self.plot_engine.save_plot(filepath, dpi=300)
                self.status_bar.showMessage(f"Plot saved as PNG: {os.path.basename(filepath)}")
                QMessageBox.information(self, "Success", f"Plot saved successfully as:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save plot:\n{str(e)}")
    
    def export_pdf(self):
        """Export plot as PDF."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Plot as PDF", "s_parameter_plot.pdf", "PDF Files (*.pdf)"
        )
        if filepath:
            try:
                self.plot_engine.save_plot(filepath, dpi=300)
                self.status_bar.showMessage(f"Plot saved as PDF: {os.path.basename(filepath)}")
                QMessageBox.information(self, "Success", f"Plot saved successfully as:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save plot:\n{str(e)}")
    
    def export_svg(self):
        """Export plot as SVG."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Plot as SVG", "s_parameter_plot.svg", "SVG Files (*.svg)"
        )
        if filepath:
            try:
                self.plot_engine.save_plot(filepath, dpi=300)
                self.status_bar.showMessage(f"Plot saved as SVG: {os.path.basename(filepath)}")
                QMessageBox.information(self, "Success", f"Plot saved successfully as:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save plot:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About S-Parameter Plot Window",
            """
            <h3>S-Parameter Plot Window</h3>
            <p>Dedicated window for displaying S-parameter plots.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Multiple plot types: Magnitude, Phase, Smith Chart, VSWR, Group Delay</li>
            <li>Customizable plot configuration</li>
            <li>Export plots as PNG, PDF, or SVG</li>
            </ul>
            <p>Use the File Manager to load touchstone files and configure traces.</p>
            """
        )
