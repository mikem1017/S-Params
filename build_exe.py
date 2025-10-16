#!/usr/bin/env python3
"""
Build script to create a standalone executable.
"""
import subprocess
import sys
import os

def build_executable():
    """Build the standalone executable using PyInstaller."""
    print("Building S-Parameter Plotting Tool executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",           # Create single executable file
        "--windowed",          # No console window
        "--name", "S-Parameter-Plotter",
        "--add-data", "requirements.txt:.",  # Include requirements file
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets", 
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "skrf",
        "--hidden-import", "matplotlib.backends.backend_qt5agg",
        "--hidden-import", "numpy",
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build successful!")
        print(f"Executable created in: dist/S-Parameter-Plotter")
        print("\nBuild output:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("✗ Build failed!")
        print("Error output:")
        print(e.stderr)
        return False
    
    except FileNotFoundError:
        print("✗ PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        return False
    
    return True

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\n🎉 Build completed successfully!")
        print("You can now distribute the executable from the 'dist' folder.")
    else:
        print("\n❌ Build failed. Check the error messages above.")
        sys.exit(1)
