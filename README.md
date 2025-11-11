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

## Tampilan Awal Program
Saat program dijalankan, pengguna disambut dengan antarmuka utama berwarna hitam dengan aksen emas, dilengkapi tombol:
- 📁 Pilih Folder
- 📄 Pilih File
- 🧾 Buat Laporan PDF

tampilan awal aplikasi:

![Image](https://github.com/user-attachments/assets/338e9838-a947-4cdd-939d-6458fe9e838d)

## Proses Analisis File
Setelah pengguna memilih satu atau beberapa file, aplikasi akan:
- Membaca file menggunakan library filetype.
- Membandingkan antara ekstensi asli dan ekstensi tertulis.
- Menentukan status file apakah Normal atau Disamarkan.
- Menampilkan metadata (ukuran, hash, waktu pembuatan, MIME type, dll) di tabel GUI.

Hasil analisis file pada GUI:

![Image](https://github.com/user-attachments/assets/7167bedc-8c51-4760-bec2-dcee4b809ce9)

## Pembuatan Laporan PDF
Setelah proses analisis selesai, pengguna dapat menekan tombol 🧾 Buat Laporan PDF. Sistem akan:
- Menghasilkan file PDF dengan nomor urut otomatis (laporan_deteksi_1.pdf, laporan_deteksi_2.pdf, dst).
- Menyimpan laporan di folder /reports/.
- Menampilkan tabel hasil deteksi dan metadata lengkap di halaman terpisah.

PDF memiliki desain header hitam-emas, tabel terformat rapi, serta footer berisi waktu pembuatan dan nomor halaman.

Contoh hasil laporan PDF:

![Image](https://github.com/user-attachments/assets/273163b3-bb7d-410f-83ec-5c0fa330b19e)

