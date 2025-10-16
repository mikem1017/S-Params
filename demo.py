#!/usr/bin/env python3
"""
Demo script showing how to use the S-Parameter plotting application programmatically.
This creates sample touchstone data for demonstration purposes.
"""
import numpy as np
import skrf as rf

def create_sample_touchstone_files():
    """Create sample touchstone files for demonstration."""
    print("Creating sample touchstone files...")
    
    # Create frequency vector (1-10 GHz)
    freq = rf.Frequency(1e9, 10e9, 1001)
    
    # Create sample S-parameter data
    # S11: Simple reflection with some frequency dependence
    s11_mag = 0.3 * np.exp(-freq.f / 5e9)  # Decaying magnitude
    s11_phase = -180 * freq.f / 10e9       # Linear phase
    
    # Convert to complex
    s11 = s11_mag * np.exp(1j * np.deg2rad(s11_phase))
    
    # Create 1-port network
    ntw1 = rf.Network(frequency=freq, s=s11.reshape(-1, 1, 1))
    ntw1.name = 'sample_1port'
    ntw1.write_touchstone('sample_1port.s1p')
    print("✓ Created sample_1port.s1p")
    
    # Create 2-port network with transmission
    s21_mag = 0.8 * np.exp(-freq.f / 8e9)  # Decaying transmission
    s21_phase = -90 * freq.f / 10e9        # Linear phase
    s21 = s21_mag * np.exp(1j * np.deg2rad(s21_phase))
    
    s22 = 0.2 * np.exp(1j * np.deg2rad(s21_phase))  # Different reflection
    s12 = s21  # Reciprocal network
    
    # Create 2x2 S-matrix
    s_matrix = np.zeros((len(freq), 2, 2), dtype=complex)
    s_matrix[:, 0, 0] = s11  # S11
    s_matrix[:, 0, 1] = s21  # S12
    s_matrix[:, 1, 0] = s21  # S21
    s_matrix[:, 1, 1] = s22  # S22
    
    # Create 2-port network
    ntw2 = rf.Network(frequency=freq, s=s_matrix)
    ntw2.name = 'sample_2port'
    ntw2.write_touchstone('sample_2port.s2p')
    print("✓ Created sample_2port.s2p")
    
    print("\nSample files created successfully!")
    print("You can now load these files in the S-Parameter Plotting Tool:")
    print("- sample_1port.s1p (1-port data)")
    print("- sample_2port.s2p (2-port data)")
    
    return ['sample_1port.s1p', 'sample_2port.s2p']

if __name__ == "__main__":
    files = create_sample_touchstone_files()
    print(f"\nCreated {len(files)} sample touchstone files for testing.")
