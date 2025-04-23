import numpy as np
import os

def _get_base_path():
    return os.path.dirname(__file__)

def list_available_ranges():
    """
    Returns a list of available preset .npy range names (without extension).
    """
    base_path = _get_base_path()
    return sorted([
        os.path.splitext(f)[0]
        for f in os.listdir(base_path)
        if f.endswith('.npy')
    ])

def load_range(name):
    """
    Loads a 13x13 preset range matrix from a .npy file.
    
    Args:
        name (str): Name of the preset (without .npy extension)
    
    Returns:
        np.ndarray: 13x13 numpy array representing the hand range
    """
    base_path = _get_base_path()
    file_path = os.path.join(base_path, f"{name}.npy")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Range file '{name}.npy' not found in preset_ranges.")
    
    matrix = np.load(file_path)
    
    if matrix.shape != (13, 13):
        raise ValueError(f"Expected 13x13 matrix, but got shape {matrix.shape}")
    
    return matrix