"""
Unit test untuk memvalidasi logika enkripsi/dekripsi menggunakan S-box.
File ini menguji fungsi-fungsi kriptografi sebelum diterapkan ke gambar.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from image_crypto_engine import ImageSPNCipher
import json
import os

def test_inverse_sbox_generation():
    """Test fungsi generate_inverse_sbox"""
    print("Testing inverse S-box generation...")
    
    # Ambil S-box AES standar sebagai contoh
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    aes_sbox_path = os.path.join(sboxes_dir, 'standart-aes.json')
    
    with open(aes_sbox_path, 'r') as f:
        sbox_data = json.load(f)
        sbox = sbox_data['sbox']
    
    cipher = ImageSPNCipher(sbox)
    
    # Verifikasi bahwa inverse S-box benar
    for i in range(256):
        sbox_value = sbox[i]
        inv_sbox_value = cipher.inv_sbox[sbox_value]
        assert inv_sbox_value == i, f"Error: inv_sbox[sbox[{i}]] = {inv_sbox_value}, expected {i}"
    
    print("[PASS] Inverse S-box generation test passed!")


def test_encrypt_decrypt_roundtrip():
    """Test bahwa decrypt(encrypt(data)) == data"""
    print("Testing encrypt/decrypt roundtrip...")
    
    # Ambil S-box AES standar
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    aes_sbox_path = os.path.join(sboxes_dir, 'standart-aes.json')
    
    with open(aes_sbox_path, 'r') as f:
        sbox_data = json.load(f)
        sbox = sbox_data['sbox']
    
    cipher = ImageSPNCipher(sbox)
    
    # Test dengan data kecil (16 byte untuk satu blok)
    test_data = bytes([i % 256 for i in range(16)])
    key = "test_key_12345"
    
    print(f"Original data: {test_data.hex()}")
    
    # Enkripsi
    encrypted = cipher.encrypt_image_buffer(test_data, key)
    print(f"Encrypted data: {encrypted.hex()}")
    
    # Dekripsi
    decrypted = cipher.decrypt_image_buffer(encrypted, key)
    print(f"Decrypted data: {decrypted.hex()}")
    
    # Bandingkan
    assert test_data == decrypted, f"Decryption failed! Original: {test_data.hex()}, Decrypted: {decrypted.hex()}"
    
    print("[PASS] Encrypt/decrypt roundtrip test passed!")


def test_encrypt_decrypt_roundtrip_multiple_blocks():
    """Test bahwa decrypt(encrypt(data)) == data untuk beberapa blok"""
    print("Testing encrypt/decrypt roundtrip for multiple blocks...")
    
    # Ambil S-box AES standar
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    aes_sbox_path = os.path.join(sboxes_dir, 'standart-aes.json')
    
    with open(aes_sbox_path, 'r') as f:
        sbox_data = json.load(f)
        sbox = sbox_data['sbox']
    
    cipher = ImageSPNCipher(sbox)
    
    # Test dengan data lebih besar (misal 48 byte = 3 blok)
    test_data = bytes([i % 256 for i in range(48)])
    key = "test_key_12345"
    
    print(f"Original data length: {len(test_data)}")
    print(f"Original data (first 16 bytes): {test_data[:16].hex()}")
    
    # Enkripsi
    encrypted = cipher.encrypt_image_buffer(test_data, key)
    print(f"Encrypted data length: {len(encrypted)}")
    print(f"Encrypted data (first 16 bytes): {encrypted[:16].hex()}")
    
    # Dekripsi
    decrypted = cipher.decrypt_image_buffer(encrypted, key)
    print(f"Decrypted data length: {len(decrypted)}")
    print(f"Decrypted data (first 16 bytes): {decrypted[:16].hex()}")
    
    # Bandingkan
    assert test_data == decrypted, f"Decryption failed! Original length: {len(test_data)}, Decrypted length: {len(decrypted)}"
    
    print("[PASS] Encrypt/decrypt roundtrip for multiple blocks test passed!")


def test_encrypt_decrypt_with_padding():
    """Test bahwa decrypt(encrypt(data)) == data untuk data yang bukan kelipatan 16"""
    print("Testing encrypt/decrypt with padding (non-multiple of 16)...")
    
    # Ambil S-box AES standar
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    aes_sbox_path = os.path.join(sboxes_dir, 'standart-aes.json')
    
    with open(aes_sbox_path, 'r') as f:
        sbox_data = json.load(f)
        sbox = sbox_data['sbox']
    
    cipher = ImageSPNCipher(sbox)
    
    # Test dengan data yang bukan kelipatan 16 (misal 17 byte)
    test_data = bytes([i % 256 for i in range(17)])
    key = "test_key_12345"
    
    print(f"Original data length: {len(test_data)}")
    print(f"Original data: {test_data.hex()}")
    
    # Enkripsi
    encrypted = cipher.encrypt_image_buffer(test_data, key)
    print(f"Encrypted data length: {len(encrypted)}")
    print(f"Encrypted data: {encrypted.hex()}")
    
    # Dekripsi
    decrypted = cipher.decrypt_image_buffer(encrypted, key)
    print(f"Decrypted data length: {len(decrypted)}")
    print(f"Decrypted data: {decrypted.hex()}")
    
    # Bandingkan
    assert test_data == decrypted, f"Decryption failed! Original length: {len(test_data)}, Decrypted length: {len(decrypted)}"
    assert len(test_data) == len(decrypted), f"Length mismatch! Original: {len(test_data)}, Decrypted: {len(decrypted)}"
    
    print("[PASS] Encrypt/decrypt with padding test passed!")


def test_block_cipher_operations():
    """Test operasi-operasi blok cipher secara individual"""
    print("Testing individual block cipher operations...")
    
    # Ambil S-box AES standar
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    aes_sbox_path = os.path.join(sboxes_dir, 'standart-aes.json')
    
    with open(aes_sbox_path, 'r') as f:
        sbox_data = json.load(f)
        sbox = sbox_data['sbox']
    
    cipher = ImageSPNCipher(sbox)
    
    # Test 1: SubBytes dan InvSubBytes
    test_block = bytes([i % 256 for i in range(16)])
    subbed = cipher._sub_bytes(test_block)
    inv_subbed = cipher._inv_sub_bytes(subbed)
    assert test_block == inv_subbed, f"Sub/InvSub test failed! Original: {test_block.hex()}, Result: {inv_subbed.hex()}"
    
    # Test 2: ShiftRows dan InvShiftRows
    shifted = cipher._shift_rows(test_block)
    inv_shifted = cipher._inv_shift_rows(shifted)
    assert test_block == inv_shifted, f"Shift/InvShift test failed! Original: {test_block.hex()}, Result: {inv_shifted.hex()}"
    
    # Test 3: MixColumns dan InvMixColumns
    mixed = cipher._mix_columns(test_block)
    inv_mixed = cipher._inv_mix_columns(mixed)
    assert test_block == inv_mixed, f"Mix/InvMix test failed! Original: {test_block.hex()}, Result: {inv_mixed.hex()}"
    
    print("[PASS] Individual block cipher operations test passed!")


def main():
    print("Starting crypto validation tests...\n")
    
    try:
        test_inverse_sbox_generation()
        print()
        
        test_block_cipher_operations()
        print()
        
        test_encrypt_decrypt_roundtrip()
        print()
        
        test_encrypt_decrypt_roundtrip_multiple_blocks()
        print()
        
        test_encrypt_decrypt_with_padding()
        print()
        
        print("[SUCCESS] All tests passed! Crypto logic is working correctly.")
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)