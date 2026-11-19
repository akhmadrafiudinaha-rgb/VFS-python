import io
import tkinter as tk
from contextlib import redirect_stdout
from vfs import format_disk, mkdir, create, write, baca_isi, delete, copy, move, daftar_isi

WARNA_LATAR = "#eef3f8"
WARNA_HIAS = "#2c3e50"
WARNA_TOMBOL = "#2c7fb8"
WARNA_TOMBOL_AKTIF = "#1f5f8b"
WARNA_ISIAN = "#d6e6f2"

gaya_tombol = {
    "bg": WARNA_TOMBOL,
    "fg": "white",
    "activebackground": WARNA_TOMBOL_AKTIF,
    "activeforeground": "white",
    "font": ("Arial", 10, "bold"),
    "width": 18,
    "relief": "flat",
}

gaya_isian = {
    "bg": WARNA_ISIAN,
    "fg": WARNA_HIAS,
    "relief": "solid",
    "bd": 1,
    "insertbackground": WARNA_HIAS,
}

def jalankan(fungsi, *args):
    keluaran = io.StringIO()
    with redirect_stdout(keluaran):
        fungsi(*args)
    label_status.config(text=keluaran.getvalue().strip())

def klik_format():
    jalankan(format_disk)

def klik_mkdir():
    jalankan(mkdir, kotak_nama.get())

def klik_create():
    jalankan(create, kotak_nama.get())

def klik_tulis():
    jalankan(write, kotak_nama.get(), kotak_isi.get())

def klik_baca():
    isi = baca_isi(kotak_nama.get())
    label_isi.config(text=isi)

def klik_hapus():
    jalankan(delete, kotak_nama.get())

def klik_salin():
    jalankan(copy, kotak_nama.get(), 0, int(kotak_tujuan.get()))

def klik_pindah():
    jalankan(move, kotak_nama.get(), 0, int(kotak_tujuan.get()))

def klik_lihat():
    kotak_daftar.delete(0, tk.END)
    for nama in daftar_isi(0):
        kotak_daftar.insert(tk.END, nama)

jendela = tk.Tk()
jendela.title("Virtual File System")
jendela.geometry("900x650")
jendela.configure(bg=WARNA_LATAR)

hias_kiri = tk.Frame(jendela, bg=WARNA_HIAS, width=60)
hias_kiri.pack(side=tk.LEFT, fill=tk.Y)
bingkai_kiri = tk.Frame(hias_kiri, bg=WARNA_TOMBOL, width=8)
bingkai_kiri.pack(side=tk.RIGHT, fill=tk.Y)

hias_kanan = tk.Frame(jendela, bg=WARNA_HIAS, width=60)
hias_kanan.pack(side=tk.RIGHT, fill=tk.Y)
bingkai_kanan = tk.Frame(hias_kanan, bg=WARNA_TOMBOL, width=8)
bingkai_kanan.pack(side=tk.LEFT, fill=tk.Y)

tengah = tk.Frame(jendela, bg=WARNA_LATAR)
tengah.pack(expand=True)

kiri = tk.Frame(tengah, bg=WARNA_LATAR)
kiri.pack(side=tk.LEFT, padx=30)

kanan = tk.Frame(tengah, bg=WARNA_LATAR)
kanan.pack(side=tk.LEFT, padx=30)

judul = tk.Label(kiri, text="Virtual File System", font=("Arial", 18, "bold"), bg=WARNA_LATAR, fg=WARNA_HIAS)
judul.pack(pady=15)

tombol = tk.Button(kiri, text="Format Disk", command=klik_format, **gaya_tombol)
tombol.pack(pady=6)

kotak_nama = tk.Entry(kiri, justify="center", width=24, font=("Arial", 11), **gaya_isian)
kotak_nama.pack(pady=6)

tombol_mkdir = tk.Button(kiri, text="Buat Folder", command=klik_mkdir, **gaya_tombol)
tombol_mkdir.pack(pady=6)

tombol_create = tk.Button(kiri, text="Buat File", command=klik_create, **gaya_tombol)
tombol_create.pack(pady=6)

kotak_isi = tk.Entry(kiri, justify="center", width=24, font=("Arial", 11), **gaya_isian)
kotak_isi.pack(pady=6)

tombol_tulis = tk.Button(kiri, text="Tulis Isi", command=klik_tulis, **gaya_tombol)
tombol_tulis.pack(pady=6)

tombol_baca = tk.Button(kiri, text="Baca File", command=klik_baca, **gaya_tombol)
tombol_baca.pack(pady=6)

tombol_hapus = tk.Button(kiri, text="Hapus", command=klik_hapus, **gaya_tombol)
tombol_hapus.pack(pady=6)

label_tujuan = tk.Label(kiri, text="Nomor folder tujuan (0 = root)", bg=WARNA_LATAR, fg=WARNA_HIAS)
label_tujuan.pack(pady=6)

kotak_tujuan = tk.Entry(kiri, justify="center", width=24, font=("Arial", 11), **gaya_isian)
kotak_tujuan.pack(pady=6)

tombol_salin = tk.Button(kiri, text="Salin", command=klik_salin, **gaya_tombol)
tombol_salin.pack(pady=6)

tombol_pindah = tk.Button(kiri, text="Pindah", command=klik_pindah, **gaya_tombol)
tombol_pindah.pack(pady=6)

judul_kanan = tk.Label(kanan, text="Hasil dan Daftar Isi", font=("Arial", 14, "bold"), bg=WARNA_TOMBOL, fg="white", padx=20, pady=6)
judul_kanan.pack(pady=(15, 10))

label_status = tk.Label(kanan, text="Siap", font=("Arial", 10, "italic"), bg=WARNA_LATAR, fg=WARNA_TOMBOL, wraplength=320)
label_status.pack(pady=5)

kartu_isi = tk.Frame(kanan, bg=WARNA_TOMBOL, padx=2, pady=2)
kartu_isi.pack(pady=10, fill=tk.X)

label_isi = tk.Label(kartu_isi, text="", font=("Arial", 12), bg=WARNA_ISIAN, fg=WARNA_HIAS, wraplength=300, padx=10, pady=10)
label_isi.pack(fill=tk.X)

tombol_lihat = tk.Button(kanan, text="Lihat Isi Root", command=klik_lihat, **gaya_tombol)
tombol_lihat.pack(pady=10)

kartu_daftar = tk.Frame(kanan, bg=WARNA_TOMBOL, padx=2, pady=2)
kartu_daftar.pack(pady=10)

kotak_daftar = tk.Listbox(kartu_daftar, width=40, height=12, bg=WARNA_ISIAN, fg=WARNA_HIAS, font=("Arial", 11), relief="flat", highlightthickness=0)
kotak_daftar.pack()

hiasan_bawah = tk.Label(kanan, text="◆  ◆  ◆", fg=WARNA_TOMBOL, bg=WARNA_LATAR, font=("Arial", 12))
hiasan_bawah.pack(pady=5)

jendela.mainloop()