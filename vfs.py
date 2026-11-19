UKURAN_DISK = 10 * 1024 * 1024 # ukuran disk: 10 MB (dalam byte)
UKURAN_BLOK = 512              # ukuran satu blok: 512 byte
NAMA_FILE = "disk.vfs"         # nama file disk 
MAGIC = b"VFS1"                # tanda pengenal bahwa ini disk VFS
UKURAN_INODE = 64              # satu inode berukuran 64 byte
MAX_INODE = 100                # jumlah inode yang di sediakan
AWAL_TABEL_INODE = 512         # tabel inode mulai dari byte 512
AWAL_DATA = 6912               # Area Data mulai di byte 6912, setelah superblock dan 100 inode

def format_disk():
    # "wb" = buka file untuk di tulis (file lama akan di timpa)
    with open(NAMA_FILE, "wb") as f:
        # membuat file dengan ukuran 10 MB, isinya nol semua
        f.truncate(UKURAN_DISK)
        # kembali ke awal file
        f.seek(0)
        # menyiapkan Superblock: tanda VFS, lalu diisi nol sampai 512 byte
        superblock = MAGIC.ljust(UKURAN_BLOK, b"\x00")
        f.write(superblock)
        # langkah 1: pindah kursor ke posisi tabel inode(byte 512)
        f.seek(AWAL_TABEL_INODE)
        # langkah 2: buat teks inode root, lalu ubah menjadi byte
        teks_inode = "0|/|folder|0"
        inode_byte = teks_inode.encode()
        # langkah 3: isi sisahnya dengan nol sampai 64 byte
        inode_byte = inode_byte.ljust(UKURAN_INODE, b"\x00")
        # langkah 4: tulis ke file 
        f.write(inode_byte)
    print("Disk baru berhasil di buat:", NAMA_FILE)

format_disk()
def cari_inode_kosong():
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_TABEL_INODE)
        for nomor in range(MAX_INODE):
            data = f.read(UKURAN_INODE)
            if data == bytes(UKURAN_INODE):
                return nomor
        return None
# print("Inode kosong sekarang:", cari_inode_kosong())
def mkdir(nama_folder, induk=0):
    if cari_inode_by_nama(nama_folder, induk) is not None:
        print("Folder sudah ada:", nama_folder)
        return
    # langkah 1: cari inode kosong
    nomor_inode = cari_inode_kosong()
    if nomor_inode is None:
        print("Tabel inode penuh, tidak bisa membuat folder baru")
        return
    # langkah 2: hitung posisi byte inode itu di dalam file
    posisi = AWAL_TABEL_INODE + nomor_inode * UKURAN_INODE
    # langkah 3: buat teks inode, ubah ke bytes, lalu isi sampai 64 byte
    teks_inode = f"{nomor_inode}|{nama_folder}|folder|{induk}"
    inode_byte = teks_inode.encode().ljust(UKURAN_INODE, b"\x00")
    # langkah 4: buka disk untuk di ubah, pindah ke posisi, lalu tulis
    with open(NAMA_FILE, "r+b") as f:
        f.seek(posisi)
        f.write(inode_byte)

    print("Folder dibuat:", nama_folder)
def cari_inode_by_nama(nama, induk):
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_TABEL_INODE)
        for nomor in range(MAX_INODE):
            data = f.read(UKURAN_INODE)
            # lewati inode yang kosong
            if data == bytes(UKURAN_INODE):
                continue
            # buang byte \x00 di belakang, lalu ubah ke teks
            teks = data.rstrip(b"\x00").decode()
            # pecah teks menjadi bagian-bagian, misalnya ["1", "dokumen", "folder", "0"]
            bagian = teks.split("|")
            # cocokan nama dan induknya
            if bagian [1] == nama and int(bagian[3]) == induk:
                return nomor
def ls(induk):
    with open(NAMA_FILE, "rb") as f:
        for nomor in range(MAX_INODE):
            f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
            data = f.read(UKURAN_INODE)

            # lewati inode kosong 
            if data == bytes(UKURAN_INODE):
                continue
            # lewati root, karena root menunjuk ke dirinya sendiri
            if nomor == 0:
                continue
            # buang byte nol di belakang, lalu ubah ke teks 
            teks = data.rstrip(b"\x00").decode()
            bagian = teks.split("|")

            # tampilkan nama jika induknya cocok
            if int(bagian[3]) == induk:
                print(bagian[1])
def create(nama_file, induk=0):
    # cek dulu apakah nama sudah ada di folder ini
    if cari_inode_by_nama(nama_file, induk) is not None:
        print("File sudah ada:", nama_file)
        return

    # cari nomor inode yang masih kosong
    nomor_inode = cari_inode_kosong()
    if nomor_inode is None:
        print("Tabel inode penuh, file tidak bisa dibuat")

    # hitung  posisi inode di dalam file
    posisi = AWAL_TABEL_INODE + nomor_inode * UKURAN_INODE

    # buat teks inode, nomor|nama|jenis|induk|ukuran|blok_awal
    teks_inode = f"{nomor_inode}|{nama_file}|file|{induk}|0|0"
    inode_byte = teks_inode.encode().ljust(UKURAN_INODE, b"\x00")

    # tulis inode ke posisinya
    with open(NAMA_FILE, "r+b") as f:
        f.seek(posisi)
        f.write(inode_byte)

    print("File dibuat:", nama_file)
    return
def write(nama_file, isi, induk=0):
    nomor = cari_inode_by_nama(nama_file, induk)
    if nomor is None:
        print("File tidak ditemukan:", nama_file)
        return

    data = isi.encode()
    jumlah_blok = (len(data) + UKURAN_BLOK - 1) // UKURAN_BLOK
    blok_awal = cari_blok_awal_kosong(jumlah_blok)
    if blok_awal is None:
        print("Ruang disk tidak cukup")
        return
    
    # tulis isi ke blok kosong yang ditemukan
    with open(NAMA_FILE, "r+b") as f:
        f.seek(AWAL_DATA + blok_awal * UKURAN_BLOK)
        f.write(data)

    # perbarui inode dengan ukuran dan blok awal yang baru
    teks_inode = f"{nomor}|{nama_file}|file|{induk}|{len(data)}|{blok_awal}"
    inode_byte = teks_inode.encode().ljust(UKURAN_INODE, b"\x00")
    with open(NAMA_FILE, "r+b") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        f.write(inode_byte)

    print("Isi ditulis ke disk:", len(data), "byte")
def read (nama_file, induk=0):
    # langkah 1: cari nomor inode file
    nomor = cari_inode_by_nama(nama_file, induk)
    if nomor is None:
        print("File tidak ditemukan:", nama_file)
        return
    # langkah 2: baca teks inode, lalu ambil ukuran dan blok awalnya
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        teks = f.read(UKURAN_INODE).rstrip(b"\x00").decode()
    bagian = teks.split("|")
    ukuran = int(bagian[4])
    blok_awal = int(bagian[5])

    # langkah 3: baca isi dari area Data sebanyak ukuran byte
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_DATA + blok_awal * UKURAN_BLOK)
        data = f.read(ukuran)

    # langkah 4: ubah bytes menjadi teks, lalu tampilkan
    print(data.decode())
def info():
    jumlah_inode_terpakai = 0
    blok_terpakai = 0

    # baca semua inode, hitung yang terpakai
    with open(NAMA_FILE, "rb") as f:
        for nomor in range(MAX_INODE):
            f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
            data = f.read(UKURAN_INODE)

            # lewati inode kosong
            if data == bytes(UKURAN_INODE):
                continue
            jumlah_inode_terpakai += 1

            # hanya file yang punya ukuran dan blok, folder dilewati
            bagian = data.rstrip(b"\x00").decode().split("|")
            if bagian[2] != "file":
                continue

            ukuran = int(bagian[4])
            blok_terpakai += (ukuran + UKURAN_BLOK - 1) // UKURAN_BLOK

    # hitung total blok di Area Data, lalu tampilkan hasilnya
    total_blok = (UKURAN_DISK - AWAL_DATA) // UKURAN_BLOK
    print("Ukuran blok    :", UKURAN_BLOK, "byte")
    print("Inode terpakai :", jumlah_inode_terpakai, "dari", MAX_INODE)
    print("Blok terpakai  :", blok_terpakai, "dari", total_blok)
    print("Ruang kosong   :", (total_blok - blok_terpakai) * UKURAN_BLOK, "byte")
def cari_blok_awal_kosong(jumlah_blok):
    total_blok = (UKURAN_DISK - AWAL_DATA) // UKURAN_BLOK

    # kumpulkan semua blok yang sudah dipakai file 
    terpakai = set()
    with open(NAMA_FILE, "rb") as f:
        for nomor in range(1, MAX_INODE):
            f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
            data = f.read(UKURAN_INODE)
            if data == bytes(UKURAN_INODE):
                continue
            bagian = data.rstrip(b"\x00").decode().split("|")
            if bagian[2] != "file":
                continue
            ukuran = int(bagian[4])
            awal = int(bagian[5])
            jml = (ukuran + UKURAN_BLOK - 1) // UKURAN_BLOK
            terpakai.update(range(awal, awal + jml))

    # cari posisi awal yang punya jumlah_blok blok kosong berurutan
    for awal in range(total_blok - jumlah_blok + 1):
        if not any(b in terpakai for b in range(awal, awal + jumlah_blok)):
            return awal
    return None
def delete(nama, induk=0):
    # langkah 1: cari nomor inode yang mau di hapus 
    nomor = cari_inode_by_nama(nama, induk)
    if nomor is None:
        print("Tidak ditemukan:", nama)
        return

    # langkah 2: kalau folder, pastikan tidak ada isinya
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        bagian = f.read(UKURAN_INODE).rstrip(b"\x00").decode()

        if bagian[2] == "folder":
            for n in range(1, MAX_INODE):
                f.seek(AWAL_TABEL_INODE + n * UKURAN_INODE)
                data = f.read(UKURAN_INODE)
                if data == bytes(UKURAN_INODE):
                    continue
                anak = data.rsplit(b"\00").decode().split("|")
                if int(anak[3]) == nomor:
                    print("Folder tidak kosong, tidak bisa di hapus:", nama)
                    return
    # langkah 3: hapus dengan mengosongkan inode (diisi nol)
    with open(NAMA_FILE, "r+b") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        f.write(bytes(UKURAN_INODE))

    print("Dihapus:", nama)
def copy(nama, induk_asal, induk_tujuan):
    nomor = cari_inode_by_nama(nama, induk_asal)
    if nomor is None:
        print("Tidak ditemukan:", nama)
        return
    if cari_inode_by_nama(nama, induk_tujuan) is not None:
        print("Sudah ada di tujuan:", nama)
        return

    # baca info file asli dari inodenya
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        bagian = f.read(UKURAN_INODE).rstrip(b"\x00").decode().split("|")
    if bagian[2] != "file":
        print("Hanya file yang bisa disalin")
        return
    ukuran = int(bagian[4])
    awal = int(bagian[5])

    # baca isi file asli
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_DATA + awal * UKURAN_BLOK)
        isi = f.read(ukuran).decode()

    # buat file baru di tujuan, lalu isi dengan salinannya
    create(nama, induk_tujuan)
    write(nama, isi, induk_tujuan)
    print("Disalin:", nama)
def move(nama, induk_asal, induk_tujuan):
    nomor = cari_inode_by_nama(nama, induk_asal)
    if nomor is None:
        print("Tidak ditemukan:", nama)
        return
    if cari_inode_by_nama(nama, induk_tujuan) is not None:
        print("Sudah ada di tujuan:", nama)
        return
    # cukup ubah kolom induk di inode, isi file tidak perlu di pindah
    with open(NAMA_FILE, "rb") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        bagian = f.read(UKURAN_INODE).rstrip(b"\x00").decode().split("|")
    bagian[3] = str(induk_tujuan)
    inode_byte = "|".join(bagian).encode().ljust(UKURAN_INODE, b"\x00")
    with open(NAMA_FILE, "r+b") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        f.write(inode_byte)
    print("Dipindahkan:", nama)
# format_disk()
# mkdir("dokumen")
# mkdir("foto")
# create("laporan.txt")
# write("laporan.txt", "halo dunia")
# copy("laporan.txt", 0, 1)
# read("laporan.txt")
# delete("laporan.txt", 0)
# move("laporan.txt", 1, 0)
# ls(0)
# ls(1)
# info()
# read("laporan.txt", 1)