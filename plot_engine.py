"""
Plot Engine for generating various S-parameter plots.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from typing import List, Dict, Tuple, Optional
import matplotlib.patches as mpatches
from matplotlib import gridspec


class PlotEngine:
    """Handles all plotting operations for S-parameters."""
    
    PLOT_TYPES = [
        "Magnitude (dB)",
        "Magnitude (Linear)",
        "Phase (Degrees)",
        "Phase (Radians)",
        "Smith Chart",
        "Real vs Imaginary",
        "VSWR",
        "Group Delay"
    ]
    
    def __init__(self):
        self.figure = Figure(figsize=(10, 7), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = None
        self.plot_config = {
            'title': 'S-Parameter Plot',
            'xlabel': 'Frequency (GHz)',
            'ylabel': 'Magnitude (dB)',
            'grid': True,
            'legend_loc': 'best',
            'xlim_auto': True,
            'ylim_auto': True,
            'xlim': [None, None],
            'ylim': [None, None]
        }
    
    def clear_plot(self):
        """Clear the current plot."""
        self.figure.clear()
        self.ax = None
    
    def plot(self, plot_type: str, traces: List[Dict]):
        """
        Generate a plot based on type and trace data.
        
        Args:
            plot_type: Type of plot to generate
            traces: List of trace dictionaries with keys:
                    - 'touchstone_file': TouchstoneFile object
                    - 'param_name': S-parameter name (e.g., 'S11')
                    - 'legend_name': Custom legend name
                    - 'color': Plot color
        """
        self.clear_plot()
        self.last_traces = traces  # Store traces for re-plotting
        
        if not traces:
            self.ax = self.figure.add_subplot(111)
            self.ax.text(0.5, 0.5, 'No data to plot', 
                        ha='center', va='center', fontsize=14)
            self.canvas.draw()
            return
        
        if plot_type == "Smith Chart":
            self._plot_smith_chart(traces)
        elif plot_type == "Real vs Imaginary":
            self._plot_real_imag(traces)
        else:
            self._plot_standard(plot_type, traces)
        
        self.canvas.draw()
    
    def _plot_standard(self, plot_type: str, traces: List[Dict]):
        """Plot standard XY plots (magnitude, phase, VSWR, group delay)."""
        self.ax = self.figure.add_subplot(111)
        
        for trace in traces:
            tf = trace['touchstone_file']
            param = trace['param_name']
            label = trace['legend_name']
            color = trace.get('color', None)
            
            try:
                if plot_type == "Magnitude (dB)":
                    freq, data = tf.get_magnitude_db(param)
                    ylabel = 'Magnitude (dB)'
                elif plot_type == "Magnitude (Linear)":
                    freq, data = tf.get_magnitude_linear(param)
                    ylabel = 'Magnitude'
                elif plot_type == "Phase (Degrees)":
                    freq, data = tf.get_phase_deg(param)
                    ylabel = 'Phase (Degrees)'
                elif plot_type == "Phase (Radians)":
                    freq, data = tf.get_phase_rad(param)
                    ylabel = 'Phase (Radians)'
                elif plot_type == "VSWR":
                    freq, data = tf.get_vswr(param)
                    ylabel = 'VSWR'
                elif plot_type == "Group Delay":
                    freq, data = tf.get_group_delay(param)
                    ylabel = 'Group Delay (s)'
                else:
                    continue
                
                # Convert frequency to GHz for plotting
                freq_ghz = freq / 1e9
                
                if color:
                    self.ax.plot(freq_ghz, data, label=label, color=color, linewidth=2)
                else:
                    self.ax.plot(freq_ghz, data, label=label, linewidth=2)
                    
            except Exception as e:
                print(f"Error plotting {label}: {str(e)}")
                continue
        
        # Apply configuration
        self.ax.set_xlabel(self.plot_config['xlabel'], fontsize=11, fontweight='bold')
        self.ax.set_ylabel(self.plot_config.get('ylabel', ylabel), fontsize=11, fontweight='bold')
        self.ax.set_title(self.plot_config['title'], fontsize=13, fontweight='bold')
        
        if self.plot_config['grid']:
            self.ax.grid(True, alpha=0.3, linestyle='--')
        
        self.ax.legend(loc=self.plot_config['legend_loc'], framealpha=0.9)
        
        # Set axis limits
        if not self.plot_config['xlim_auto']:
            if self.plot_config['xlim'][0] is not None and self.plot_config['xlim'][1] is not None:
                self.ax.set_xlim(self.plot_config['xlim'])
        
        if not self.plot_config['ylim_auto']:
            if self.plot_config['ylim'][0] is not None and self.plot_config['ylim'][1] is not None:
                self.ax.set_ylim(self.plot_config['ylim'])
        
        self.figure.tight_layout()
    
    def _plot_smith_chart(self, traces: List[Dict]):
        """Plot Smith chart."""
        self.ax = self.figure.add_subplot(111, projection='polar')
        
        # Draw Smith chart grid
        self._draw_smith_grid()
        
        for trace in traces:
            tf = trace['touchstone_file']
            param = trace['param_name']
            label = trace['legend_name']
            color = trace.get('color', None)
            
            try:
                s_data = tf.get_complex_data(param)
                
                # Convert S-parameters to reflection coefficient for Smith chart
                # For Smith chart, we plot Gamma (reflection coefficient)
                gamma = s_data
                
                # Convert to polar coordinates for plotting
                # Smith chart uses: real and imaginary parts mapped to polar
                real = np.real(gamma)
                imag = np.imag(gamma)
                
                # Convert to polar (theta, r)
                r = np.abs(gamma)
                theta = np.angle(gamma)
                
                if color:
                    self.ax.plot(theta, r, label=label, color=color, linewidth=2)
                else:
                    self.ax.plot(theta, r, label=label, linewidth=2)
                
                # Mark start and end points
                self.ax.plot(theta[0], r[0], 'o', markersize=6, color=color if color else None)
                self.ax.plot(theta[-1], r[-1], 's', markersize=6, color=color if color else None)
                
            except Exception as e:
                print(f"Error plotting {label} on Smith chart: {str(e)}")
                continue
        
        self.ax.set_ylim(0, 1)
        self.ax.set_title(self.plot_config['title'], fontsize=13, fontweight='bold', pad=20)
        self.ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1.0), framealpha=0.9)
        self.figure.tight_layout()
    
    def _draw_smith_grid(self):
        """Draw Smith chart grid circles."""
        # Constant resistance circles
        for r in [0, 0.2, 0.5, 1.0, 2.0, 5.0]:
            if r == 0:
                continue
            center_x = r / (1 + r)
            radius = 1 / (1 + r)
            circle = plt.Circle((center_x, 0), radius, fill=False, 
                               color='gray', alpha=0.3, linewidth=0.5,
                               transform=self.ax.transData._b)
            
        # Constant reactance circles
        for x in [0.2, 0.5, 1.0, 2.0, 5.0, -0.2, -0.5, -1.0, -2.0, -5.0]:
            center_y = 1 / x if x != 0 else 0
            radius = abs(1 / x) if x != 0 else 0
        
        # Set grid
        self.ax.grid(True, alpha=0.3, linestyle='--')
    
    def _plot_real_imag(self, traces: List[Dict]):
        """Plot real vs imaginary parts."""
        self.ax = self.figure.add_subplot(111)
        
        for trace in traces:
            tf = trace['touchstone_file']
            param = trace['param_name']
            label = trace['legend_name']
            color = trace.get('color', None)
            
            try:
                freq, real, imag = tf.get_real_imag(param)
                freq_ghz = freq / 1e9
                
                # Plot both real and imaginary
                if color:
                    self.ax.plot(freq_ghz, real, label=f"{label} (Real)", 
                               color=color, linewidth=2, linestyle='-')
                    self.ax.plot(freq_ghz, imag, label=f"{label} (Imag)", 
                               color=color, linewidth=2, linestyle='--')
                else:
                    line, = self.ax.plot(freq_ghz, real, label=f"{label} (Real)", linewidth=2)
                    self.ax.plot(freq_ghz, imag, label=f"{label} (Imag)", 
                               color=line.get_color(), linewidth=2, linestyle='--')
                    
            except Exception as e:
                print(f"Error plotting {label}: {str(e)}")
                continue
        
        self.ax.set_xlabel(self.plot_config['xlabel'], fontsize=11, fontweight='bold')
        self.ax.set_ylabel('Real / Imaginary', fontsize=11, fontweight='bold')
        self.ax.set_title(self.plot_config['title'], fontsize=13, fontweight='bold')
        
        if self.plot_config['grid']:
            self.ax.grid(True, alpha=0.3, linestyle='--')
        
        self.ax.legend(loc=self.plot_config['legend_loc'], framealpha=0.9)
        
        # Set axis limits
        if not self.plot_config['xlim_auto']:
            if self.plot_config['xlim'][0] is not None and self.plot_config['xlim'][1] is not None:
                self.ax.set_xlim(self.plot_config['xlim'])
        
        if not self.plot_config['ylim_auto']:
            if self.plot_config['ylim'][0] is not None and self.plot_config['ylim'][1] is not None:
                self.ax.set_ylim(self.plot_config['ylim'])
        
        self.figure.tight_layout()
    
    def update_config(self, config: Dict):
        """Update plot configuration."""
        self.plot_config.update(config)
    
    def save_plot(self, filepath: str, dpi: int = 300):
        """Save the current plot to file."""
        try:
            self.figure.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
            print(f"Plot saved successfully to: {filepath}")
        except Exception as e:
            print(f"Error saving plot: {e}")
            raise

