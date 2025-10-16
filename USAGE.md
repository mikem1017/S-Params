# Quick Start Guide

## Running the Application

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the application**:
   ```bash
   python main.py
   ```

3. **Create sample data** (optional):
   ```bash
   python demo.py
   ```
   This creates `sample_1port.s1p` and `sample_2port.s2p` for testing.

## Basic Workflow

### Step 1: Load Files
1. Click **"Browse"** in File Slot 1
2. Select a `.s1p`, `.s2p`, `.s3p`, or `.s4p` file
3. The file will be automatically parsed

### Step 2: Select S-Parameters
1. Choose an S-parameter from the dropdown (e.g., S11, S21, etc.)
2. Customize the legend name if desired
3. Check **"Enable"** to include this trace in the plot

### Step 3: Choose Plot Type
1. Select from the **Plot Type** dropdown:
   - **Magnitude (dB)**: Most common for RF analysis
   - **Phase (Degrees)**: For phase analysis
   - **Smith Chart**: For impedance visualization
   - **VSWR**: For matching analysis
   - **Group Delay**: For time-domain analysis

### Step 4: Customize Plot
1. Edit the **Title** and **Axis Labels**
2. Toggle **Grid** on/off
3. Set **Legend Position**
4. Configure **Axis Limits** (auto or manual)

### Step 5: Export
1. Click **"Save as PNG"**, **"Save as PDF"**, or **"Save as SVG"**
2. Choose location and filename

## Tips

- **Multiple Files**: Load up to 4 files and compare different measurements
- **Color Coding**: Each file slot gets a unique color automatically
- **Real-time Updates**: Plots update immediately when you change settings
- **File Menu**: Use File → Open Files... to load multiple files at once
- **Keyboard Shortcuts**: Ctrl+N (New), Ctrl+O (Open), Ctrl+Q (Quit)

## Common Use Cases

### Antenna Analysis
1. Load `.s1p` file (1-port measurement)
2. Plot **Magnitude (dB)** of S11
3. Add **VSWR** plot to assess matching
4. Use **Smith Chart** for impedance analysis

### Filter Analysis
1. Load `.s2p` file (2-port measurement)
2. Plot **Magnitude (dB)** of S21 (transmission)
3. Plot **Magnitude (dB)** of S11 (reflection)
4. Analyze passband, stopband, and transition regions

### Amplifier Analysis
1. Load `.s2p` file
2. Plot **Magnitude (dB)** of S21 (gain)
3. Plot **Phase (Degrees)** of S21 (phase response)
4. Check **Group Delay** for linearity

## Troubleshooting

- **File won't load**: Ensure it's a valid touchstone format
- **No S-parameters showing**: Check file format and port count
- **Plot not updating**: Verify the file slot is enabled
- **Application won't start**: Check that all dependencies are installed

## Building Executable

To create a standalone `.exe` file:
```bash
python build_exe.py
```

The executable will be in the `dist` folder and can be distributed without requiring Python installation.
