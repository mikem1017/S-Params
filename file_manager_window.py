"""
File Manager Window - Main interface for managing up to 4 files.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QGroupBox, QGridLayout,
                             QMessageBox, QFileDialog, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional, List, Dict
import os
from file_manager import TouchstoneFile
from s_param_selector import SParamSelectorDialog
from plot_window import PlotWindow


class FileManagerWindow(QMainWindow):
    """Main window for managing up to 4 touchstone files."""
    
    def __init__(self):
        super().__init__()
        self.loaded_files = {}  # Dict of slot_id -> TouchstoneFile
        self.selected_s_params = {}  # Dict of slot_id -> list of selected S-params with names
        self.plot_window = None
        
        self.init_ui()
        
        # Set window properties
        self.setWindowTitle("S-Parameter File Manager")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("S-Parameter File Manager")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Load up to 4 touchstone files, then choose which S-parameters to plot from each file.")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # File slots
        files_group = QGroupBox("Files")
        files_layout = QGridLayout()
        files_layout.setSpacing(15)
        
        # Create 4 file slots
        self.file_slots = []
        for i in range(4):
            slot = self.create_file_slot(i)
            self.file_slots.append(slot)
            
            # Add to grid layout (2x2)
            row = i // 2
            col = i % 2
            files_layout.addLayout(slot, row, col)
        
        files_group.setLayout(files_layout)
        main_layout.addWidget(files_group)
        
        # Control buttons
        control_layout = QHBoxLayout()
        control_layout.addStretch()
        
        self.plot_button = QPushButton("Open Plot Window")
        self.plot_button.clicked.connect(self.open_plot_window)
        self.plot_button.setMinimumWidth(150)
        self.plot_button.setMinimumHeight(40)
        control_layout.addWidget(self.plot_button)
        
        self.clear_all_button = QPushButton("Clear All Files")
        self.clear_all_button.clicked.connect(self.clear_all_files)
        control_layout.addWidget(self.clear_all_button)
        
        main_layout.addLayout(control_layout)
        
        # Status
        self.status_label = QLabel("Ready - Load files and select S-parameters")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
    
    def create_file_slot(self, slot_id: int):
        """Create a file slot widget."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Slot header
        header_label = QLabel(f"File {slot_id + 1}")
        header_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)
        
        # File info
        file_info_label = QLabel("No file loaded")
        file_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_info_label.setWordWrap(True)
        file_info_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(file_info_label)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        load_button = QPushButton("Load File")
        load_button.clicked.connect(lambda: self.load_file(slot_id))
        button_layout.addWidget(load_button)
        
        choose_button = QPushButton("Choose S-Parameters")
        choose_button.clicked.connect(lambda: self.choose_s_params(slot_id))
        choose_button.setEnabled(False)
        button_layout.addWidget(choose_button)
        
        remove_button = QPushButton("Remove File")
        remove_button.clicked.connect(lambda: self.remove_file(slot_id))
        remove_button.setEnabled(False)
        button_layout.addWidget(remove_button)
        
        layout.addLayout(button_layout)
        
        # Store references for updating
        layout.file_info_label = file_info_label
        layout.choose_button = choose_button
        layout.remove_button = remove_button
        
        return layout
    
    def load_file(self, slot_id: int):
        """Load a touchstone file into the specified slot."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            f"Select Touchstone File for Slot {slot_id + 1}",
            "",
            "Touchstone Files (*.s1p *.s2p *.s3p *.s4p);;All Files (*)"
        )
        
        if filepath:
            try:
                # Load the file
                touchstone_file = TouchstoneFile(filepath)
                self.loaded_files[slot_id] = touchstone_file
                
                # Update UI
                slot_layout = self.file_slots[slot_id]
                filename = os.path.basename(filepath)
                slot_layout.file_info_label.setText(f"{filename}\n({len(touchstone_file.s_params)} S-parameters)")
                slot_layout.file_info_label.setStyleSheet("color: black; font-style: normal;")
                
                slot_layout.choose_button.setEnabled(True)
                slot_layout.remove_button.setEnabled(True)
                
                # Clear any previous S-parameter selections for this slot
                self.selected_s_params[slot_id] = []
                
                self.update_status(f"Loaded {filename} with {len(touchstone_file.s_params)} S-parameters")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load file:\n{str(e)}")
    
    def choose_s_params(self, slot_id: int):
        """Open S-parameter selector dialog for the specified slot."""
        if slot_id not in self.loaded_files:
            return
        
        touchstone_file = self.loaded_files[slot_id]
        current_selections = self.selected_s_params.get(slot_id, [])
        
        # Create and show dialog
        dialog = SParamSelectorDialog(touchstone_file, current_selections, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            # Update selections
            self.selected_s_params[slot_id] = dialog.get_selections()
            
            # Update status
            num_selected = len(self.selected_s_params[slot_id])
            filename = os.path.basename(touchstone_file.filepath)
            self.update_status(f"{filename}: {num_selected} S-parameters selected for plotting")
    
    def remove_file(self, slot_id: int):
        """Remove file from the specified slot."""
        if slot_id in self.loaded_files:
            del self.loaded_files[slot_id]
        
        if slot_id in self.selected_s_params:
            del self.selected_s_params[slot_id]
        
        # Update UI
        slot_layout = self.file_slots[slot_id]
        slot_layout.file_info_label.setText("No file loaded")
        slot_layout.file_info_label.setStyleSheet("color: gray; font-style: italic;")
        slot_layout.choose_button.setEnabled(False)
        slot_layout.remove_button.setEnabled(False)
        
        self.update_status("File removed")
    
    def clear_all_files(self):
        """Clear all loaded files."""
        reply = QMessageBox.question(
            self, 'Clear All Files', 
            'Are you sure you want to clear all loaded files?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for slot_id in range(4):
                self.remove_file(slot_id)
            self.update_status("All files cleared")
    
    def open_plot_window(self):
        """Open the plot window with current S-parameter selections."""
        # Collect all selected traces
        traces = []
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        trace_count = 0
        for slot_id, selections in self.selected_s_params.items():
            if slot_id in self.loaded_files and selections:
                touchstone_file = self.loaded_files[slot_id]
                for param_name, legend_name in selections:
                    traces.append({
                        'touchstone_file': touchstone_file,
                        'param_name': param_name,
                        'legend_name': legend_name,
                        'color': colors[trace_count % len(colors)]
                    })
                    trace_count += 1
        
        if not traces:
            QMessageBox.information(self, "No Data", "Please select S-parameters to plot first.")
            return
        
        # Create or update plot window
        if self.plot_window is None or not self.plot_window.isVisible():
            self.plot_window = PlotWindow(self)
            self.plot_window.show()
        
        # Update plot with current data
        self.plot_window.update_plot(traces)
        self.update_status(f"Plot window updated with {len(traces)} traces")
    
    def update_status(self, message: str):
        """Update the status label."""
        self.status_label.setText(message)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Close plot window if it's open
        if self.plot_window and self.plot_window.isVisible():
            self.plot_window.close()
        event.accept()
