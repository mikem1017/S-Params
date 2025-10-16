"""
Main Window for the S-Parameter plotting application.
"""
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QSplitter, QStatusBar, QMessageBox, QMenuBar, 
                             QFileDialog, QApplication, QScrollArea, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence
import matplotlib
matplotlib.use('QtAgg')  # Use Qt backend for matplotlib

from file_manager import FileManager
from plot_engine import PlotEngine
from ui_components import FileSlotWidget, PlotControlsWidget


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.file_manager = FileManager()
        self.plot_engine = PlotEngine()
        self.file_slots = []
        self.traces = []  # List of active traces for plotting
        
        self.init_ui()
        self.setup_connections()
        
        # Set window properties
        self.setWindowTitle("S-Parameter Plotting Tool")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
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
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - File slots
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Center panel - Plot area
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)
        
        # Right panel - Plot controls
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (25% left, 55% center, 20% right)
        splitter.setSizes([400, 880, 320])
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def create_left_panel(self):
        """Create the left panel with file slots."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Title
        title = QWidget()
        title_layout = QVBoxLayout(title)
        title_label = QWidget()
        title_label_layout = QVBoxLayout(title_label)
        title_label_layout.addWidget(QLabel("File Loading"))
        title_label_layout.addWidget(QLabel("(Up to 4 files)"))
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addWidget(title)
        
        # File slots
        for i in range(4):
            slot = FileSlotWidget(i)
            self.file_slots.append(slot)
            layout.addWidget(slot)
        
        layout.addStretch()
        return panel
    
    def create_center_panel(self):
        """Create the center panel with plot area."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Add plot canvas
        layout.addWidget(self.plot_engine.canvas)
        
        return panel
    
    def create_right_panel(self):
        """Create the right panel with plot controls."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Add plot controls
        self.plot_controls = PlotControlsWidget()
        layout.addWidget(self.plot_controls)
        
        layout.addStretch()
        return panel
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # New action
        new_action = QAction('New', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip('Clear all files')
        new_action.triggered.connect(self.clear_all_files)
        file_menu.addAction(new_action)
        
        # Open action
        open_action = QAction('Open Files...', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip('Open touchstone files')
        open_action.triggered.connect(self.open_files)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.setStatusTip('About S-Parameter Plotting Tool')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_connections(self):
        """Set up signal connections."""
        # Connect file slot signals
        for slot in self.file_slots:
            slot.file_loaded.connect(self.on_file_loaded)
            slot.file_removed.connect(self.on_file_removed)
            slot.param_changed.connect(self.on_param_changed)
            slot.legend_changed.connect(self.on_legend_changed)
            slot.enabled_changed.connect(self.on_enabled_changed)
        
        # Connect plot control signals
        self.plot_controls.plot_type_changed.connect(self.on_plot_type_changed)
        self.plot_controls.config_changed.connect(self.on_config_changed)
    
    def on_file_loaded(self, slot_id: int, filepath: str):
        """Handle file loaded signal."""
        try:
            self.file_manager.load_file(slot_id, filepath)
            self.update_plot()
            self.status_bar.showMessage(f"Loaded file: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
    
    def on_file_removed(self, slot_id: int):
        """Handle file removed signal."""
        self.file_manager.remove_file(slot_id)
        self.update_plot()
        self.status_bar.showMessage("File removed")
    
    def on_param_changed(self, slot_id: int, param_name: str):
        """Handle parameter change signal."""
        self.update_plot()
    
    def on_legend_changed(self, slot_id: int, legend_name: str):
        """Handle legend name change signal."""
        self.update_plot()
    
    def on_enabled_changed(self, slot_id: int, enabled: bool):
        """Handle enable/disable signal."""
        self.update_plot()
    
    def on_plot_type_changed(self, plot_type: str):
        """Handle plot type change signal."""
        self.update_plot()
    
    def on_config_changed(self, config: dict):
        """Handle plot configuration change signal."""
        self.plot_engine.update_config(config)
        self.update_plot()
    
    def update_plot(self):
        """Update the plot with current data."""
        # Collect active traces
        self.traces = []
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        for i, slot in enumerate(self.file_slots):
            trace_data = slot.get_trace_data()
            if trace_data:
                trace_data['color'] = colors[i % len(colors)]
                self.traces.append(trace_data)
        
        # Update plot
        plot_type = self.plot_controls.get_plot_type()
        self.plot_engine.plot(plot_type, self.traces)
    
    def clear_all_files(self):
        """Clear all loaded files."""
        reply = QMessageBox.question(
            self, 'Clear All Files', 
            'Are you sure you want to clear all loaded files?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for slot in self.file_slots:
                slot.remove_file()
            self.file_manager.clear_all()
            self.update_plot()
            self.status_bar.showMessage("All files cleared")
    
    def open_files(self):
        """Open multiple files at once."""
        filepaths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Touchstone Files",
            "",
            "Touchstone Files (*.s1p *.s2p *.s3p *.s4p);;All Files (*)"
        )
        
        if filepaths:
            # Load files into available slots
            for i, filepath in enumerate(filepaths[:4]):  # Max 4 files
                if i < len(self.file_slots):
                    self.file_slots[i].load_file(filepath)
            
            self.status_bar.showMessage(f"Loaded {len(filepaths)} files")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About S-Parameter Plotting Tool",
            """
            <h3>S-Parameter Plotting Tool</h3>
            <p>A modern desktop application for visualizing S-parameter data from touchstone files.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Load up to 4 touchstone files (.s1p to .s4p)</li>
            <li>Multiple plot types: Magnitude, Phase, Smith Chart, VSWR, Group Delay</li>
            <li>Customizable legends and plot configuration</li>
            <li>Export plots as PNG, PDF, or SVG</li>
            </ul>
            <p>Built with PyQt6, scikit-rf, and matplotlib.</p>
            """
        )
    
    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(
            self, 'Exit Application',
            'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
