"""Nonlinearity (NL) metric calculation for S-boxes."""

import numpy as np
from .utils import walsh_transform, sbox_to_boolean_functions


def compute_nl(sbox):
    """
    Compute the nonlinearity of the S-box.
    
    Nonlinearity is defined as the minimum distance of a Boolean function 
    to the set of all affine functions. For an S-box, this is typically
    computed for each output bit separately and then the minimum is taken.
    
    Args:
        sbox: A list of 256 integers representing the S-box
        
    Returns:
        The minimum nonlinearity across all output bits
    """
    boolean_functions = sbox_to_boolean_functions(sbox)
    nonlinearities = []
    
    for func in boolean_functions:
        # Calculate Walsh-Hadamard transform
        walsh_spectrum = walsh_transform(func)
        
        # Find the maximum absolute value in the spectrum
        max_walsh = np.max(np.abs(walsh_spectrum))
        
        # Nonlinearity = 2^(n-1) - (1/2) * max(|W(a)|)
        # For 8x8 S-box, n=8, so 2^(n-1) = 2^7 = 128
        nl = 128 - max_walsh / 2
        nonlinearities.append(int(round(nl)))
    
    # Return the minimum nonlinearity across all output bits
    return min(nonlinearities)