# Dokumentasi Fitur Enkripsi/Dekripsi S-Box

Fitur ini memungkinkan pengguna untuk melakukan enkripsi dan dekripsi teks menggunakan berbagai S-box yang tersedia atau S-box kustom.

## Arsitektur

Fitur ini terdiri dari beberapa komponen utama:

1. **SPNCipher Class** (`backend/crypto_engine.py`): Implementasi dari Substitution-Permutation Network sederhana
2. **API Endpoints** (`backend/app.py`): Endpoint untuk enkripsi/dekripsi dengan S-box yang dipilih
3. **UI Frontend** (`frontend/index.html`): Antarmuka untuk memilih S-box dan melakukan enkripsi/dekripsi

## Fungsi Utama

### 1. SPNCipher Class
- Mendukung enkripsi/dekripsi menggunakan S-box modular
- Melakukan transformasi: SubBytes, ShiftRows, MixColumns, AddRoundKey
- Menggunakan padding PKCS7 untuk menangani data dengan panjang berapa pun
- Memiliki fungsi untuk menghasilkan inverse S-box otomatis

### 2. Transformasi yang Dilakukan
- **SubBytes**: Mengganti setiap byte menggunakan S-box yang dipilih
- **ShiftRows**: Menggeser byte dalam baris dengan pola tertentu
- **MixColumns**: Menggabungkan byte dalam kolom menggunakan operasi di GF(2^8)
- **AddRoundKey**: Mengkombinasikan state dengan kunci menggunakan XOR
- **Padding**: Menggunakan PKCS7 untuk memastikan panjang data kelipatan 16 byte

### 3. API Endpoints
- `POST /api/encrypt`: Enkripsi teks menggunakan S-box tertentu
- `POST /api/decrypt`: Dekripsi teks menggunakan S-box tertentu
- `POST /api/custom_encrypt`: Enkripsi teks menggunakan S-box kustom
- `POST /api/custom_decrypt`: Dekripsi teks menggunakan S-box kustom

### 4. Validasi S-box
- Memastikan S-box memiliki tepat 256 elemen
- Memastikan semua nilai dalam rentang 0-255
- Memastikan tidak ada duplikat (harus berisi semua angka 0-255)

## Penggunaan

### Melalui UI
1. Pilih S-box dari dropdown
2. Masukkan teks yang akan dienkripsi
3. Masukkan kunci
4. Klik "Enkripsi" atau "Dekripsi"

### Melalui API
```json
{
  "plaintext": "teks yang akan dienkripsi",
  "key": "kunci enkripsi",
  "sbox_id": "id_sbox_yang_dipilih"
}
```

Atau untuk S-box kustom:
```json
{
  "plaintext": "teks yang akan dienkripsi",
  "key": "kunci enkripsi",
  "sbox": [256 nilai integer antara 0-255]
}
```

## Tes

File `test_crypto.py` berisi berbagai tes untuk memastikan fungsionalitas bekerja dengan benar:
- Enkripsi/dekripsi dengan berbagai S-box
- Enkripsi/dekripsi dengan berbagai jenis teks
- Enkripsi/dekripsi dengan berbagai kunci
- Validasi S-box
- Fungsi untuk mendapatkan S-box yang tersedia

## Integrasi dengan Sistem Pengujian S-box

Fitur ini terintegrasi dengan sistem pengujian S-box yang sudah ada:
- Menggunakan S-box yang disimpan di `backend/sboxes/`
- Menggunakan fungsi validasi yang sama dengan sistem pengujian
- Dapat menggunakan hasil analisis S-box untuk memilih S-box dengan properti kriptografi terbaik