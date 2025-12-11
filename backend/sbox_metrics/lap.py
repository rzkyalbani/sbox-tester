"""Linear Approximation Probability (LAP) metric calculation for S-boxes."""

import numpy as np
from .utils import hamming_weight


def compute_lap(sbox):
    """
    Compute the Linear Approximation Probability (LAP) of an S-box.
    
    LAP measures the maximum probability bias in linear approximations
    of the S-box. For an 8x8 S-box, this involves calculating the
    Linear Approximation Table (LAT) and finding its maximum entry.
    
    Args:
        sbox: A list of 256 integers representing the S-box
        
    Returns:
        Maximum Linear Approximation Probability
    """
    # Create the Linear Approximation Table (LAT)
    # For efficiency, we'll calculate all entries
    lat = np.zeros((256, 256), dtype=int)
    
    # For each input mask (a) and output mask (b)
    for a in range(256):
        for b in range(256):
            # Calculate the correlation for mask pair (a, b)
            correlation = 0
            for x in range(256):
                # Calculate dot product of a with x
                ax = hamming_weight(a & x) % 2
                # Calculate dot product of b with sbox[x]
                bs = hamming_weight(b & sbox[x]) % 2
                # Add 1 if they are equal, subtract 1 if not
                if ax == bs:
                    correlation += 1
                else:
                    correlation -= 1
            
            # Store in LAT (we store the raw correlation value)
            lat[a][b] = abs(correlation)
    
    # The maximum value in the LAT (excluding zero input/output masks)
    # corresponds to the maximum linear approximation probability
    # normalized by dividing by 256 (the domain size)
    max_lat_value = np.max(lat[1:, 1:])  # Exclude first row/column (zero masks)
    
    # LAP is calculated as (max_correlation)^2 / 2^n
    # For 8x8 S-box, n=8, so LAP = (max_lat_value)^2 / 256^2
    # Alternatively, we can normalize the maximum correlation directly
    lap = max_lat_value / 256.0
    
    return lap