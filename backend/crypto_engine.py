"""
Modul ini menyediakan engine kriptografi untuk enkripsi dan dekripsi menggunakan S-box modular.
Mendukung berbagai S-box dan menyediakan implementasi SPN (Substitution-Permutation Network) sederhana.
"""

import os
import json
from typing import List, Dict, Tuple
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class SPNCipher:
    """
    Kelas untuk implementasi SPN (Substitution-Permutation Network) sederhana.
    Mendukung enkripsi dan dekripsi menggunakan S-box modular.
    """

    def __init__(self, sbox: List[int]):
        """
        Inisialisasi cipher dengan S-box tertentu.

        Args:
            sbox: Daftar 256 nilai integer yang merepresentasikan S-box
        """
        if len(sbox) != 256:
            raise ValueError("S-box harus berisi tepat 256 elemen")

        # Validasi bahwa S-box berisi semua nilai 0-255 tanpa duplikat
        if sorted(sbox) != list(range(256)):
            raise ValueError("S-box harus berisi semua nilai 0-255 tanpa duplikat")

        self.sbox = sbox
        self.inv_sbox = self._generate_inverse_sbox(sbox)

    def _generate_inverse_sbox(self, sbox: List[int]) -> List[int]:
        """
        Menghasilkan inverse S-box dari S-box yang diberikan.

        Args:
            sbox: Daftar 256 nilai integer yang merepresentasikan S-box

        Returns:
            Daftar 256 nilai integer yang merepresentasikan inverse S-box
        """
        inv_sbox = [0] * 256
        for i in range(256):
            inv_sbox[sbox[i]] = i
        return inv_sbox

    def _sub_bytes(self, data: bytes) -> bytes:
        """
        Melakukan substitusi byte menggunakan S-box.
        Tahap SubBytes: Mengganti setiap byte dengan nilai dari S-box berdasarkan indeks byte tersebut.

        Args:
            data: Data bytes yang akan disubstitusi

        Returns:
            Hasil substitusi bytes
        """
        return bytes([self.sbox[byte] for byte in data])

    def _inv_sub_bytes(self, data: bytes) -> bytes:
        """
        Melakukan inversi substitusi byte menggunakan inverse S-box.
        Tahap invers SubBytes: Mengganti setiap byte dengan nilai dari inverse S-box.

        Args:
            data: Data bytes yang akan diinversi

        Returns:
            Hasil inversi substitusi bytes
        """
        return bytes([self.inv_sbox[byte] for byte in data])

    def _shift_rows(self, data: bytes) -> bytes:
        """
        Melakukan pergeseran baris sederhana (untuk blok 16 byte).
        Tahap ShiftRows: Menggeser baris-baris byte ke kiri dengan jumlah pergeseran berbeda.
        Ini adalah versi sederhana dari shift rows seperti pada AES.

        Args:
            data: Data bytes yang akan digeser

        Returns:
            Hasil pergeseran bytes
        """
        # Jika data bukan kelipatan 16, padding dulu
        if len(data) % 16 != 0:
            padded_data = data + b'\x00' * (16 - (len(data) % 16))
        else:
            padded_data = data

        result = bytearray()

        # Proses per blok 16 byte (4x4 matrix: 4 baris, 4 kolom)
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]

            # Shift rows sederhana: hanya geser beberapa posisi
            shifted_block = bytearray(16)

            # Baris 0 (posisi 0,4,8,12): tidak digeser
            shifted_block[0] = block[0]
            shifted_block[4] = block[4]
            shifted_block[8] = block[8]
            shifted_block[12] = block[12]

            # Baris 1 (posisi 1,5,9,13): geser 1 posisi ke kiri
            shifted_block[1] = block[5]
            shifted_block[5] = block[9]
            shifted_block[9] = block[13]
            shifted_block[13] = block[1]

            # Baris 2 (posisi 2,6,10,14): geser 2 posisi ke kiri
            shifted_block[2] = block[10]
            shifted_block[6] = block[14]
            shifted_block[10] = block[2]
            shifted_block[14] = block[6]

            # Baris 3 (posisi 3,7,11,15): geser 3 posisi ke kiri
            shifted_block[3] = block[15]
            shifted_block[7] = block[3]
            shifted_block[11] = block[7]
            shifted_block[15] = block[11]

            result.extend(shifted_block)

        return bytes(result)

    def _inv_shift_rows(self, data: bytes) -> bytes:
        """
        Melakukan inversi pergeseran baris.
        Tahap invers ShiftRows: Menggeser baris-baris byte ke kanan untuk mengembalikan posisi semula.

        Args:
            data: Data bytes yang akan diinversi pergeserannya

        Returns:
            Hasil inversi pergeseran bytes
        """
        # Jika data bukan kelipatan 16, padding dulu
        if len(data) % 16 != 0:
            padded_data = data + b'\x00' * (16 - (len(data) % 16))
        else:
            padded_data = data

        result = bytearray()

        # Proses per blok 16 byte
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]

            # Invers shift rows
            shifted_block = bytearray(16)

            # Baris 0 (posisi 0,4,8,12): tidak digeser
            shifted_block[0] = block[0]
            shifted_block[4] = block[4]
            shifted_block[8] = block[8]
            shifted_block[12] = block[12]

            # Baris 1 (posisi 1,5,9,13): geser 1 posisi ke kanan (invers dari kiri)
            shifted_block[1] = block[13]
            shifted_block[5] = block[1]
            shifted_block[9] = block[5]
            shifted_block[13] = block[9]

            # Baris 2 (posisi 2,6,10,14): geser 2 posisi ke kanan (invers dari kiri)
            shifted_block[2] = block[10]
            shifted_block[6] = block[14]
            shifted_block[10] = block[2]
            shifted_block[14] = block[6]

            # Baris 3 (posisi 3,7,11,15): geser 3 posisi ke kanan (invers dari kiri)
            shifted_block[3] = block[7]
            shifted_block[7] = block[11]
            shifted_block[11] = block[15]
            shifted_block[15] = block[3]

            result.extend(shifted_block)

        return bytes(result)

    def _mix_columns(self, data: bytes) -> bytes:
        """
        Operasi sederhana mix columns (berdasarkan operasi di GF(2^8) seperti pada AES).
        Tahap MixColumns: Menggabungkan byte dalam kolom yang sama menggunakan operasi GF(2^8).

        Matriks mix columns AES:
        [[2, 3, 1, 1],
         [1, 2, 3, 1],
         [1, 1, 2, 3],
         [3, 1, 1, 2]]

        Args:
            data: Data bytes yang akan dioperasikan

        Returns:
            Hasil operasi mix columns
        """
        # Jika data bukan kelipatan 16, padding dulu
        if len(data) % 16 != 0:
            padded_data = data + b'\x00' * (16 - (len(data) % 16))
        else:
            padded_data = data

        result = bytearray()

        # Proses per blok 16 byte
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]

            # Mix columns: mengikuti matriks AES
            mixed_block = bytearray(16)

            # Kolom 1 (posisi 0, 4, 8, 12)
            mixed_block[0] = self._gf_multiply(2, block[0]) ^ self._gf_multiply(3, block[4]) ^ block[8] ^ block[12]
            mixed_block[4] = block[0] ^ self._gf_multiply(2, block[4]) ^ self._gf_multiply(3, block[8]) ^ block[12]
            mixed_block[8] = block[0] ^ block[4] ^ self._gf_multiply(2, block[8]) ^ self._gf_multiply(3, block[12])
            mixed_block[12] = self._gf_multiply(3, block[0]) ^ block[4] ^ block[8] ^ self._gf_multiply(2, block[12])

            # Kolom 2 (posisi 1, 5, 9, 13)
            mixed_block[1] = self._gf_multiply(2, block[1]) ^ self._gf_multiply(3, block[5]) ^ block[9] ^ block[13]
            mixed_block[5] = block[1] ^ self._gf_multiply(2, block[5]) ^ self._gf_multiply(3, block[9]) ^ block[13]
            mixed_block[9] = block[1] ^ block[5] ^ self._gf_multiply(2, block[9]) ^ self._gf_multiply(3, block[13])
            mixed_block[13] = self._gf_multiply(3, block[1]) ^ block[5] ^ block[9] ^ self._gf_multiply(2, block[13])

            # Kolom 3 (posisi 2, 6, 10, 14)
            mixed_block[2] = self._gf_multiply(2, block[2]) ^ self._gf_multiply(3, block[6]) ^ block[10] ^ block[14]
            mixed_block[6] = block[2] ^ self._gf_multiply(2, block[6]) ^ self._gf_multiply(3, block[10]) ^ block[14]
            mixed_block[10] = block[2] ^ block[6] ^ self._gf_multiply(2, block[10]) ^ self._gf_multiply(3, block[14])
            mixed_block[14] = self._gf_multiply(3, block[2]) ^ block[6] ^ block[10] ^ self._gf_multiply(2, block[14])

            # Kolom 4 (posisi 3, 7, 11, 15)
            mixed_block[3] = self._gf_multiply(2, block[3]) ^ self._gf_multiply(3, block[7]) ^ block[11] ^ block[15]
            mixed_block[7] = block[3] ^ self._gf_multiply(2, block[7]) ^ self._gf_multiply(3, block[11]) ^ block[15]
            mixed_block[11] = block[3] ^ block[7] ^ self._gf_multiply(2, block[11]) ^ self._gf_multiply(3, block[15])
            mixed_block[15] = self._gf_multiply(3, block[3]) ^ block[7] ^ block[11] ^ self._gf_multiply(2, block[15])

            result.extend(mixed_block)

        return bytes(result)

    def _inv_mix_columns(self, data: bytes) -> bytes:
        """
        Operasi invers mix columns (berdasarkan operasi di GF(2^8) seperti pada AES).
        Tahap invers MixColumns: Menggunakan matriks invers dari matriks AES mix columns.

        Matriks invers mix columns AES:
        [[14, 11, 13, 9],
         [9, 14, 11, 13],
         [13, 9, 14, 11],
         [11, 13, 9, 14]]

        Args:
            data: Data bytes yang akan dioperasikan

        Returns:
            Hasil operasi invers mix columns
        """
        # Jika data bukan kelipatan 16, padding dulu
        if len(data) % 16 != 0:
            padded_data = data + b'\x00' * (16 - (len(data) % 16))
        else:
            padded_data = data

        result = bytearray()

        # Proses per blok 16 byte
        for i in range(0, len(padded_data), 16):
            block = padded_data[i:i+16]

            # Invers mix columns: mengikuti matriks invers AES
            mixed_block = bytearray(16)

            # Kolom 1 (posisi 0, 4, 8, 12)
            mixed_block[0] = self._gf_multiply(14, block[0]) ^ self._gf_multiply(11, block[4]) ^ self._gf_multiply(13, block[8]) ^ self._gf_multiply(9, block[12])
            mixed_block[4] = self._gf_multiply(9, block[0]) ^ self._gf_multiply(14, block[4]) ^ self._gf_multiply(11, block[8]) ^ self._gf_multiply(13, block[12])
            mixed_block[8] = self._gf_multiply(13, block[0]) ^ self._gf_multiply(9, block[4]) ^ self._gf_multiply(14, block[8]) ^ self._gf_multiply(11, block[12])
            mixed_block[12] = self._gf_multiply(11, block[0]) ^ self._gf_multiply(13, block[4]) ^ self._gf_multiply(9, block[8]) ^ self._gf_multiply(14, block[12])

            # Kolom 2 (posisi 1, 5, 9, 13)
            mixed_block[1] = self._gf_multiply(14, block[1]) ^ self._gf_multiply(11, block[5]) ^ self._gf_multiply(13, block[9]) ^ self._gf_multiply(9, block[13])
            mixed_block[5] = self._gf_multiply(9, block[1]) ^ self._gf_multiply(14, block[5]) ^ self._gf_multiply(11, block[9]) ^ self._gf_multiply(13, block[13])
            mixed_block[9] = self._gf_multiply(13, block[1]) ^ self._gf_multiply(9, block[5]) ^ self._gf_multiply(14, block[9]) ^ self._gf_multiply(11, block[13])
            mixed_block[13] = self._gf_multiply(11, block[1]) ^ self._gf_multiply(13, block[5]) ^ self._gf_multiply(9, block[9]) ^ self._gf_multiply(14, block[13])

            # Kolom 3 (posisi 2, 6, 10, 14)
            mixed_block[2] = self._gf_multiply(14, block[2]) ^ self._gf_multiply(11, block[6]) ^ self._gf_multiply(13, block[10]) ^ self._gf_multiply(9, block[14])
            mixed_block[6] = self._gf_multiply(9, block[2]) ^ self._gf_multiply(14, block[6]) ^ self._gf_multiply(11, block[10]) ^ self._gf_multiply(13, block[14])
            mixed_block[10] = self._gf_multiply(13, block[2]) ^ self._gf_multiply(9, block[6]) ^ self._gf_multiply(14, block[10]) ^ self._gf_multiply(11, block[14])
            mixed_block[14] = self._gf_multiply(11, block[2]) ^ self._gf_multiply(13, block[6]) ^ self._gf_multiply(9, block[10]) ^ self._gf_multiply(14, block[14])

            # Kolom 4 (posisi 3, 7, 11, 15)
            mixed_block[3] = self._gf_multiply(14, block[3]) ^ self._gf_multiply(11, block[7]) ^ self._gf_multiply(13, block[11]) ^ self._gf_multiply(9, block[15])
            mixed_block[7] = self._gf_multiply(9, block[3]) ^ self._gf_multiply(14, block[7]) ^ self._gf_multiply(11, block[11]) ^ self._gf_multiply(13, block[15])
            mixed_block[11] = self._gf_multiply(13, block[3]) ^ self._gf_multiply(9, block[7]) ^ self._gf_multiply(14, block[11]) ^ self._gf_multiply(11, block[15])
            mixed_block[15] = self._gf_multiply(11, block[3]) ^ self._gf_multiply(13, block[7]) ^ self._gf_multiply(9, block[11]) ^ self._gf_multiply(14, block[15])

            result.extend(mixed_block)

        return bytes(result)

    def _gf_multiply(self, a: int, b: int) -> int:
        """
        Mengalikan dua elemen dalam GF(2^8) dengan modulo x^8 + x^4 + x^3 + x + 1 (0x11B)
        Digunakan dalam operasi MixColumns.

        Args:
            a: Elemen pertama
            b: Elemen kedua

        Returns:
            Hasil perkalian dalam GF(2^8)
        """
        # Perkalian di GF(2^8) dengan reduksi polinomial x^8 + x^4 + x^3 + x + 1
        result = 0
        while b:
            if b & 1:
                result ^= a
            a <<= 1
            if a & 0x100:  # Jika a > 255 (melebihi 8-bit)
                a ^= 0x11B  # Reduksi dengan polinomial irreducible
            b >>= 1
        return result % 256

    def _add_round_key(self, data: bytes, key: bytes) -> bytes:
        """
        Menambahkan kunci putaran (XOR dengan kunci).
        Tahap AddRoundKey: Mengkombinasikan state dengan kunci putaran menggunakan XOR.

        Args:
            data: Data bytes yang akan ditambahkan kuncinya
            key: Kunci untuk operasi XOR

        Returns:
            Hasil operasi XOR
        """
        result = bytearray()

        for i in range(len(data)):
            result.append(data[i] ^ key[i % len(key)])

        return bytes(result)

    def encrypt_block(self, plaintext: bytes, key: bytes) -> bytes:
        """
        Mengenkripsi satu blok data (16 byte).

        Args:
            plaintext: Data plaintext (harus 16 byte)
            key: Kunci enkripsi

        Returns:
            Data ciphertext (16 byte)
        """
        if len(plaintext) != 16:
            raise ValueError("Plaintext harus berupa blok 16 byte")

        # Round 0: AddRoundKey
        state = self._add_round_key(plaintext, key)

        # Round 1: SubBytes, ShiftRows, MixColumns, AddRoundKey
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._mix_columns(state)
        state = self._add_round_key(state, key)

        # Round 2: SubBytes, ShiftRows, AddRoundKey (tanpa MixColumns di round terakhir)
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, key)

        return state

    def decrypt_block(self, ciphertext: bytes, key: bytes) -> bytes:
        """
        Mendekripsi satu blok data (16 byte).

        Args:
            ciphertext: Data ciphertext (harus 16 byte)
            key: Kunci dekripsi

        Returns:
            Data plaintext (16 byte)
        """
        if len(ciphertext) != 16:
            raise ValueError("Ciphertext harus berupa blok 16 byte")

        # Round 2 inverse: InvAddRoundKey, InvShiftRows, InvSubBytes
        state = self._add_round_key(ciphertext, key)
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)

        # Round 1 inverse: InvAddRoundKey, InvMixColumns, InvShiftRows, InvSubBytes
        state = self._add_round_key(state, key)
        state = self._inv_mix_columns(state)  # Perbaikan: gunakan invers mix columns
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)

        # Round 0 inverse: InvAddRoundKey
        state = self._add_round_key(state, key)

        return state

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Mengenkripsi string teks menjadi bentuk terenkripsi.

        Args:
            plaintext: Teks yang akan dienkripsi
            key: Kunci enkripsi (string)

        Returns:
            Ciphertext dalam format hex
        """
        # Konversi string ke bytes
        plaintext_bytes = plaintext.encode('utf-8')
        key_bytes = key.encode('utf-8')[:32]  # Ambil maksimal 32 byte untuk kunci

        # Padding menggunakan PKCS7 untuk memastikan panjang kelipatan 16
        if len(plaintext_bytes) % 16 != 0:
            plaintext_bytes = pad(plaintext_bytes, 16)

        # Enkripsi per blok
        ciphertext_blocks = []
        for i in range(0, len(plaintext_bytes), 16):
            block = plaintext_bytes[i:i+16]
            encrypted_block = self.encrypt_block(block, key_bytes)
            ciphertext_blocks.append(encrypted_block)

        # Gabungkan semua blok dan konversi ke hex
        full_ciphertext = b''.join(ciphertext_blocks)
        return full_ciphertext.hex()

    def decrypt(self, ciphertext_hex: str, key: str) -> str:
        """
        Mendekripsi ciphertext hex menjadi teks asli.

        Args:
            ciphertext_hex: Ciphertext dalam format hex
            key: Kunci dekripsi (string)

        Returns:
            Plaintext dalam bentuk string
        """
        # Konversi hex ke bytes
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        key_bytes = key.encode('utf-8')[:32]  # Ambil maksimal 32 byte untuk kunci

        # Validasi bahwa ciphertext merupakan kelipatan 16 byte
        if len(ciphertext_bytes) % 16 != 0:
            raise ValueError("Ciphertext harus merupakan kelipatan 16 byte")

        # Dekripsi per blok
        plaintext_blocks = []
        for i in range(0, len(ciphertext_bytes), 16):
            block = ciphertext_bytes[i:i+16]
            decrypted_block = self.decrypt_block(block, key_bytes)
            plaintext_blocks.append(decrypted_block)

        # Gabungkan semua blok
        full_plaintext = b''.join(plaintext_blocks)

        # Hapus padding PKCS7 dan konversi ke string
        try:
            unpadded_plaintext = unpad(full_plaintext, 16)
            return unpadded_plaintext.decode('utf-8')
        except ValueError:
            # Jika unpad gagal, mungkin tidak ada padding atau format salah
            return full_plaintext.decode('utf-8', errors='ignore')


def get_available_sboxes() -> List[Dict[str, str]]:
    """
    Mendapatkan daftar S-box yang tersedia dari direktori sboxes.
    
    Returns:
        Daftar informasi S-box
    """
    sboxes_dir = os.path.join(os.path.dirname(__file__), 'sboxes')
    sbox_files = [f for f in os.listdir(sboxes_dir) if f.endswith('.json')]
    
    sboxes_info = []
    for filename in sbox_files:
        filepath = os.path.join(sboxes_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Buat ID dari nama file tanpa ekstensi
            sbox_id = os.path.splitext(filename)[0]
            sboxes_info.append({
                'id': sbox_id,
                'name': data.get('name', ''),
                'source': data.get('source', ''),
                'description': data.get('description', '')
            })
    
    return sboxes_info


def get_sbox_by_id(sbox_id: str) -> List[int]:
    """
    Mendapatkan konten S-box berdasarkan ID.
    
    Args:
        sbox_id: ID S-box
        
    Returns:
        Daftar nilai S-box
    """
    filepath = os.path.join(os.path.dirname(__file__), 'sboxes', f'{sbox_id}.json')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"S-box '{sbox_id}' tidak ditemukan")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return data['sbox']


def validate_sbox(sbox: List[int]) -> bool:
    """
    Validasi S-box untuk memastikan format yang benar.
    
    Args:
        sbox: Daftar 256 nilai integer
        
    Returns:
        True jika valid, False jika tidak
    """
    if not isinstance(sbox, list) or len(sbox) != 256:
        return False
    
    for val in sbox:
        if not isinstance(val, int) or val < 0 or val > 255:
            return False
    
    # Pastikan tidak ada duplikat (harus berisi semua angka 0-255)
    if sorted(sbox) != list(range(256)):
        return False
    
    return True