"""
Custom UI Components for the S-Parameter plotting application.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QCheckBox,
                             QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
                             QFrame, QSizePolicy, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette
from typing import Optional, List
import os


class FileSlotWidget(QWidget):
    """Widget for managing a single file slot."""
    
    file_loaded = pyqtSignal(int, str)  # slot_id, filepath
    file_removed = pyqtSignal(int)
    param_changed = pyqtSignal(int, str)  # slot_id, param_name
    legend_changed = pyqtSignal(int, str)  # slot_id, legend_name
    enabled_changed = pyqtSignal(int, bool)  # slot_id, enabled
    
    def __init__(self, slot_id: int, parent=None):
        super().__init__(parent)
        self.slot_id = slot_id
        self.filepath = None
        self.touchstone_file = None
        self.available_params = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Slot header
        header_layout = QHBoxLayout()
        self.slot_label = QLabel(f"File {self.slot_id + 1}")
        self.slot_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        header_layout.addWidget(self.slot_label)
        
        self.enabled_checkbox = QCheckBox("Enable")
        self.enabled_checkbox.setChecked(False)
        self.enabled_checkbox.stateChanged.connect(self.on_enabled_changed)
        header_layout.addWidget(self.enabled_checkbox)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file loaded")
        self.file_label.setStyleSheet("color: gray; font-style: italic;")
        self.file_label.setWordWrap(True)
        file_layout.addWidget(self.file_label)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setMinimumWidth(100)
        file_layout.addWidget(self.browse_button)
        
        layout.addLayout(file_layout)
        
        # Remove file button
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_file)
        self.remove_button.setEnabled(False)
        self.remove_button.setMinimumWidth(100)
        layout.addWidget(self.remove_button)
        
        # S-parameter selection
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("S-Parameter:"))
        self.param_combo = QComboBox()
        self.param_combo.setEnabled(False)
        self.param_combo.currentTextChanged.connect(self.on_param_changed)
        param_layout.addWidget(self.param_combo)
        layout.addLayout(param_layout)
        
        # Legend name
        legend_layout = QHBoxLayout()
        legend_layout.addWidget(QLabel("Legend:"))
        self.legend_edit = QLineEdit()
        self.legend_edit.setEnabled(False)
        self.legend_edit.textChanged.connect(self.on_legend_changed)
        legend_layout.addWidget(self.legend_edit)
        layout.addLayout(legend_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        self.setLayout(layout)
        self.setEnabled(False)
    
    def browse_file(self):
        """Open file dialog to select a touchstone file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            f"Select Touchstone File for Slot {self.slot_id + 1}",
            "",
            "Touchstone Files (*.s1p *.s2p *.s3p *.s4p);;All Files (*)"
        )
        
        if filepath:
            self.load_file(filepath)
    
    def load_file(self, filepath: str):
        """Load a touchstone file into this slot."""
        try:
            from file_manager import TouchstoneFile
            self.touchstone_file = TouchstoneFile(filepath)
            self.filepath = filepath
            
            # Update UI
            filename = os.path.basename(filepath)
            self.file_label.setText(filename)
            self.file_label.setStyleSheet("color: black; font-style: normal;")
            self.browse_button.setText("Change")
            self.remove_button.setEnabled(True)
            
            # Update available parameters
            self.available_params = self.touchstone_file.s_params.copy()
            self.param_combo.clear()
            self.param_combo.addItems(self.available_params)
            
            # Set default legend name
            if self.available_params:
                self.legend_edit.setText(self.available_params[0])
                self.param_combo.setCurrentText(self.available_params[0])
            
            # Enable controls
            self.setEnabled(True)
            self.param_combo.setEnabled(True)
            self.legend_edit.setEnabled(True)
            
            # Emit signals
            self.file_loaded.emit(self.slot_id, filepath)
            self.enabled_checkbox.setChecked(True)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load file:\n{str(e)}")
    
    def remove_file(self):
        """Remove the loaded file."""
        self.touchstone_file = None
        self.filepath = None
        self.available_params = []
        
        # Reset UI
        self.file_label.setText("No file loaded")
        self.file_label.setStyleSheet("color: gray; font-style: italic;")
        self.browse_button.setText("Browse")
        self.remove_button.setEnabled(False)
        self.param_combo.clear()
        self.param_combo.setEnabled(False)
        self.legend_edit.clear()
        self.legend_edit.setEnabled(False)
        self.setEnabled(False)
        self.enabled_checkbox.setChecked(False)
        
        self.file_removed.emit(self.slot_id)
    
    def on_param_changed(self, param_name: str):
        """Handle S-parameter selection change."""
        if param_name and self.touchstone_file:
            self.param_changed.emit(self.slot_id, param_name)
    
    def on_legend_changed(self, legend_name: str):
        """Handle legend name change."""
        if legend_name and self.touchstone_file:
            self.legend_changed.emit(self.slot_id, legend_name)
    
    def on_enabled_changed(self, state):
        """Handle enable/disable checkbox change."""
        enabled = state == Qt.CheckState.Checked.value
        self.enabled_changed.emit(self.slot_id, enabled)
    
    def get_trace_data(self):
        """Get current trace data for plotting."""
        if (self.enabled_checkbox.isChecked() and 
            self.touchstone_file and 
            self.param_combo.currentText() and
            self.legend_edit.text()):
            
            return {
                'touchstone_file': self.touchstone_file,
                'param_name': self.param_combo.currentText(),
                'legend_name': self.legend_edit.text(),
                'slot_id': self.slot_id
            }
        return None


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
        self.save_png_button.clicked.connect(self.save_png)
        self.save_png_button.setMinimumWidth(140)
        export_layout.addWidget(self.save_png_button)
        
        self.save_pdf_button = QPushButton("Save as PDF")
        self.save_pdf_button.clicked.connect(self.save_pdf)
        self.save_pdf_button.setMinimumWidth(140)
        export_layout.addWidget(self.save_pdf_button)
        
        self.save_svg_button = QPushButton("Save as SVG")
        self.save_svg_button.clicked.connect(self.save_svg)
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
    
    def save_png(self):
        """Save plot as PNG."""
        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Plot as PNG", "s_parameter_plot.png", "PNG Files (*.png)"
        )
        if filepath:
            return filepath, 'png'
        return None, None
    
    def save_pdf(self):
        """Save plot as PDF."""
        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Plot as PDF", "s_parameter_plot.pdf", "PDF Files (*.pdf)"
        )
        if filepath:
            return filepath, 'pdf'
        return None, None
    
    def save_svg(self):
        """Save plot as SVG."""
        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Plot as SVG", "s_parameter_plot.svg", "SVG Files (*.svg)"
        )
        if filepath:
            return filepath, 'svg'
        return None, None
