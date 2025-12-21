"""
File tes untuk menguji fungsionalitas enkripsi dan dekripsi menggunakan berbagai S-box.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from crypto_engine import SPNCipher, get_available_sboxes, get_sbox_by_id, validate_sbox

def test_encrypt_decrypt_with_aes_sbox():
    """Menguji enkripsi dan dekripsi menggunakan S-box AES standar"""
    print("Menguji enkripsi/dekripsi dengan S-box AES standar...")
    
    # Ambil S-box AES
    aes_sbox = get_sbox_by_id('standart-aes')
    
    # Validasi S-box
    assert validate_sbox(aes_sbox), "S-box AES tidak valid"
    
    # Buat cipher
    cipher = SPNCipher(aes_sbox)
    
    # Teks uji
    plaintext = "Halo, dunia kriptografi!"
    key = "kunci-rahasia-123"
    
    # Enkripsi
    ciphertext = cipher.encrypt(plaintext, key)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext (hex): {ciphertext}")
    
    # Dekripsi
    decrypted = cipher.decrypt(ciphertext, key)
    print(f"Dekripsi: {decrypted}")
    
    # Verifikasi
    assert plaintext == decrypted, f"Enkripsi/Dekripsi gagal: {plaintext} != {decrypted}"
    print("V Enkripsi/Dekripsi berhasil dengan S-box AES\n")


def test_encrypt_decrypt_with_custom_sbox():
    """Menguji enkripsi dan dekripsi menggunakan S-box kustom"""
    print("Menguji enkripsi/dekripsi dengan S-box kustom...")
    
    # S-box identitas (byte tidak berubah)
    identity_sbox = list(range(256))
    
    # Validasi S-box
    assert validate_sbox(identity_sbox), "S-box identitas tidak valid"
    
    # Buat cipher
    cipher = SPNCipher(identity_sbox)
    
    # Teks uji
    plaintext = "Test kustom S-box"
    key = "kunci-test"
    
    # Enkripsi
    ciphertext = cipher.encrypt(plaintext, key)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext (hex): {ciphertext}")
    
    # Dekripsi
    decrypted = cipher.decrypt(ciphertext, key)
    print(f"Dekripsi: {decrypted}")
    
    # Verifikasi
    assert plaintext == decrypted, f"Enkripsi/Dekripsi gagal: {plaintext} != {decrypted}"
    print("V Enkripsi/Dekripsi berhasil dengan S-box kustom\n")


def test_encrypt_decrypt_with_different_texts():
    """Menguji enkripsi dan dekripsi dengan berbagai jenis teks"""
    print("Menguji enkripsi/dekripsi dengan berbagai jenis teks...")
    
    # Ambil S-box AES
    aes_sbox = get_sbox_by_id('standart-aes')
    cipher = SPNCipher(aes_sbox)
    
    test_cases = [
        "A",  # Satu karakter
        "AB",  # Dua karakter
        "ABC",  # Tiga karakter
        "Hello, World!",  # Teks pendek
        "Ini adalah teks yang lebih panjang untuk menguji fungsionalitas enkripsi dan dekripsi.",  # Teks panjang
        "Teks dengan karakter spesial: !@#$%^&*()",  # Karakter spesial
        "Teks dengan angka: 1234567890",  # Angka
        "Mixed case: AbCdEfGhIjK",  # Huruf besar kecil
        "Teks dengan spasi    dan banyak spasi",  # Banyak spasi
        "Test karakter ASCII"  # Karakter ASCII saja untuk kompatibilitas
    ]
    
    key = "test-key-12345"
    
    for i, plaintext in enumerate(test_cases):
        ciphertext = cipher.encrypt(plaintext, key)
        decrypted = cipher.decrypt(ciphertext, key)
        
        assert plaintext == decrypted, f"Test case {i+1} gagal: {plaintext} != {decrypted}"
        print(f"  V Test case {i+1}: '{plaintext[:20]}{'...' if len(plaintext) > 20 else ''}'")

    print("V Semua test case berhasil\n")


def test_encrypt_decrypt_with_different_keys():
    """Menguji enkripsi dan dekripsi dengan berbagai kunci"""
    print("Menguji enkripsi/dekripsi dengan berbagai kunci...")
    
    # Ambil S-box AES
    aes_sbox = get_sbox_by_id('standart-aes')
    cipher = SPNCipher(aes_sbox)
    
    plaintext = "Test dengan berbagai kunci"
    
    test_keys = [
        "k",  # Satu karakter
        "kunci",  # Lima karakter
        "kunci-panjang-untuk-test",  # Kunci panjang
        "12345",  # Angka
        "!@#$%",  # Karakter spesial
        "Mixed123!@#"  # Campuran
    ]
    
    for i, key in enumerate(test_keys):
        ciphertext = cipher.encrypt(plaintext, key)
        decrypted = cipher.decrypt(ciphertext, key)
        
        assert plaintext == decrypted, f"Test kunci {i+1} gagal: {plaintext} != {decrypted}"
        print(f"  V Kunci {i+1}: '{key}'")

    print("V Semua test kunci berhasil\n")


def test_sbox_validation():
    """Menguji validasi S-box"""
    print("Menguji validasi S-box...")
    
    # S-box valid
    valid_sbox = list(range(256))
    assert validate_sbox(valid_sbox), "S-box valid tidak diterima"
    print("  V S-box valid diterima")

    # S-box terlalu pendek
    short_sbox = list(range(255))
    assert not validate_sbox(short_sbox), "S-box terlalu pendek seharusnya ditolak"
    print("  V S-box terlalu pendek ditolak")

    # S-box terlalu panjang
    long_sbox = list(range(257))
    assert not validate_sbox(long_sbox), "S-box terlalu panjang seharusnya ditolak"
    print("  V S-box terlalu panjang ditolak")

    # S-box dengan duplikat
    dup_sbox = list(range(256))
    dup_sbox[0] = 1  # Duplikat nilai 1
    assert not validate_sbox(dup_sbox), "S-box dengan duplikat seharusnya ditolak"
    print("  V S-box dengan duplikat ditolak")

    # S-box dengan nilai di luar rentang
    out_of_range_sbox = list(range(256))
    out_of_range_sbox[0] = 256  # Di luar rentang 0-255
    assert not validate_sbox(out_of_range_sbox), "S-box dengan nilai di luar rentang seharusnya ditolak"
    print("  V S-box dengan nilai di luar rentang ditolak")

    print("V Semua validasi S-box berhasil\n")


def test_available_sboxes():
    """Menguji fungsi untuk mendapatkan S-box yang tersedia"""
    print("Menguji fungsi untuk mendapatkan S-box yang tersedia...")
    
    sboxes = get_available_sboxes()
    assert len(sboxes) > 0, "Harus ada setidaknya satu S-box yang tersedia"
    
    print(f"  V Ditemukan {len(sboxes)} S-box yang tersedia")

    for sbox_info in sboxes:
        sbox_id = sbox_info['id']
        sbox_data = get_sbox_by_id(sbox_id)
        assert validate_sbox(sbox_data), f"S-box {sbox_id} tidak valid"
        print(f"  V S-box '{sbox_info['name']}' ({sbox_id}) dapat dimuat dan valid")

    print("V Semua S-box yang tersedia dapat dimuat dan valid\n")


def run_all_tests():
    """Menjalankan semua tes"""
    print("Memulai pengujian fungsionalitas enkripsi/dekripsi...\n")
    
    try:
        test_encrypt_decrypt_with_aes_sbox()
        test_encrypt_decrypt_with_custom_sbox()
        test_encrypt_decrypt_with_different_texts()
        test_encrypt_decrypt_with_different_keys()
        test_sbox_validation()
        test_available_sboxes()
        
        print("BERHASIL! Semua tes berhasil! Fungsionalitas enkripsi/dekripsi bekerja dengan baik.")

    except Exception as e:
        print(f"ERROR: Tes gagal dengan error: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()