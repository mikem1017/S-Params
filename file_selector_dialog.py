"""
File Selection Dialog for managing touchstone files.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QCheckBox,
                             QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QFileDialog, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional, List, Dict
import os
from file_manager import TouchstoneFile


class FileSelectorDialog(QDialog):
    """Dialog for selecting and configuring touchstone files."""
    
    files_updated = pyqtSignal(list)  # Emit list of trace data
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.traces = []  # List of active traces
        self.loaded_files = {}  # Dict of file_id -> TouchstoneFile
        self.file_counter = 0
        
        self.init_ui()
        self.apply_styling()
        
        # Set dialog properties
        self.setWindowTitle("S-Parameter File Manager")
        self.setModal(False)  # Allow interaction with plot window
        self.resize(800, 600)
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("S-Parameter File Manager")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # File loading section
        load_group = QGroupBox("Load Files")
        load_layout = QVBoxLayout()
        
        # Add file buttons
        button_layout = QHBoxLayout()
        self.add_file_button = QPushButton("Add Touchstone File")
        self.add_file_button.clicked.connect(self.add_file)
        button_layout.addWidget(self.add_file_button)
        
        self.add_multiple_button = QPushButton("Add Multiple Files")
        self.add_multiple_button.clicked.connect(self.add_multiple_files)
        button_layout.addWidget(self.add_multiple_button)
        
        button_layout.addStretch()
        load_layout.addLayout(button_layout)
        
        load_group.setLayout(load_layout)
        layout.addWidget(load_group)
        
        # Files table
        files_group = QGroupBox("S-Parameters")
        files_layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("Check the S-parameters you want to plot and customize their legend names:")
        instructions.setWordWrap(True)
        files_layout.addWidget(instructions)
        
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(5)
        self.files_table.setHorizontalHeaderLabels([
            "File", "S-Parameter", "Legend Name", "Plot?", "Remove"
        ])
        
        # Set table properties
        header = self.files_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # File column
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # S-Param
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Legend (expandable)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Plot checkbox
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Remove button
        
        self.files_table.setAlternatingRowColors(True)
        self.files_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        files_layout.addWidget(self.files_table)
        files_group.setLayout(files_layout)
        layout.addWidget(files_group)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_all_files)
        control_layout.addWidget(self.clear_all_button)
        
        control_layout.addStretch()
        
        self.update_plot_button = QPushButton("Update Plot")
        self.update_plot_button.clicked.connect(self.update_plot)
        control_layout.addWidget(self.update_plot_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        control_layout.addWidget(self.close_button)
        
        layout.addLayout(control_layout)
        
        self.setLayout(layout)
    
    def apply_styling(self):
        """Use default Qt styling - no custom colors."""
        pass
    
    def add_file(self):
        """Add a single touchstone file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Touchstone File",
            "",
            "Touchstone Files (*.s1p *.s2p *.s3p *.s4p);;All Files (*)"
        )
        
        if filepath:
            self.load_touchstone_file(filepath)
    
    def add_multiple_files(self):
        """Add multiple touchstone files at once."""
        filepaths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Touchstone Files",
            "",
            "Touchstone Files (*.s1p *.s2p *.s3p *.s4p);;All Files (*)"
        )
        
        for filepath in filepaths:
            self.load_touchstone_file(filepath)
    
    def load_touchstone_file(self, filepath: str):
        """Load a touchstone file and add it to the table."""
        try:
            # Load the file
            touchstone_file = TouchstoneFile(filepath)
            file_id = self.file_counter
            self.file_counter += 1
            
            self.loaded_files[file_id] = touchstone_file
            
            # Add all available S-parameters as separate rows
            for param in touchstone_file.s_params:
                self.add_table_row(file_id, touchstone_file, param)
            
            # Show success message
            QMessageBox.information(self, "Success", f"Loaded {len(touchstone_file.s_params)} S-parameters from {os.path.basename(filepath)}")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load file:\n{str(e)}")
    
    def add_table_row(self, file_id: int, touchstone_file: TouchstoneFile, param_name: str):
        """Add a row to the files table."""
        row = self.files_table.rowCount()
        self.files_table.insertRow(row)
        
        # File name
        filename = os.path.basename(touchstone_file.filepath)
        file_item = QTableWidgetItem(filename)
        file_item.setData(Qt.ItemDataRole.UserRole, file_id)
        self.files_table.setItem(row, 0, file_item)
        
        # S-parameter name (read-only)
        param_item = QTableWidgetItem(param_name)
        param_item.setFlags(param_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.files_table.setItem(row, 1, param_item)
        
        # Legend name (editable text)
        legend_item = QTableWidgetItem(param_name)  # Default to S-param name
        legend_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.files_table.setItem(row, 2, legend_item)
        
        # Enabled checkbox (default unchecked)
        enabled_checkbox = QCheckBox()
        enabled_checkbox.setChecked(False)  # Default to unchecked
        enabled_checkbox.stateChanged.connect(self.on_enabled_changed)
        self.files_table.setCellWidget(row, 3, enabled_checkbox)
        
        # Remove button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_row(row))
        remove_button.setMaximumWidth(80)
        self.files_table.setCellWidget(row, 4, remove_button)
    
    def remove_row(self, row: int):
        """Remove a row from the table."""
        self.files_table.removeRow(row)
        self.update_plot()
    
    def on_param_changed(self):
        """Handle S-parameter selection change."""
        self.update_plot()
    
    def on_enabled_changed(self):
        """Handle enable/disable checkbox change."""
        self.update_plot()
    
    def update_plot(self):
        """Update the plot with current data."""
        # Collect active traces
        self.traces = []
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        for row in range(self.files_table.rowCount()):
            file_item = self.files_table.item(row, 0)
            if not file_item:
                continue
                
            file_id = file_item.data(Qt.ItemDataRole.UserRole)
            if file_id not in self.loaded_files:
                continue
            
            enabled_checkbox = self.files_table.cellWidget(row, 3)
            if not enabled_checkbox or not enabled_checkbox.isChecked():
                continue
            
            param_combo = self.files_table.cellWidget(row, 1)
            legend_item = self.files_table.item(row, 2)
            
            if legend_item:
                touchstone_file = self.loaded_files[file_id]
                param_item = self.files_table.item(row, 1)
                if param_item:
                    param_name = param_item.text()
                    legend_name = legend_item.text()
                
                    trace_data = {
                        'touchstone_file': touchstone_file,
                        'param_name': param_name,
                        'legend_name': legend_name,
                        'color': colors[row % len(colors)]
                    }
                    self.traces.append(trace_data)
        
        # Emit signal to update plot
        self.files_updated.emit(self.traces)
    
    def clear_all_files(self):
        """Clear all loaded files."""
        reply = QMessageBox.question(
            self, 'Clear All Files', 
            'Are you sure you want to clear all loaded files?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.files_table.setRowCount(0)
            self.loaded_files.clear()
            self.traces.clear()
            self.update_plot()
    
    def get_traces(self):
        """Get current trace data."""
        return self.traces
