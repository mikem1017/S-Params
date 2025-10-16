"""
Simple plot controls widget for the plot window.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QCheckBox,
                             QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Dict


class PlotControlsWidget(QWidget):
    """Widget for plot configuration controls."""
    
    plot_type_changed = pyqtSignal(str)
    config_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Plot Type Selection
        plot_type_group = QGroupBox("Plot Type")
        plot_type_layout = QVBoxLayout()
        
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems([
            "Magnitude (dB)",
            "Magnitude (Linear)",
            "Phase (Degrees)",
            "Phase (Radians)",
            "Smith Chart",
            "Real vs Imaginary",
            "VSWR",
            "Group Delay"
        ])
        self.plot_type_combo.currentTextChanged.connect(
            self.on_plot_type_changed
        )
        plot_type_layout.addWidget(self.plot_type_combo)
        
        plot_type_group.setLayout(plot_type_layout)
        layout.addWidget(plot_type_group)
        
        # Plot Configuration
        config_group = QGroupBox("Plot Configuration")
        config_layout = QFormLayout()
        config_layout.setSpacing(8)
        
        # Title
        self.title_edit = QLineEdit("S-Parameter Plot")
        self.title_edit.textChanged.connect(self.update_config)
        config_layout.addRow("Title:", self.title_edit)
        
        # X-axis label
        self.xlabel_edit = QLineEdit("Frequency (GHz)")
        self.xlabel_edit.textChanged.connect(self.update_config)
        config_layout.addRow("X-Axis Label:", self.xlabel_edit)
        
        # Y-axis label
        self.ylabel_edit = QLineEdit("Magnitude (dB)")
        self.ylabel_edit.textChanged.connect(self.update_config)
        config_layout.addRow("Y-Axis Label:", self.ylabel_edit)
        
        # Grid checkbox
        self.grid_checkbox = QCheckBox("Show Grid")
        self.grid_checkbox.setChecked(True)
        self.grid_checkbox.stateChanged.connect(self.update_config)
        config_layout.addRow(self.grid_checkbox)
        
        # Legend position
        self.legend_combo = QComboBox()
        self.legend_combo.addItems([
            "best", "upper right", "upper left", "lower left", "lower right",
            "center left", "center right", "lower center", "upper center", "center"
        ])
        self.legend_combo.currentTextChanged.connect(self.update_config)
        config_layout.addRow("Legend Position:", self.legend_combo)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Axis Limits
        limits_group = QGroupBox("Axis Limits")
        limits_layout = QFormLayout()
        limits_layout.setSpacing(8)
        
        # X-axis limits
        self.xlim_auto_checkbox = QCheckBox("Auto X-Limits")
        self.xlim_auto_checkbox.setChecked(True)
        self.xlim_auto_checkbox.stateChanged.connect(self.update_config)
        limits_layout.addRow(self.xlim_auto_checkbox)
        
        xlim_layout = QHBoxLayout()
        self.xmin_spinbox = QDoubleSpinBox()
        self.xmin_spinbox.setRange(-999999, 999999)
        self.xmin_spinbox.setDecimals(3)
        self.xmin_spinbox.setEnabled(False)
        self.xmin_spinbox.valueChanged.connect(self.update_config)
        xlim_layout.addWidget(self.xmin_spinbox)
        xlim_layout.addWidget(QLabel("to"))
        self.xmax_spinbox = QDoubleSpinBox()
        self.xmax_spinbox.setRange(-999999, 999999)
        self.xmax_spinbox.setDecimals(3)
        self.xmax_spinbox.setEnabled(False)
        self.xmax_spinbox.valueChanged.connect(self.update_config)
        xlim_layout.addWidget(self.xmax_spinbox)
        limits_layout.addRow("X-Limits:", xlim_layout)
        
        # Y-axis limits
        self.ylim_auto_checkbox = QCheckBox("Auto Y-Limits")
        self.ylim_auto_checkbox.setChecked(True)
        self.ylim_auto_checkbox.stateChanged.connect(self.update_config)
        limits_layout.addRow(self.ylim_auto_checkbox)
        
        ylim_layout = QHBoxLayout()
        self.ymin_spinbox = QDoubleSpinBox()
        self.ymin_spinbox.setRange(-999999, 999999)
        self.ymin_spinbox.setDecimals(3)
        self.ymin_spinbox.setEnabled(False)
        self.ymin_spinbox.valueChanged.connect(self.update_config)
        ylim_layout.addWidget(self.ymin_spinbox)
        ylim_layout.addWidget(QLabel("to"))
        self.ymax_spinbox = QDoubleSpinBox()
        self.ymax_spinbox.setRange(-999999, 999999)
        self.ymax_spinbox.setDecimals(3)
        self.ymax_spinbox.setEnabled(False)
        self.ymax_spinbox.valueChanged.connect(self.update_config)
        ylim_layout.addWidget(self.ymax_spinbox)
        limits_layout.addRow("Y-Limits:", ylim_layout)
        
        limits_group.setLayout(limits_layout)
        layout.addWidget(limits_group)
        
        # Export buttons
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout()
        
        self.save_png_button = QPushButton("Save as PNG")
        self.save_png_button.setMinimumWidth(140)
        export_layout.addWidget(self.save_png_button)
        
        self.save_pdf_button = QPushButton("Save as PDF")
        self.save_pdf_button.setMinimumWidth(140)
        export_layout.addWidget(self.save_pdf_button)
        
        self.save_svg_button = QPushButton("Save as SVG")
        self.save_svg_button.setMinimumWidth(140)
        export_layout.addWidget(self.save_svg_button)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Connect auto-limit checkboxes
        self.xlim_auto_checkbox.stateChanged.connect(self.toggle_xlim_controls)
        self.ylim_auto_checkbox.stateChanged.connect(self.toggle_ylim_controls)
    
    def toggle_xlim_controls(self, state):
        """Toggle X-axis limit controls based on auto checkbox."""
        enabled = state != Qt.CheckState.Checked.value
        self.xmin_spinbox.setEnabled(enabled)
        self.xmax_spinbox.setEnabled(enabled)
        self.update_config()
    
    def toggle_ylim_controls(self, state):
        """Toggle Y-axis limit controls based on auto checkbox."""
        enabled = state != Qt.CheckState.Checked.value
        self.ymin_spinbox.setEnabled(enabled)
        self.ymax_spinbox.setEnabled(enabled)
        self.update_config()
    
    def on_plot_type_changed(self, plot_type: str):
        """Handle plot type change."""
        self.plot_type_changed.emit(plot_type)
        self.update_config()
    
    def update_config(self):
        """Update plot configuration."""
        config = {
            'title': self.title_edit.text(),
            'xlabel': self.xlabel_edit.text(),
            'ylabel': self.ylabel_edit.text(),
            'grid': self.grid_checkbox.isChecked(),
            'legend_loc': self.legend_combo.currentText(),
            'xlim_auto': self.xlim_auto_checkbox.isChecked(),
            'ylim_auto': self.ylim_auto_checkbox.isChecked(),
            'xlim': [self.xmin_spinbox.value(), self.xmax_spinbox.value()] 
                     if not self.xlim_auto_checkbox.isChecked() else [None, None],
            'ylim': [self.ymin_spinbox.value(), self.ymax_spinbox.value()] 
                     if not self.ylim_auto_checkbox.isChecked() else [None, None]
        }
        self.config_changed.emit(config)
    
    def get_plot_type(self):
        """Get current plot type."""
        return self.plot_type_combo.currentText()
