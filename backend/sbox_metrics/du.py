"""Differential Uniformity (DU) metric calculation for S-boxes."""


def compute_du(sbox):
    """
    Compute the Differential Uniformity (DU) of an S-box.
    
    Differential uniformity is the maximum value in the Difference Distribution Table (DDT),
    excluding the zero input difference. An S-box has differential uniformity δ if
    the maximum number of solutions to S(x+a) + S(x) = b is δ for any non-zero a and any b.
    
    Args:
        sbox: A list of 256 integers representing the S-box
        
    Returns:
        Differential Uniformity value (δ)
    """
    # Create the Difference Distribution Table (DDT)
    ddt = [[0 for _ in range(256)] for _ in range(256)]
    
    # For each possible input difference dx
    for dx in range(1, 256):  # Skip dx=0 as it's not interesting
        # For each possible input x
        for x in range(256):
            # Calculate corresponding input x'
            x_prime = x ^ dx
            # Calculate output difference dy = sbox[x] ^ sbox[x']
            dy = sbox[x] ^ sbox[x_prime]
            # Increment count in DDT
            ddt[dx][dy] += 1
    
    # Find the maximum value in the DDT (excluding the dx=0 row)
    max_du = 0
    for dx in range(1, 256):
        for dy in range(256):
            if ddt[dx][dy] > max_du:
                max_du = ddt[dx][dy]
    
    return max_du