import os
import hashlib
import datetime
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import filetype
from fpdf import FPDF
import textwrap
from functools import partial

# === FUNGSI UTILITAS ===

def get_hash(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def analyze_file(path):
    """Analisis ekstensi asli, bandingkan, dan ekstrak metadata."""
    try:
        kind = filetype.guess(path)
        ext_asli = kind.extension if kind else "Tidak diketahui"
        mime = kind.mime if kind else "Unknown"
    except Exception:
        ext_asli, mime = "Error", "Error"

    stat = os.stat(path)
    ukuran = f"{stat.st_size/1024:.2f} KB"
    waktu_buat = datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    waktu_modif = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    nama_file = os.path.basename(path)
    ext_tertulis = os.path.splitext(nama_file)[1][1:].lower()
    status = "Disamarkan" if ext_asli != ext_tertulis and ext_asli != "Tidak diketahui" else "Normal"

    info_metadata = (
        f"Ukuran: {ukuran}, "
        f"MD5: {get_hash(path, 'md5')[:12]}..., "
        f"SHA256: {get_hash(path, 'sha256')[:12]}..., "
        f"Buat: {waktu_buat}, "
        f"Modif: {waktu_modif}, "
        f"MIME: {mime}"
    )

    return {
        "nama": nama_file,
        "ext_tertulis": ext_tertulis,
        "ext_asli": ext_asli,
        "status": status,
        "info_metadata": info_metadata,
    }

# === FUNGSI LAPORAN PDF ===

class PDFReport(FPDF):
    def header(self):
        # Header dengan warna hitam emas
        self.set_fill_color(30, 30, 30)
        self.set_text_color(255, 215, 0)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 12, "LAPORAN DETEKSI PENYAMARAN FILE", ln=True, align="C", fill=True)
        self.ln(5)

    def footer(self):
        # Footer dengan tanggal dan nomor halaman
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100)
        tanggal = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
        self.cell(0, 8, f"Halaman {self.page_no()} | Dibuat: {tanggal}", align="C")

def generate_pdf_report(results):
    """Membuat laporan PDF profesional lengkap dengan metadata dan footer otomatis."""
    os.makedirs("reports", exist_ok=True)

    # Nomor urut otomatis agar tidak menimpa laporan sebelumnya
    base_name = "laporan_deteksi"
    i = 1
    while os.path.exists(f"reports/{base_name}_{i}.pdf"):
        i += 1
    filename = f"reports/{base_name}_{i}.pdf"

    pdf = PDFReport()
    pdf.add_page()

    # === BAGIAN PENJELASAN ===
    pdf.set_text_color(0)
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(
        0, 7,
        "Analisis File:\n"
        "- Mengecek ekstensi asli menggunakan file signature (magic number).\n"
        "- Membandingkan dengan ekstensi nama file, dan menandai jika berbeda.\n"
        "- Mengekstrak metadata detail: ukuran file, hash MD5 & SHA256, waktu pembuatan & modifikasi, serta MIME type.\n"
    )
    pdf.ln(5)

    # === TABEL HASIL UTAMA ===
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(200, 180, 50)
    pdf.set_text_color(0)
    headers = ["No", "Nama File", "Ext Tertulis", "Ext Asli", "Status"]
    widths = [10, 65, 35, 35, 35]

    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.set_fill_color(245, 245, 245)
    fill = False

    for idx, r in enumerate(results, start=1):
        pdf.cell(widths[0], 8, str(idx), border=1, fill=fill)
        pdf.cell(widths[1], 8, r["nama"][:38], border=1, fill=fill)
        pdf.cell(widths[2], 8, r["ext_tertulis"], border=1, fill=fill)
        pdf.cell(widths[3], 8, r["ext_asli"], border=1, fill=fill)
        pdf.cell(widths[4], 8, r["status"], border=1, fill=fill)
        pdf.ln()
        fill = not fill

    pdf.ln(10)

    # === DETAIL METADATA LENGKAP ===
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, " Detail Metadata Setiap File", ln=True)
    pdf.set_font("Helvetica", "", 9)

    for idx, r in enumerate(results, start=1):
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(0, 8, f"{idx}. {r['nama']}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        wrapped = textwrap.fill(r["info_metadata"], width=110)
        pdf.multi_cell(0, 6, wrapped)
        pdf.ln(3)

        # Garis pemisah antar metadata
        y = pdf.get_y()
        pdf.set_draw_color(180, 180, 180)
        pdf.line(10, y, 200, y)
        pdf.ln(3)

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 10, "Laporan ini dibuat otomatis oleh Sistem Deteksi File Penyamaran.", 0, 1, "C")

    pdf.output(filename)
    messagebox.showinfo("Sukses", f"Laporan berhasil disimpan:\n{filename}")
# === GUI TKINTER ===

class DeteksiGUI:
    def __init__(self, master):
        self.master = master
        master.title("🔍 Deteksi File Disamarkan")
        master.geometry("1100x620")
        master.configure(bg="#1a1a1a")

        # === HEADER ===
        header = tk.Label(
            master,
            text="🧾 Sistem Deteksi File Disamarkan",
            bg="#1a1a1a", fg="gold",
            font=("Segoe UI", 16, "bold"),
            pady=10
        )
        header.pack()

        tk.Frame(master, bg="#d4af37", height=2).pack(fill="x", padx=20, pady=(0,10))

        # === FRAME TOMBOL ===
        self.frame_btn = tk.Frame(master, bg="#1a1a1a")
        self.frame_btn.pack(pady=10)

        btn_style = {"bg": "#333", "fg": "white", "font": ("Segoe UI", 10, "bold"), "width": 17, "relief": "flat"}

        self.btn_folder = tk.Button(self.frame_btn, text="📁 Pilih Folder", command=self.select_folder, **btn_style)
        self.btn_files = tk.Button(self.frame_btn, text="📄 Pilih File", command=self.select_files, **btn_style)
        self.btn_pdf = tk.Button(self.frame_btn, text="🧾 Buat Laporan PDF", command=self.export_pdf, bg="gold", fg="black", width=20)

        for i, btn in enumerate([self.btn_folder, self.btn_files, self.btn_pdf]):
            btn.grid(row=0, column=i, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#555"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#333" if b != self.btn_pdf else "gold"))

        # === PROGRESS BAR ===
        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=(5,0))

        # === TABEL ===
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#262626", foreground="white",
                        fieldbackground="#262626", font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background="#444", foreground="gold",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#555555")])

        columns = ("nama", "ext_tertulis", "ext_asli", "status", "info_metadata")
        self.tree = ttk.Treeview(master, columns=columns, show="headings", height=20)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        for col, text, width in [
            ("nama", "Nama File", 180),
            ("ext_tertulis", "Ext Tertulis", 100),
            ("ext_asli", "Ext Asli", 100),
            ("status", "Status Penyamaran", 140),
            ("info_metadata", "Info Metadata", 550),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w")

        # === STATUS BAR ===
        self.status = tk.Label(master, text="Menunggu analisis...", bg="#1a1a1a", fg="gray", font=("Segoe UI", 9))
        self.status.pack(side="bottom", pady=5)

        self.results = []

    # === EVENT HANDLERS ===
    def select_folder(self):
        folder = filedialog.askdirectory(title="Pilih Folder Target")
        if folder:
            files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            self.analyze_files(files)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Pilih File", filetypes=[("All files", "*.*")])
        if files:
            self.analyze_files(files)

    def analyze_files(self, files):
        from time import sleep
        self.tree.delete(*self.tree.get_children())
        self.results.clear()

        total = len(files)
        self.progress["maximum"] = total

        for i, file_path in enumerate(files, start=1):
            data = analyze_file(file_path)
            self.results.append(data)
            self.tree.insert("", "end", values=(
                data["nama"], data["ext_tertulis"], data["ext_asli"], data["status"], data["info_metadata"]
            ))
            self.progress["value"] = i
            self.master.update_idletasks()
            sleep(0.05)  # efek animasi ringan

        self.status.config(text=f"✅ {total} file berhasil dianalisis pada {datetime.datetime.now().strftime('%H:%M:%S')}")
        messagebox.showinfo("Selesai", f"Analisis selesai untuk {total} file.")

    def export_pdf(self):
        print("Tombol PDF ditekan...")  # cek log
        if not self.results:
            messagebox.showwarning("Peringatan", "Belum ada hasil analisis.")
            print("Tidak ada hasil analisis")
            return
        print(f"Membuat laporan untuk {len(self.results)} file...")
        generate_pdf_report(self.results)
        print("PDF selesai dibuat")

# === MAIN ===

if __name__ == "__main__":
    root = tk.Tk()
    app = DeteksiGUI(root)
    root.mainloop()
