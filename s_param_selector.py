"""
S-Parameter Selector Dialog for choosing S-parameters from a file.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QCheckBox, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import List, Tuple
from file_manager import TouchstoneFile


class SParamSelectorDialog(QDialog):
    """Dialog for selecting S-parameters from a touchstone file."""
    
    def __init__(self, touchstone_file: TouchstoneFile, current_selections: List[Tuple[str, str]], parent=None):
        super().__init__(parent)
        self.touchstone_file = touchstone_file
        self.current_selections = current_selections.copy()
        
        self.init_ui()
        
        # Set dialog properties
        self.setWindowTitle(f"Select S-Parameters - {touchstone_file.filename}")
        self.setModal(True)
        self.resize(600, 500)
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel(f"S-Parameter Selection")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # File info
        file_info = QLabel(f"File: {self.touchstone_file.filename}")
        file_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_info.setWordWrap(True)
        layout.addWidget(file_info)
        
        # Instructions
        instructions = QLabel("Check the S-parameters you want to plot and customize their legend names:")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # S-parameters table
        self.params_table = QTableWidget()
        self.params_table.setColumnCount(3)
        self.params_table.setHorizontalHeaderLabels([
            "S-Parameter", "Legend Name", "Include?"
        ])
        
        # Set table properties
        header = self.params_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # S-Param
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Legend Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Include checkbox
        
        self.params_table.setAlternatingRowColors(True)
        self.params_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.params_table)
        
        # Populate table
        self.populate_table()
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all)
        button_layout.addWidget(select_all_button)
        
        select_none_button = QPushButton("Select None")
        select_none_button.clicked.connect(self.select_none)
        button_layout.addWidget(select_none_button)
        
        button_layout.addStretch()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def populate_table(self):
        """Populate the table with available S-parameters."""
        # Create a dict of current selections for quick lookup
        current_dict = {param: legend for param, legend in self.current_selections}
        
        self.params_table.setRowCount(len(self.touchstone_file.s_params))
        
        for row, param in enumerate(self.touchstone_file.s_params):
            # S-parameter name (read-only)
            param_item = QTableWidgetItem(param)
            param_item.setFlags(param_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.params_table.setItem(row, 0, param_item)
            
            # Legend name (editable)
            legend_name = current_dict.get(param, param)  # Use current selection or default to param name
            legend_item = QTableWidgetItem(legend_name)
            self.params_table.setItem(row, 1, legend_item)
            
            # Include checkbox
            include_checkbox = QCheckBox()
            include_checkbox.setChecked(param in current_dict)  # Check if currently selected
            self.params_table.setCellWidget(row, 2, include_checkbox)
    
    def select_all(self):
        """Select all S-parameters."""
        for row in range(self.params_table.rowCount()):
            checkbox = self.params_table.cellWidget(row, 2)
            if checkbox:
                checkbox.setChecked(True)
    
    def select_none(self):
        """Deselect all S-parameters."""
        for row in range(self.params_table.rowCount()):
            checkbox = self.params_table.cellWidget(row, 2)
            if checkbox:
                checkbox.setChecked(False)
    
    def get_selections(self):
        """Get the current selections."""
        selections = []
        
        for row in range(self.params_table.rowCount()):
            checkbox = self.params_table.cellWidget(row, 2)
            if checkbox and checkbox.isChecked():
                param_item = self.params_table.item(row, 0)
                legend_item = self.params_table.item(row, 1)
                
                if param_item and legend_item:
                    param_name = param_item.text()
                    legend_name = legend_item.text().strip()
                    
                    # Use param name if legend is empty
                    if not legend_name:
                        legend_name = param_name
                    
                    selections.append((param_name, legend_name))
        
        return selections
