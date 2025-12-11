"""Utility functions for S-box metric computations."""

import numpy as np
from typing import List


def sbox_to_boolean_functions(sbox: List[int]) -> List[np.ndarray]:
    """
    Convert an S-box to its 8 Boolean component functions.
    
    Args:
        sbox: A list of 256 integers representing the S-box
        
    Returns:
        A list of 8 Boolean functions (each as a numpy array of 0s and 1s)
    """
    boolean_funcs = []
    for bit_pos in range(8):
        func = np.zeros(256, dtype=np.int8)
        for i in range(256):
            # Extract bit at position bit_pos from sbox[i]
            func[i] = (sbox[i] >> bit_pos) & 1
        boolean_funcs.append(func)
    return boolean_funcs


def get_bit(value: int, pos: int) -> int:
    """Extract the bit at the given position from the value."""
    return (value >> pos) & 1


def hamming_weight(value: int) -> int:
    """Calculate the Hamming weight (number of 1 bits) of an integer."""
    count = 0
    while value:
        count += value & 1
        value >>= 1
    return count


def walsh_transform(func: np.ndarray) -> np.ndarray:
    """
    Compute the Walsh-Hadamard transform of a Boolean function.
    
    Args:
        func: A Boolean function represented as a numpy array of 0s and 1s
        
    Returns:
        Walsh-Hadamard transform of the function
    """
    # Convert to {-1, +1} representation
    f_plus_minus = (-1) ** func
    
    # Apply Walsh-Hadamard transform using recursive algorithm
    n = len(f_plus_minus)
    W = f_plus_minus.copy().astype(np.float64)
    
    # Iteratively apply Hadamard matrix
    h = 2
    while h <= n:
        for i in range(0, n, h):
            for j in range(h // 2):
                u = W[i + j]
                v = W[i + j + h // 2]
                W[i + j] = u + v
                W[i + j + h // 2] = u - v
        h *= 2
    
    return W


def get_component_functions(sbox: List[int]) -> List[np.ndarray]:
    """
    Get the 8 component Boolean functions of an 8x8 S-box.
    
    Args:
        sbox: A list of 256 integers representing the S-box
        
    Returns:
        A list of 8 Boolean functions
    """
    return sbox_to_boolean_functions(sbox)


def generate_input_diff_pairs(input_val: int) -> List[tuple]:
    """
    Generate all input pairs that differ by the given input difference.
    
    Args:
        input_val: The input difference value
        
    Returns:
        A list of tuples containing pairs of inputs that differ by input_val
    """
    pairs = []
    for x in range(256):
        y = x ^ input_val
        if x != y:  # Skip if x equals y (which happens when input_val is 0)
            pairs.append((x, y))
    return pairs


def generate_output_mask_pairs(mask_a: int, mask_b: int, sbox: List[int]) -> List[tuple]:
    """
    Generate pairs of (input_masked_output, other_masked_output) for given masks.
    
    Args:
        mask_a: First mask for output bits
        mask_b: Second mask for output bits
        sbox: The S-box being analyzed
        
    Returns:
        A list of tuples containing masked output pairs
    """
    pairs = []
    for i in range(256):
        out_a = sbox[i] & mask_a
        out_b = sbox[i] & mask_b
        pairs.append((out_a, out_b))
    return pairs