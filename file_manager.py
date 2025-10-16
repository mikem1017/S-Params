"""
File Manager for loading and parsing Touchstone files using scikit-rf.
"""
import skrf as rf
import numpy as np
from pathlib import Path
from typing import Optional, List, Tuple


class TouchstoneFile:
    """Represents a loaded Touchstone file with its S-parameters."""
    
    def __init__(self, filepath: str):
        """
        Load a Touchstone file.
        
        Args:
            filepath: Path to the touchstone file (.s1p, .s2p, .s3p, .s4p)
        """
        self.filepath = filepath
        self.filename = Path(filepath).name
        self.network = None
        self.s_params = []
        self.frequency = None
        self.load_file()
    
    def load_file(self):
        """Load the touchstone file using scikit-rf."""
        try:
            self.network = rf.Network(self.filepath)
            self.frequency = self.network.f  # Frequency in Hz
            
            # Determine available S-parameters based on network size
            nports = self.network.nports
            self.s_params = []
            
            for i in range(nports):
                for j in range(nports):
                    self.s_params.append(f"S{i+1}{j+1}")
            
        except Exception as e:
            raise ValueError(f"Error loading {self.filename}: {str(e)}")
    
    def get_s_parameter(self, param_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get a specific S-parameter data.
        
        Args:
            param_name: S-parameter name (e.g., 'S11', 'S21')
        
        Returns:
            Tuple of (frequency array, complex S-parameter array)
        """
        if param_name not in self.s_params:
            raise ValueError(f"{param_name} not available in {self.filename}")
        
        # Parse the parameter name (e.g., 'S21' -> row=1, col=0)
        row = int(param_name[1]) - 1
        col = int(param_name[2]) - 1
        
        # Get the S-parameter data (complex values)
        s_data = self.network.s[:, row, col]
        
        return self.frequency, s_data
    
    def get_magnitude_db(self, param_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get magnitude in dB."""
        freq, s_data = self.get_s_parameter(param_name)
        mag_db = 20 * np.log10(np.abs(s_data))
        return freq, mag_db
    
    def get_magnitude_linear(self, param_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get magnitude (linear)."""
        freq, s_data = self.get_s_parameter(param_name)
        mag = np.abs(s_data)
        return freq, mag
    
    def get_phase_deg(self, param_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get phase in degrees."""
        freq, s_data = self.get_s_parameter(param_name)
        phase = np.angle(s_data, deg=True)
        return freq, phase
    
    def get_phase_rad(self, param_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get phase in radians."""
        freq, s_data = self.get_s_parameter(param_name)
        phase = np.angle(s_data, deg=False)
        return freq, phase
    
    def get_real_imag(self, param_name: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get real and imaginary parts."""
        freq, s_data = self.get_s_parameter(param_name)
        real = np.real(s_data)
        imag = np.imag(s_data)
        return freq, real, imag
    
    def get_vswr(self, param_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate VSWR from reflection coefficient.
        Only valid for reflection parameters (S11, S22, etc.)
        """
        freq, s_data = self.get_s_parameter(param_name)
        gamma = np.abs(s_data)  # Reflection coefficient magnitude
        
        # VSWR = (1 + |Γ|) / (1 - |Γ|)
        # Clip to avoid division by zero
        gamma = np.clip(gamma, 0, 0.9999)
        vswr = (1 + gamma) / (1 - gamma)
        
        return freq, vswr
    
    def get_group_delay(self, param_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate group delay.
        Group delay = -dφ/dω where φ is phase and ω is angular frequency.
        """
        freq, s_data = self.get_s_parameter(param_name)
        phase = np.unwrap(np.angle(s_data))  # Unwrap phase for derivative
        
        # Calculate angular frequency
        omega = 2 * np.pi * freq
        
        # Calculate group delay using numerical derivative
        if len(phase) > 1:
            group_delay = -np.gradient(phase, omega)
        else:
            group_delay = np.zeros_like(phase)
        
        return freq, group_delay
    
    def get_complex_data(self, param_name: str) -> np.ndarray:
        """Get raw complex S-parameter data for Smith chart."""
        _, s_data = self.get_s_parameter(param_name)
        return s_data


class FileManager:
    """Manages multiple touchstone files."""
    
    def __init__(self):
        self.files = {}  # Dictionary mapping slot_id to TouchstoneFile
    
    def load_file(self, slot_id: int, filepath: str) -> TouchstoneFile:
        """
        Load a touchstone file into a specific slot.
        
        Args:
            slot_id: Slot number (0-3)
            filepath: Path to touchstone file
        
        Returns:
            TouchstoneFile object
        """
        touchstone_file = TouchstoneFile(filepath)
        self.files[slot_id] = touchstone_file
        return touchstone_file
    
    def remove_file(self, slot_id: int):
        """Remove a file from a slot."""
        if slot_id in self.files:
            del self.files[slot_id]
    
    def get_file(self, slot_id: int) -> Optional[TouchstoneFile]:
        """Get the TouchstoneFile object for a slot."""
        return self.files.get(slot_id)
    
    def clear_all(self):
        """Clear all loaded files."""
        self.files.clear()

