# S-Parameter Plotting Tool

A modern desktop application for visualizing S-parameter data from touchstone files (.s1p to .s4p) with multiple plot types and full customization options.

## Features

- **Multi-file Support**: Load up to 4 touchstone files simultaneously
- **Multiple Plot Types**:
  - Magnitude (dB and Linear)
  - Phase (Degrees and Radians)
  - Smith Chart
  - Real vs Imaginary
  - VSWR
  - Group Delay
- **Interactive Controls**: Select individual S-parameters from each file
- **Customizable Legends**: Rename traces for better readability
- **Plot Customization**: 
  - Editable titles and axis labels
  - Manual or automatic axis limits
  - Grid on/off toggle
  - Legend position control
- **Export Options**: Save plots as PNG, PDF, or SVG
- **Modern UI**: Clean, professional interface built with PyQt6

## Installation

1. Install Python 3.8 or later
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

**Option 1: Improved Workflow (Recommended)**
```bash
python main_improved.py
```
This opens a clean file manager with 4 file slots. Load files, choose S-parameters, then open the plot window.

**Option 2: Separate Windows**
```bash
python main_separate.py
```
This opens two windows:
- **File Manager**: Load and configure touchstone files
- **Plot Window**: Display plots and controls

**Option 3: Single Window**
```bash
python main.py
```
This opens a single window with all controls and the plot area.

### Loading Files

1. Click "Browse" in any of the 4 file slots
2. Select a touchstone file (.s1p, .s2p, .s3p, or .s4p)
3. The file will be automatically parsed and available S-parameters listed
4. Select the desired S-parameter from the dropdown
5. Customize the legend name in the text field
6. Check "Enable" to include this trace in the plot

### Plot Types

Select from the dropdown in the Plot Controls panel:
- **Magnitude (dB)**: S-parameter magnitude in decibels
- **Magnitude (Linear)**: S-parameter magnitude (linear scale)
- **Phase (Degrees)**: S-parameter phase in degrees
- **Phase (Radians)**: S-parameter phase in radians
- **Smith Chart**: Polar plot showing reflection coefficients
- **Real vs Imaginary**: Complex plane representation
- **VSWR**: Voltage Standing Wave Ratio
- **Group Delay**: Signal delay vs frequency

### Customizing Plots

Use the Plot Configuration panel to:
- Edit plot title and axis labels
- Toggle grid display
- Set legend position
- Configure axis limits (auto or manual)
- Export plots in various formats

### File Formats

The application supports standard touchstone files:
- **.s1p**: 1-port S-parameters
- **.s2p**: 2-port S-parameters  
- **.s3p**: 3-port S-parameters
- **.s4p**: 4-port S-parameters

All standard touchstone formats are supported (magnitude/phase, dB/phase, real/imaginary).

## Building Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable using the provided script:
   ```bash
   # For the improved version (recommended)
   python build_improved_exe.py
   
   # For the original version
   python build_exe.py
   ```

3. The executable will be created in the `dist` folder:
   - `S-Parameter-Plotter-Improved` (recommended)
   - `S-Parameter-Plotter` (original)

## Distribution

The `dist` folder contains ready-to-distribute executables:

- **Windows**: `S-Parameter-Plotter-Improved.exe` (double-click to run)
- **macOS**: `S-Parameter-Plotter-Improved.app` (double-click to run)  
- **Linux**: `S-Parameter-Plotter-Improved` (run from terminal)

**No Python installation required** - everything is bundled into the executable!

## Dependencies

- **PyQt6**: Modern GUI framework
- **scikit-rf**: Touchstone file parsing and RF calculations
- **matplotlib**: Plotting and visualization
- **numpy**: Numerical computations

## Troubleshooting

### Common Issues

1. **File won't load**: Ensure the file is a valid touchstone format
2. **Plot not updating**: Check that the file slot is enabled
3. **Missing S-parameters**: Verify the file contains the expected parameters

### Error Messages

- **"Error loading file"**: File format not recognized or corrupted
- **"S-parameter not available"**: Selected parameter doesn't exist in the file

## License

This project is open source and available under the MIT License.