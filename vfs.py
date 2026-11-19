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

# format_disk()
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
def write(nama_file, isi):
    # ubah teks menjadi bytes
    data = isi.encode()

    # buka disk untuk di ubah, pindah ke area Data, lalu tulis
    with open(NAMA_FILE, "r+b") as f:
        f.seek(AWAL_DATA)
        f.write(data)

    print("Isi di tulis ke disk:", len(data), "byte")

    # langkah 1: cari nomor inode file ini (di root, induk = 0)
    nomor = cari_inode_by_nama(nama_file, 0)
    if nomor is None:
        print("File tidak ditemukan:", nama_file)
        return

    # langkah 2: buat teks inode baru, ukuran dari panjang data, blok awal 0
    teks_inode = f"{nomor}|{nama_file}|file|0|{len(data)}|0"
    inode_byte = teks_inode.encode().ljust(UKURAN_INODE, b"\x00")

    # langkah 3: tulis ulang inode ke posisinya 
    with open(NAMA_FILE, "r+b") as f:
        f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        f.write(inode_byte)

    # nomor = cari_inode_by_nama("laporan.txt", 0)
    # with open(NAMA_FILE, "rb") as f:
        # f.seek(AWAL_TABEL_INODE + nomor * UKURAN_INODE)
        # print(f.read(UKURAN_INODE).rstrip(b"\x00").decode())
# mkdir("dokumen")
# mkdir("foto")
# create("laporan.txt")
ls(0)
# write("laporan.txt", "halo dunia")