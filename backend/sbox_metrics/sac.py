"""Strict Avalanche Criterion (SAC) metric calculation for S-boxes."""

import numpy as np


def compute_sac(sbox):
    """
    Compute the Strict Avalanche Criterion (SAC) property of an S-box.
    
    SAC measures the probability that flipping a single input bit
    causes each output bit to change. For an ideal S-box, this probability
    should be close to 0.5 for all input/output bit combinations.
    
    Args:
        sbox: A list of 256 integers representing the S-box
        
    Returns:
        Average SAC value across all input/output bit combinations
    """
    # Count how many times flipping one input bit flips each output bit
    changes = np.zeros((8, 8))  # input_bit -> output_bit changes
    
    for input_bit in range(8):
        mask = 1 << input_bit
        for x in range(256):
            flipped_x = x ^ mask
            if flipped_x < 256:  # Just a safety check, should always be true
                orig_output = sbox[x]
                flipped_output = sbox[flipped_x]
                
                # Compare each output bit
                for output_bit in range(8):
                    orig_bit = (orig_output >> output_bit) & 1
                    flipped_bit = (flipped_output >> output_bit) & 1
                    
                    # If the output bit changed, increment the counter
                    if orig_bit != flipped_bit:
                        changes[input_bit][output_bit] += 1
    
    # Calculate probability for each input/output bit combination
    # Divide by 256 since we tested with all possible inputs
    probabilities = changes / 256.0
    
    # Calculate the average SAC value
    total_sac = np.sum(probabilities)
    avg_sac = total_sac / (8 * 8)  # 8 input bits * 8 output bits
    
    # For SAC, we want the value to be close to 0.5,
    # so we measure how close we are to 0.5: 1 - 2*|actual - 0.5|
    # But for simplicity, returning the actual average
    return float(avg_sac)