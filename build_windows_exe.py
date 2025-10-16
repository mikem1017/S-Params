#!/usr/bin/env python3
"""
Build script to create a Windows .exe file.
Note: This script is designed to be run on Windows to create a proper .exe file.
"""
import subprocess
import sys
import os

def build_windows_executable():
    """Build the Windows executable using PyInstaller."""
    print("Building S-Parameter Plotting Tool for Windows (.exe)...")
    print("Note: This script should be run on Windows to create a proper .exe file.")
    
    # PyInstaller command for Windows
    cmd = [
        "pyinstaller",
        "--onefile",           # Create single executable file
        "--windowed",          # No console window
        "--name", "S-Parameter-Plotter-Improved",
        "--add-data", "requirements.txt:.",  # Include requirements file
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets", 
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "skrf",
        "--hidden-import", "matplotlib.backends.backend_qtagg",
        "--hidden-import", "matplotlib.backends._backend_qt",
        "--hidden-import", "numpy",
        "--hidden-import", "scipy",
        "--hidden-import", "pandas",
        "--collect-data", "matplotlib",  # Include matplotlib data files
        "--collect-data", "skrf",        # Include scikit-rf data files
        "--icon", "icon.ico",            # Windows icon (if available)
        "main.py"                        # Main application file
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Windows build successful!")
        print(f"Executable created: dist/S-Parameter-Plotter-Improved.exe")
        print("\nBuild output:")
        print(result.stdout)
        
        # Check if file was created
        exe_path = "dist/S-Parameter-Plotter-Improved.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
            print(f"\n📦 Executable size: {file_size:.1f} MB")
            print(f"📁 Location: {os.path.abspath(exe_path)}")
        
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
    success = build_windows_executable()
    if success:
        print("\n🎉 Windows executable created successfully!")
        print("You can now distribute S-Parameter-Plotter-Improved.exe")
    else:
        print("\n❌ Build failed. Check the error messages above.")
        sys.exit(1)
