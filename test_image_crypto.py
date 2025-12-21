"""
Unit test untuk memvalidasi logika enkripsi/dekripsi gambar menggunakan S-box.
File ini menguji fungsi-fungsi enkripsi/dekripsi gambar sebelum diterapkan ke UI.
"""

import sys
import os
import tempfile
from io import BytesIO
import numpy as np
from PIL import Image

# Tambahkan path ke backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from image_crypto_engine import ImageSPNCipher
import json


def create_test_image(width=64, height=64, channels=3):
    """Membuat gambar tes dengan ukuran tertentu"""
    # Buat array numpy dengan nilai piksel sederhana
    img_array = np.random.randint(0, 256, size=(height, width, channels), dtype=np.uint8)
    img = Image.fromarray(img_array, 'RGB')
    
    # Simpan ke buffer byte
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer.getvalue()


def test_image_encrypt_decrypt_roundtrip():
    """Test bahwa decrypt(encrypt(gambar)) == gambar asli"""
    print("Testing image encrypt/decrypt roundtrip...")
    
    # Ambil S-box AES standar
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    aes_sbox_path = os.path.join(sboxes_dir, 'standart-aes.json')
    
    with open(aes_sbox_path, 'r') as f:
        sbox_data = json.load(f)
        sbox = sbox_data['sbox']
    
    cipher = ImageSPNCipher(sbox)
    
    # Buat gambar tes
    test_image_bytes = create_test_image(32, 32, 3)  # 32x32 RGB
    key = "test_key_12345"
    
    print(f"Original image size: {len(test_image_bytes)} bytes")
    
    # Enkripsi gambar
    encrypted_image_bytes = cipher.encrypt_image_bytes_v2(test_image_bytes, key)
    print(f"Encrypted image size: {len(encrypted_image_bytes)} bytes")
    
    # Dekripsi gambar
    decrypted_image_bytes = cipher.decrypt_image_bytes_v2(encrypted_image_bytes, key)
    print(f"Decrypted image size: {len(decrypted_image_bytes)} bytes")
    
    # Buka gambar asli dan hasil dekripsi untuk dibandingkan
    original_img = Image.open(BytesIO(test_image_bytes))
    decrypted_img = Image.open(BytesIO(decrypted_image_bytes))
    
    # Bandingkan ukuran gambar
    assert original_img.size == decrypted_img.size, f"Size mismatch! Original: {original_img.size}, Decrypted: {decrypted_img.size}"
    print(f"Image sizes match: {original_img.size}")
    
    # Bandingkan mode gambar
    assert original_img.mode == decrypted_img.mode, f"Mode mismatch! Original: {original_img.mode}, Decrypted: {decrypted_img.mode}"
    print(f"Image modes match: {original_img.mode}")
    
    # Konversi ke array numpy untuk perbandingan pixel
    original_array = np.array(original_img)
    decrypted_array = np.array(decrypted_img)
    
    # Bandingkan array numpy
    arrays_equal = np.array_equal(original_array, decrypted_array)
    assert arrays_equal, "Pixel data mismatch! Images are not identical"
    
    print("[PASS] Image encrypt/decrypt roundtrip test passed!")
    print(f"Arrays are identical: {arrays_equal}")


def test_different_image_sizes():
    """Test dengan berbagai ukuran gambar"""
    print("Testing with different image sizes...")
    
    # Ambil S-box AES standar
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    aes_sbox_path = os.path.join(sboxes_dir, 'standart-aes.json')
    
    with open(aes_sbox_path, 'r') as f:
        sbox_data = json.load(f)
        sbox = sbox_data['sbox']
    
    cipher = ImageSPNCipher(sbox)
    
    sizes = [(16, 16), (32, 32), (64, 32), (31, 31), (17, 23)]  # Termasuk ukuran ganjil
    key = "test_key_12345"
    
    for width, height in sizes:
        print(f"  Testing size {width}x{height}...")
        
        # Buat gambar tes
        test_image_bytes = create_test_image(width, height, 3)
        
        # Enkripsi
        encrypted_image_bytes = cipher.encrypt_image_bytes_v2(test_image_bytes, key)
        
        # Dekripsi
        decrypted_image_bytes = cipher.decrypt_image_bytes_v2(encrypted_image_bytes, key)
        
        # Bandingkan
        original_img = Image.open(BytesIO(test_image_bytes))
        decrypted_img = Image.open(BytesIO(decrypted_image_bytes))

        original_array = np.array(original_img)
        decrypted_array = np.array(decrypted_img)

        arrays_equal = np.array_equal(original_array, decrypted_array)
        assert arrays_equal, f"Pixel data mismatch for size {width}x{height}!"

        print(f"    [PASS] Size {width}x{height} works correctly")

    print("[PASS] All different image sizes test passed!")


def test_different_sboxes():
    """Test dengan berbagai S-box yang tersedia"""
    print("Testing with different S-boxes...")
    
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'backend', 'sboxes')
    sbox_files = [f for f in os.listdir(sboxes_dir) if f.endswith('.json')]
    
    key = "test_key_12345"
    test_image_bytes = create_test_image(16, 16, 3)
    
    for sbox_file in sbox_files:
        print(f"  Testing with S-box: {sbox_file}")
        
        sbox_path = os.path.join(sboxes_dir, sbox_file)
        with open(sbox_path, 'r') as f:
            sbox_data = json.load(f)
            sbox = sbox_data['sbox']
        
        cipher = ImageSPNCipher(sbox)
        
        # Enkripsi
        encrypted_image_bytes = cipher.encrypt_image_bytes_v2(test_image_bytes, key)
        
        # Dekripsi
        decrypted_image_bytes = cipher.decrypt_image_bytes_v2(encrypted_image_bytes, key)
        
        # Bandingkan
        original_img = Image.open(BytesIO(test_image_bytes))
        decrypted_img = Image.open(BytesIO(decrypted_image_bytes))

        original_array = np.array(original_img)
        decrypted_array = np.array(decrypted_img)

        arrays_equal = np.array_equal(original_array, decrypted_array)
        assert arrays_equal, f"Pixel data mismatch with S-box {sbox_file}!"

        print(f"    [PASS] S-box {sbox_file} works correctly")

    print("[PASS] All different S-boxes test passed!")


def main():
    print("Starting image crypto validation tests...\n")
    
    try:
        test_image_encrypt_decrypt_roundtrip()
        print()
        
        test_different_image_sizes()
        print()
        
        test_different_sboxes()
        print()
        
        print("[SUCCESS] All image crypto tests passed! Image encryption/decryption is working correctly.")
        
    except AssertionError as e:
        print(f"[FAIL] Test failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)