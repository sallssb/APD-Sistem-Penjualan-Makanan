import os
import sys

try:
    from prettytable import PrettyTable
    import inquirer
except ModuleNotFoundError:
    print("Library belum terpasang. Jalankan perintah ini di terminal:")
    print(f'"{sys.executable}" -m pip install prettytable inquirer')
    raise SystemExit(1)


# ==========================================
# 1. VARIABEL DAN STRUKTUR DATA
# ==========================================

KATEGORI = ("Makanan", "Minuman")
PERSEN_DISKON = 0.10
BATAS_DISKON = 100000

daftar_menu = [
    {"kode": "M01", "nama": "Nasi Goreng", "kategori": "Makanan", "harga": 18000},
    {"kode": "M02", "nama": "Mie Goreng", "kategori": "Makanan", "harga": 15000},
    {"kode": "M03", "nama": "Ayam Geprek", "kategori": "Makanan", "harga": 20000},
    {"kode": "M04", "nama": "Soto Banjar", "kategori": "Makanan", "harga": 25000},
    {"kode": "D01", "nama": "Es Teh", "kategori": "Minuman", "harga": 5000},
    {"kode": "D02", "nama": "Es Jeruk", "kategori": "Minuman", "harga": 8000},
]

riwayat_transaksi = []


# ==========================================
# 2. FUNGSI INPUT DAN FORMAT
# ==========================================

def rupiah(nilai):
    return "Rp" + format(nilai, ",").replace(",", ".")


def input_teks(pesan):
    while True:
        teks = input(pesan).strip()

        if teks:
            return teks

        print("Input tidak boleh kosong.")


def input_angka(pesan, minimum=0, maksimum=None):
    while True:
        try:
            angka = int(input(pesan))

            if angka < minimum or (maksimum is not None and angka > maksimum):
                print("Angka di luar batas yang diizinkan.")
            else:
                return angka

        except ValueError:
            print("Masukkan bilangan bulat, tanpa titik atau koma.")


def pilih_opsi(pesan, pilihan):
    jawaban = inquirer.prompt([
        inquirer.List("pilihan", message=pesan, choices=pilihan)
    ])

    if jawaban is None:
        raise KeyboardInterrupt

    return jawaban["pilihan"]


def pilih_kategori():
    return pilih_opsi("Pilih kategori", list(KATEGORI))


# ==========================================
# 3. FUNGSI SORTING (BUBBLE SORT)
# ==========================================

def bubble_sort(data, atribut, menurun=False):
    hasil = data.copy()

    for i in range(len(hasil) - 1):
        tertukar = False

        for j in range(len(hasil) - i - 1):
            kiri = hasil[j][atribut]
            kanan = hasil[j + 1][atribut]

            if isinstance(kiri, str):
                kiri = kiri.lower()
                kanan = kanan.lower()

            if (not menurun and kiri > kanan) or (menurun and kiri < kanan):
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
                tertukar = True

        if not tertukar:
            break

    return hasil


# ==========================================
# 4. FUNGSI SEARCHING (BINARY SEARCH)
# ==========================================

def cari_kode(kode):
    data = bubble_sort(daftar_menu, "kode")

    kode = kode.strip().upper()
    bawah = 0
    atas = len(data) - 1

    while bawah <= atas:
        tengah = (bawah + atas) // 2

        if data[tengah]["kode"] == kode:
            return data[tengah]

        elif data[tengah]["kode"] < kode:
            bawah = tengah + 1

        else:
            atas = tengah - 1

    return None


# ==========================================
# 5. FUNGSI MENAMPILKAN MENU
# ==========================================

def tampilkan_menu(data):
    if not data:
        print("Tidak ada menu yang dapat ditampilkan.")
        return

    # Mengurutkan berdasarkan kategori
    urutan_menu = sorted(
        data,
        key=lambda x: KATEGORI.index(x["kategori"])
    )

    tabel = PrettyTable()
    tabel.title = "DAFTAR MENU"
    tabel.field_names = ["Kode", "Nama Menu", "Kategori", "Harga"]
    tabel.align = "l"
    tabel.align["Harga"] = "r"
    tabel.max_width["Nama Menu"] = 28

    for menu in urutan_menu:
        tabel.add_row([
            menu["kode"],
            menu["nama"],
            menu["kategori"],
            rupiah(menu["harga"])
        ])

    print(tabel)


# ==========================================
# 6. CREATE (MENAMBAHKAN MENU)
# ==========================================

def tambah_menu():
    while True:
        kode = input_teks("Kode menu (contoh M05): ").upper()

        if not kode.isascii() or not kode.isalnum():
            print("Kode hanya boleh berisi huruf A-Z dan angka 0-9.")

        elif cari_kode(kode) is not None:
            print("Kode sudah digunakan.")

        else:
            break

    nama = input_teks("Nama menu: ").title()
    kategori = pilih_kategori()
    harga = input_angka("Harga (Rp): ", 1)

    daftar_menu.append({
        "kode": kode,
        "nama": nama,
        "kategori": kategori,
        "harga": harga
    })

    print("Menu berhasil ditambahkan.")


# ==========================================
# 7. UPDATE (MENGUBAH MENU)
# ==========================================

def ubah_menu():
    tampilkan_menu(daftar_menu)

    if not daftar_menu:
        return

    menu = cari_kode(input_teks("Kode menu yang diubah: "))

    if menu is None:
        print("Kode tidak ditemukan.")
        return

    nama = input_teks("Nama baru: ").title()
    kategori = pilih_kategori()
    harga = input_angka("Harga baru (Rp): ", 1)

    menu.update({
        "nama": nama,
        "kategori": kategori,
        "harga": harga
    })

    print("Menu berhasil diubah. Kode menu tetap.")


# ==========================================
# 8. DELETE (MENGHAPUS MENU)
# ==========================================

def hapus_menu():
    tampilkan_menu(daftar_menu)

    if not daftar_menu:
        return

    menu = cari_kode(input_teks("Kode menu yang dihapus: "))

    if menu is None:
        print("Kode tidak ditemukan.")
        return

    print(f"Hapus {menu['nama']}?")

    konfirmasi = pilih_opsi(
        "Konfirmasi hapus",
        [("Batal", 0), ("Ya, hapus", 1)]
    )

    if konfirmasi == 1:
        daftar_menu.remove(menu)
        print("Menu berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")


# ==========================================
# 9. FUNGSI PENCARIAN MENU
# ==========================================

def cari_menu():
    pilihan = pilih_opsi(
        "Pilih pencarian",
        [("Kode (Binary Search)", 1), ("Sebagian nama", 2)]
    )

    if pilihan == 1:
        menu = cari_kode(input_teks("Kode menu: "))
        hasil = [menu] if menu is not None else []

    else:
        kata = input_teks("Nama menu: ").lower()
        hasil = []

        for menu in daftar_menu:
            if kata in menu["nama"].lower():
                hasil.append(menu)

    tampilkan_menu(hasil)


# ==========================================
# 10. FUNGSI SORTING MENU
# ==========================================

def urutkan_menu():
    pilihan = pilih_opsi(
        "Urutkan berdasarkan",
        [("Nama", 1), ("Harga", 2)]
    )

    atribut = "nama" if pilihan == 1 else "harga"

    menurun = pilih_opsi(
        "Pilih urutan",
        [
            ("Menaik (A-Z / termurah)", False),
            ("Menurun (Z-A / termahal)", True)
        ]
    )

    hasil = bubble_sort(daftar_menu, atribut, menurun)

    tampilkan_menu(hasil)


# ==========================================
# 11. PERHITUNGAN TOTAL DAN DISKON
# ==========================================

def hitung_total(pesanan):
    subtotal = 0

    for item in pesanan:
        subtotal += item["harga"] * item["jumlah"]

    diskon = (
        round(subtotal * PERSEN_DISKON)
        if subtotal >= BATAS_DISKON
        else 0
    )

    return subtotal, diskon, subtotal - diskon


# ==========================================
# 12. MENAMPILKAN PESANAN
# ==========================================

def tampilkan_pesanan(pesanan):
    tabel = PrettyTable()

    tabel.field_names = ["Menu", "Jumlah", "Harga", "Total"]
    tabel.align["Menu"] = "l"
    tabel.max_width["Menu"] = 28

    for item in pesanan:
        total_item = item["harga"] * item["jumlah"]

        tabel.add_row([
            item["nama"],
            item["jumlah"],
            rupiah(item["harga"]),
            rupiah(total_item)
        ])

    print(tabel)

    subtotal, diskon, total = hitung_total(pesanan)

    ringkasan = PrettyTable(["Informasi", "Nominal"])
    ringkasan.align = "l"

    ringkasan.add_rows([
        ["Subtotal", rupiah(subtotal)],
        ["Diskon", rupiah(diskon)],
        ["Total bayar", rupiah(total)]
    ])

    print(ringkasan)


# ==========================================
# 13. MEMBUAT PESANAN
# ==========================================

def buat_pesanan():
    if not daftar_menu:
        print("Tambahkan menu terlebih dahulu.")
        return

    pelanggan = input_teks("Nama pelanggan: ").title()
    pesanan = []

    while True:
        tampilkan_menu(daftar_menu)

        pilihan = pilih_opsi(
            "Pesanan",
            [
                ("Tambah item", 1),
                ("Bayar", 2),
                ("Batalkan pesanan", 0)
            ]
        )

        if pilihan == 0:
            print("Pesanan dibatalkan. Tidak dicatat sebagai penjualan.")
            return

        elif pilihan == 1:
            menu = cari_kode(input_teks("Kode menu: "))

            if menu is None:
                print("Kode tidak ditemukan.")
                continue

            jumlah = input_angka("Jumlah pesanan: ", 1)
            ditemukan = False

            for item in pesanan:
                if item["kode"] == menu["kode"]:
                    item["jumlah"] += jumlah
                    ditemukan = True
                    break

            if not ditemukan:
                item = menu.copy()
                item["jumlah"] = jumlah
                pesanan.append(item)

            tampilkan_pesanan(pesanan)

        else:
            if not pesanan:
                print("Pesanan masih kosong.")
                continue

            tampilkan_pesanan(pesanan)

            subtotal, diskon, total = hitung_total(pesanan)

            while True:
                bayar = input_angka(
                    "Uang pembayaran (0 untuk batal): ", 0
                )

                if bayar == 0:
                    print("Pesanan dibatalkan.")
                    return

                if bayar >= total:
                    break

                print("Uang pembayaran belum cukup.")

            transaksi = {
                "nomor": len(riwayat_transaksi) + 1,
                "pelanggan": pelanggan,
                "pesanan": pesanan,
                "subtotal": subtotal,
                "diskon": diskon,
                "total": total,
                "bayar": bayar,
                "kembalian": bayar - total
            }

            riwayat_transaksi.append(transaksi)

            print(f"\nSTRUK #{transaksi['nomor']} | {pelanggan}")

            tampilkan_pesanan(pesanan)

            print(f"Bayar    : {rupiah(bayar)}")
            print(f"Kembalian: {rupiah(transaksi['kembalian'])}")
            print("Transaksi berhasil. Terima kasih!")

            return


# ==========================================
# 14. LAPORAN PENJUALAN
# ==========================================

def laporan_penjualan():
    if not riwayat_transaksi:
        print("Belum ada transaksi berhasil.")
        return

    omzet_kotor = 0
    total_diskon = 0
    pendapatan = 0
    jumlah_item = 0

    kategori_terjual = set()

    print("\nLAPORAN PENJUALAN")

    for transaksi in riwayat_transaksi:
        print(f"\n#{transaksi['nomor']} | {transaksi['pelanggan']}")

        tampilkan_pesanan(transaksi["pesanan"])

        omzet_kotor += transaksi["subtotal"]
        total_diskon += transaksi["diskon"]
        pendapatan += transaksi["total"]

        for item in transaksi["pesanan"]:
            jumlah_item += item["jumlah"]
            kategori_terjual.add(item["kategori"])

    ringkasan = PrettyTable(["Informasi", "Hasil"])
    ringkasan.align = "l"

    ringkasan.add_rows([
        ["Jumlah transaksi", len(riwayat_transaksi)],
        ["Jumlah item", jumlah_item],
        ["Omzet kotor", rupiah(omzet_kotor)],
        ["Total diskon", rupiah(total_diskon)],
        ["Pendapatan", rupiah(pendapatan)],
        [
            "Kategori terjual",
            ", ".join(k for k in KATEGORI if k in kategori_terjual)
        ]
    ])

    print(ringkasan)


# ==========================================
# 15. CLEAR TERMINAL
# ==========================================

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# 16. MENU UTAMA
# ==========================================

def main():
    berjalan = True

    while berjalan:
        clear_terminal()

        print("Data tersimpan selama program berjalan saja.")
        print("Diskon 10% untuk subtotal minimal Rp100.000.")
        print("\n=== SISTEM PENJUALAN MAKANAN ===")

        pilihan = pilih_opsi(
            "Pilih menu (panah atas/bawah, lalu Enter)",
            [
                ("1. Tambah menu", 1),
                ("2. Tampilkan menu", 2),
                ("3. Ubah menu", 3),
                ("4. Hapus menu", 4),
                ("5. Cari menu", 5),
                ("6. Urutkan menu", 6),
                ("7. Buat pesanan", 7),
                ("8. Laporan penjualan", 8),
                ("9. Keluar", 9)
            ]
        )

        if pilihan == 1:
            tambah_menu()

        elif pilihan == 2:
            tampilkan_menu(daftar_menu)

        elif pilihan == 3:
            ubah_menu()

        elif pilihan == 4:
            hapus_menu()

        elif pilihan == 5:
            cari_menu()

        elif pilihan == 6:
            urutkan_menu()

        elif pilihan == 7:
            buat_pesanan()

        elif pilihan == 8:
            laporan_penjualan()

        else:
            berjalan = False
            print("Program selesai. Data sesi ini tidak disimpan ke file.")

        if berjalan:
            input("\nTekan Enter untuk kembali ke menu utama...")


# ==========================================
# 17. MENJALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    if not sys.stdin.isatty():
        print("Jalankan program di Terminal VS Code, bukan panel Output.")
        print("Perintah: python penjualan_makanan.py")
        raise SystemExit(1)

    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan. Data sesi ini tidak disimpan ke file.")