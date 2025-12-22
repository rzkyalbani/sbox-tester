"""
Affine S-Box Generator
Generates S-Boxes using Affine Matrix transformation in GF(2^8)
Algorithm: S(x) = A * x^(-1) + C
"""

# Irreducible polynomial for GF(2^8): x^8 + x^4 + x^3 + x + 1 (0x11B)
IRREDUCIBLE_POLY = 0x11B

def gf_mult(a, b):
    """
    Multiply two numbers in GF(2^8) using the irreducible polynomial.
    
    Args:
        a: First operand (0-255)
        b: Second operand (0-255)
    
    Returns:
        Product in GF(2^8) (0-255)
    """
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= IRREDUCIBLE_POLY
        b >>= 1
    return p & 0xFF


def gf_inverse(x):
    """
    Calculate multiplicative inverse in GF(2^8) using Extended Euclidean Algorithm.
    
    Args:
        x: Number to invert (0-255)
    
    Returns:
        Multiplicative inverse of x in GF(2^8), or 0 if x is 0
    """
    if x == 0:
        return 0
    
    # Extended Euclidean Algorithm
    r0, r1 = IRREDUCIBLE_POLY, x
    t0, t1 = 0, 1
    
    while r1 != 0:
        q = 0
        temp_r0 = r0
        
        # Calculate quotient by repeated subtraction (XOR in GF(2))
        while temp_r0.bit_length() >= r1.bit_length():
            shift = temp_r0.bit_length() - r1.bit_length()
            temp_r0 ^= (r1 << shift)
            q ^= (1 << shift)
        
        # Update remainders and coefficients
        r0, r1 = r1, temp_r0
        t0, t1 = t1, t0 ^ gf_mult(q & 0xFF, t1)
    
    return t0 & 0xFF


def affine_transform(x, matrix_value, additive_constant):
    """
    Apply affine transformation to a byte.
    
    Args:
        x: Input byte (0-255)
        matrix_value: 8-bit matrix representation
        additive_constant: Constant to add (0-255)
    
    Returns:
        Transformed byte (0-255)
    """
    result = 0
    
    # Apply matrix transformation
    # Each output bit is XOR of selected input bits based on matrix
    for i in range(8):
        bit = 0
        for j in range(8):
            # Check if bit j of matrix row i is set
            if (matrix_value >> ((i + j) % 8)) & 1:
                bit ^= (x >> j) & 1
        result |= (bit << i)
    
    # Add constant (XOR in GF(2))
    return result ^ additive_constant


def generate_affine_sbox(matrix_value=0x57, additive_constant=0x63):
    """
    Generate a complete S-Box using affine transformation.
    
    Args:
        matrix_value: 8-bit matrix representation (default: 0x57 for K44)
        additive_constant: Additive constant (default: 0x63 for standard AES)
    
    Returns:
        List of 256 S-Box values
    """
    sbox = []
    
    for x in range(256):
        # Step 1: Calculate multiplicative inverse in GF(2^8)
        inv = gf_inverse(x)
        
        # Step 2: Apply affine transformation
        transformed = affine_transform(inv, matrix_value, additive_constant)
        
        sbox.append(transformed)
    
    return sbox


# Predefined matrices
PREDEFINED_MATRICES = {
    "K44": {
        "value": 0x57,
        "binary": "01010111",
        "description": "Standard AES Matrix (K44)"
    },
    "K128": {
        "value": 0x1F,
        "binary": "00011111",
        "description": "Alternative Matrix (K128)"
    },
    "K63": {
        "value": 0x3F,
        "binary": "00111111",
        "description": "K63 Matrix"
    }
}


def get_predefined_matrices():
    """
    Get list of predefined matrices.
    
    Returns:
        Dictionary of predefined matrices
    """
    return PREDEFINED_MATRICES
