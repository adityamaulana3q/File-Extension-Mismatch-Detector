# 🔍 Deteksi File Disamarkan (File Extension Mismatch Detector)

Aplikasi berbasis **Python + Tkinter** untuk mendeteksi file yang disamarkan dengan membandingkan **ekstensi tertulis** dan **ekstensi asli** berdasarkan *magic number (file signature)*.  
Hasil analisis disajikan dalam tampilan GUI yang menarik bertema **hitam-emas**, serta dapat diekspor otomatis menjadi laporan **PDF profesional**.

---

## 📁 Struktur Proyek
deteksi_penyamaran/
│
├── deteksi_file.py # File utama program
│
├── target_scan/ # Folder contoh file yang akan diperiksa
│ ├── contoh1.jpg
│ ├── dokumen.pdf
│ └── file_tes.png
│
└── reports/ # Folder laporan otomatis
└── laporan_deteksi_1.pdf


---

## ⚙️ Fitur Utama

✅ **Analisis File Otomatis**
- Mengecek ekstensi asli berdasarkan *magic number / file signature* menggunakan `filetype`.
- Membandingkan hasil dengan ekstensi tertulis pada nama file.
- Memberi tanda jika ditemukan perbedaan (status: *Disamarkan*).

✅ **Ekstraksi Metadata Lengkap**
- Ukuran file (KB)
- Hash MD5 & SHA256
- Waktu pembuatan & modifikasi
- MIME type

✅ **Tampilan GUI Modern**
- Tema **hitam dan emas** elegan.
- Pilih file/folder langsung dari GUI.
- Hasil analisis ditampilkan dalam tabel interaktif.

✅ **Laporan PDF Profesional**
- Tabel hasil analisis dengan nomor urut otomatis.
- Detail metadata di bagian bawah laporan.
- Tidak menimpa laporan sebelumnya (penomoran otomatis: `laporan_deteksi_1.pdf`, `laporan_deteksi_2.pdf`, dst).

---

## 🧰 Library yang Digunakan

| Library | Fungsi |
|----------|--------|
| `tkinter` | GUI aplikasi |
| `filetype` | Deteksi tipe file asli dari signature |
| `hashlib` | Menghasilkan hash MD5 & SHA256 |
| `os`, `datetime` | Pengelolaan file dan waktu |
| `fpdf` | Pembuatan laporan PDF |
| `textwrap` | Format teks metadata agar rapi |

---

## 🚀 Cara Menjalankan

1. **Clone repositori:**
   ```bash
   git clone https://github.com/username/deteksi_penyamaran.git
   cd deteksi_penyamaran

