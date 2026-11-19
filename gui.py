import tkinter as tk
from vfs import format_disk, mkdir, create, write, read, daftar_isi

def klik_format():
    format_disk()

def klik_mkdir():
    mkdir(kotak_nama.get())

def klik_create():
    create(kotak_nama.get())

def klik_tulis():
    write(kotak_nama.get(), kotak_isi.get())

def klik_baca():
    read(kotak_nama.get())

def klik_lihat():
    kotak_daftar.delete(0, tk.END)
    for nama in daftar_isi(0):
        kotak_daftar.insert(tk.END, nama)

jendela = tk.Tk()
jendela.title("Virtual File System")
jendela.geometry("500x700")

judul = tk.Label(jendela, text="Virtual File System", font=("Arial",16))
judul.pack(pady=20)

tombol = tk.Button(jendela, text="Format Disk", command=klik_format)
tombol.pack(pady=10)

kotak_nama = tk.Entry(jendela)
kotak_nama.pack(pady=10)

tombol_mkdir = tk.Button(jendela, text="Buat folder", command=klik_mkdir)
tombol_mkdir.pack(pady=10)

tombol_create = tk.Button(jendela, text="Buat File", command=klik_create)
tombol_create.pack(pady=10)

kotak_isi = tk.Entry(jendela)
kotak_isi.pack(pady=10)

tombol_tulis = tk.Button(jendela, text="Tulis Isi", command=klik_tulis)
tombol_tulis.pack(pady=10)

tombol_baca = tk.Button(jendela, text="Baca File", command=klik_baca)
tombol_baca.pack(pady=10)

tombol_lihat = tk.Button(jendela, text="Lihat isi Root", command=klik_lihat)
tombol_lihat.pack(pady=10)

kotak_daftar = tk.Listbox(jendela, width=40, height=8)
kotak_daftar.pack(pady=10)

jendela.mainloop()