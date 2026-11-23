from utils import (
    tampilkanHeader, bersihkanLayar, cetakTabel, formatRupiah,
    pilih, konfirmasi, inputTeks, tekanEnter,
    validatorAngka, validatorKode, validatorNama,
)

kategoriMenu = ("Makanan", "Minuman", "Snack", "Dessert")
batasStokMenipis = 5

rentangHarga = (
    ("Murah (< Rp 10.000)", 0, 9999),
    ("Sedang (Rp 10.000 - Rp 20.000)", 10000, 20000),
    ("Mahal (> Rp 20.000)", 20001, 10 ** 9),
)

kolomMenu = ["No", "Kode", "Nama Menu", "Kategori", "Harga", "Stok", "Status"]


def buatDataAwal():
    return {
        "M001": {"nama": "Nasi Goreng", "kategori": "Makanan", "harga": 15000, "stok": 20},
        "M002": {"nama": "Mie Ayam", "kategori": "Makanan", "harga": 13000, "stok": 15},
        "M003": {"nama": "Ayam Geprek", "kategori": "Makanan", "harga": 18000, "stok": 12},
        "M004": {"nama": "Es Teh Manis", "kategori": "Minuman", "harga": 5000, "stok": 40},
        "M005": {"nama": "Jus Alpukat", "kategori": "Minuman", "harga": 12000, "stok": 3},
        "M006": {"nama": "Kentang Goreng", "kategori": "Snack", "harga": 10000, "stok": 25},
        "M007": {"nama": "Pisang Coklat", "kategori": "Dessert", "harga": 8000, "stok": 0},
        "M008": {"nama": "Es Krim Vanila", "kategori": "Dessert", "harga": 9000, "stok": 18},
    }


def statusStok(stok):
    if stok == 0:
        return "Habis"
    elif stok <= batasStokMenipis:
        return "Menipis"
    else:
        return "Tersedia"


def tampilkanTabelMenu(data, judul="Daftar Menu"):
    baris = []
    for nomor, (kode, info) in enumerate(data, start=1):
        baris.append([
            nomor, kode, info["nama"], info["kategori"],
            formatRupiah(info["harga"]), info["stok"], statusStok(info["stok"]),
        ])
    cetakTabel(judul, kolomMenu, baris, kolomKanan=("No", "Harga", "Stok"))


def pilihKodeMenu(menu, pesan, hanyaTersedia=False):
    pilihan = []
    for kode, info in menu.items():
        if hanyaTersedia and info["stok"] == 0:
            continue
        label = (f"{kode} | {info['nama']:<16} | "
                 f"{formatRupiah(info['harga']):<10} | stok {info['stok']}")
        pilihan.append((label, kode))
    if not pilihan:
        return None
    pilihan.append(("<< Batal", None))
    return pilih(pesan, pilihan)


def tambahMenu(menu):
    bersihkanLayar()
    tampilkanHeader("Tambah Menu")

    kode = inputTeks("Kode menu (contoh: M009)", validatorKode(menu))
    if kode is None:
        return
    kode = kode.upper()

    nama = inputTeks("Nama menu", validatorNama(menu))
    if nama is None:
        return
    nama = nama.title()

    kategori = pilih("Kategori", list(kategoriMenu))
    if kategori is None:
        return

    harga = inputTeks("Harga (Rp)", validatorAngka(1))
    if harga is None:
        return

    stok = inputTeks("Stok awal", validatorAngka(0))
    if stok is None:
        return

    menu[kode] = {
        "nama": nama,
        "kategori": kategori,
        "harga": int(harga),
        "stok": int(stok),
    }
    print(f"\nMenu '{nama}' berhasil ditambahkan.")
    tekanEnter()


def tampilkanMenu(menu):
    """Menampilkan seluruh menu."""
    bersihkanLayar()
    tampilkanHeader("Daftar Menu")
    if not menu:
        print("\nBelum ada data menu.")
    else:
        tampilkanTabelMenu(list(menu.items()))
        totalItem = sum(info["stok"] for info in menu.values())
        print(f"Jumlah jenis menu : {len(menu)}")
        print(f"Total stok        : {totalItem}")
    tekanEnter()


def ubahMenu(menu):
    bersihkanLayar()
    tampilkanHeader("Ubah Data Menu")
    if not menu:
        print("\nBelum ada data menu.")
        tekanEnter()
        return

    kode = pilihKodeMenu(menu, "Pilih menu yang diubah")
    if kode is None:
        return
    info = menu[kode]

    bagian = pilih("Bagian yang diubah", [
        ("Harga", "harga"), ("Stok", "stok"), ("Kategori", "kategori"),
        ("<< Batal", None),
    ])

    if bagian == "harga":
        langkah = (("+ Rp 500", 500), ("+ Rp 1.000", 1000), ("+ Rp 2.000", 2000),
                   ("+ Rp 5.000", 5000), ("- Rp 500", -500), ("- Rp 1.000", -1000),
                   ("- Rp 2.000", -2000), ("- Rp 5.000", -5000))
        delta = pilih(f"Harga sekarang {formatRupiah(info['harga'])}. Ubah",
                      list(langkah) + [("<< Batal", None)])
        if delta is None:
            return
        hargaBaru = info["harga"] + delta
        if hargaBaru <= 0:
            print("\nGagal: harga harus lebih dari 0.")
            tekanEnter()
            return
        info["harga"] = hargaBaru

    elif bagian == "stok":
        langkah = (("+ 1", 1), ("+ 5", 5), ("+ 10", 10), ("+ 20", 20), ("+ 50", 50),
                   ("- 1", -1), ("- 5", -5), ("- 10", -10),
                   ("Kosongkan stok (0)", -info["stok"]))
        delta = pilih(f"Stok sekarang {info['stok']}. Ubah",
                      list(langkah) + [("<< Batal", None)])
        if delta is None:
            return
        stokBaru = info["stok"] + delta
        if stokBaru < 0:
            print("\nGagal: stok tidak boleh minus.")
            tekanEnter()
            return
        info["stok"] = stokBaru

    elif bagian == "kategori":
        baru = pilih(f"Kategori sekarang {info['kategori']}. Ganti ke",
                     list(kategoriMenu) + [("<< Batal", None)])
        if baru is None:
            return
        info["kategori"] = baru
    else:
        return

    print(f"\nData '{info['nama']}' berhasil diperbarui.")
    tampilkanTabelMenu([(kode, info)], "Data Setelah Diubah")
    tekanEnter()


def hapusMenu(menu):
    bersihkanLayar()
    tampilkanHeader("Hapus Menu")
    if not menu:
        print("\nBelum ada data menu.")
        tekanEnter()
        return

    kode = pilihKodeMenu(menu, "Pilih menu yang dihapus")
    if kode is None:
        return
    nama = menu[kode]["nama"]
    if konfirmasi(f"Yakin hapus '{nama}'?", default=False):
        del menu[kode]
        print(f"\nMenu '{nama}' berhasil dihapus.")
    else:
        print("\nPenghapusan dibatalkan.")
    tekanEnter()


def cariBerdasarkanKategori(menu, kategori):
    hasil = []
    for kode, info in menu.items():
        if info["kategori"] == kategori:
            hasil.append((kode, info))
    return hasil


def cariBerdasarkanHarga(menu, hargaMin, hargaMaks):
    hasil = []
    for kode, info in menu.items():
        if hargaMin <= info["harga"] <= hargaMaks:
            hasil.append((kode, info))
    return hasil


def cariBerdasarkanStatus(menu, status):
    hasil = []
    for kode, info in menu.items():
        if statusStok(info["stok"]) == status:
            hasil.append((kode, info))
    return hasil


def cariBerdasarkanHurufAwal(menu, huruf):
    hasil = []
    for kode, info in menu.items():
        if info["nama"].upper().startswith(huruf):
            hasil.append((kode, info))
    return hasil


def cariMenu(menu):
    bersihkanLayar()
    tampilkanHeader("Cari Menu")
    if not menu:
        print("\nBelum ada data menu.")
        tekanEnter()
        return

    kriteria = pilih("Cari berdasarkan", [
        ("Kode / Nama (pilih dari daftar)", "kode"),
        ("Huruf awal nama", "huruf"),
        ("Kategori", "kategori"),
        ("Rentang harga", "harga"),
        ("Status stok", "status"),
        ("<< Batal", None),
    ])

    hasil = []
    judul = "Hasil Pencarian"

    if kriteria == "kode":
        kode = pilihKodeMenu(menu, "Pilih menu")
        if kode is None:
            return
        hasil = [(kode, menu[kode])]
        judul = "Hasil Pencarian - Kode / Nama"

    elif kriteria == "huruf":
        hurufAwal = sorted({info["nama"][0].upper() for info in menu.values()})
        huruf = pilih("Huruf awal nama", hurufAwal)
        if huruf is None:
            return
        hasil = cariBerdasarkanHurufAwal(menu, huruf)
        judul = f"Hasil Pencarian - Huruf Awal '{huruf}'"

    elif kriteria == "kategori":
        kategori = pilih("Pilih kategori", list(kategoriMenu))
        if kategori is None:
            return
        hasil = cariBerdasarkanKategori(menu, kategori)
        judul = f"Hasil Pencarian - Kategori {kategori}"

    elif kriteria == "harga":
        pilihan = [(label, (a, b)) for label, a, b in rentangHarga]
        rentang = pilih("Pilih rentang harga", pilihan)
        if rentang is None:
            return
        hasil = cariBerdasarkanHarga(menu, rentang[0], rentang[1])
        judul = "Hasil Pencarian - Rentang Harga"

    elif kriteria == "status":
        status = pilih("Pilih status stok", ["Tersedia", "Menipis", "Habis"])
        if status is None:
            return
        hasil = cariBerdasarkanStatus(menu, status)
        judul = f"Hasil Pencarian - Stok {status}"

    else:
        return

    print()
    if hasil:
        tampilkanTabelMenu(hasil, judul)
        print(f"Ditemukan {len(hasil)} menu.")
    else:
        print("Data tidak ditemukan.")
    tekanEnter()


def nilaiUrut(item, kunci):
    kode, info = item
    if kunci == "kode":
        return kode
    nilai = info[kunci]
    return nilai.lower() if isinstance(nilai, str) else nilai


def urutkanData(data, kunci, menurun=False):
    n = len(hasil)
    for i in range(n - 1):
        idxTerpilih = i
        for j in range(i + 1, n):
            a = nilaiUrut(hasil[j], kunci)
            b = nilaiUrut(hasil[idxTerpilih], kunci)
            lebihCocok = a > b if menurun else a < b
            if lebihCocok:
                idxTerpilih = j
        if idxTerpilih != i:
            hasil[i], hasil[idxTerpilih] = hasil[idxTerpilih], hasil[i]
    return hasil


def urutkanMenu(menu):
    bersihkanLayar()
    tampilkanHeader("Urutkan Menu")
    if not menu:
        print("\nBelum ada data menu.")
        tekanEnter()
        return

    kunci = pilih("Urutkan berdasarkan", [
        ("Kode", "kode"), ("Nama", "nama"), ("Kategori", "kategori"),
        ("Harga", "harga"), ("Stok", "stok"), ("<< Batal", None),
    ])
    if kunci is None:
        return

    arah = pilih("Arah pengurutan", [
        ("Naik (A-Z / kecil ke besar)", False),
        ("Turun (Z-A / besar ke kecil)", True),
    ])
    if arah is None:
        return

    hasil = urutkanData(list(menu.items()), kunci, arah)
    namaArah = "Turun" if arah else "Naik"
    print()
    tampilkanTabelMenu(hasil, f"Menu Diurutkan: {kunci.title()} ({namaArah})")
    tekanEnter()