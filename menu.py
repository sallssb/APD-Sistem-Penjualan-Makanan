from prettytable import PrettyTable

from data import daftar_menu
from input_utils import (
    rupiah,
    input_teks,
    input_angka,
    pilih_kategori
)
from sorting_search import bubble_sort, cari_kode


def tampilkan_menu(data=None):
    if data is None:
        data = daftar_menu

    tabel = PrettyTable()

    tabel.field_names = [
        "Kode",
        "Nama",
        "Kategori",
        "Harga",
        "Stok"
    ]

    for menu in data:
        tabel.add_row([
            menu["kode"],
            menu["nama"],
            menu["kategori"],
            rupiah(menu["harga"]),
            menu["stok"]
        ])

    print(tabel)


def tambah_menu():
    print("\n=== TAMBAH MENU ===")

    kode = input_teks("Masukkan kode menu: ").upper()

    if cari_kode(kode) is not None:
        print("Kode menu sudah digunakan!")
        return

    nama = input_teks("Masukkan nama menu: ")
    kategori = pilih_kategori()
    harga = input_angka("Masukkan harga: ", minimal=1)
    stok = input_angka("Masukkan stok: ", minimal=0)

    menu_baru = {
        "kode": kode,
        "nama": nama,
        "kategori": kategori,
        "harga": harga,
        "stok": stok
    }

    daftar_menu.append(menu_baru)

    print("Menu berhasil ditambahkan!")


def ubah_menu():
    print("\n=== UBAH MENU ===")

    kode = input_teks("Masukkan kode menu: ").upper()
    menu = cari_kode(kode)

    if menu is None:
        print("Menu tidak ditemukan!")
        return

    print("\nData menu saat ini:")
    tampilkan_menu([menu])

    pilihan = input_teks(
        "Ubah (1) Nama, (2) Kategori, "
        "(3) Harga, (4) Stok, (5) Semua: "
    )

    if pilihan == "1":
        menu["nama"] = input_teks("Nama baru: ")

    elif pilihan == "2":
        menu["kategori"] = pilih_kategori()

    elif pilihan == "3":
        menu["harga"] = input_angka(
            "Harga baru: ", minimal=1
        )

    elif pilihan == "4":
        menu["stok"] = input_angka(
            "Stok baru: ", minimal=0
        )

    elif pilihan == "5":
        menu["nama"] = input_teks("Nama baru: ")
        menu["kategori"] = pilih_kategori()
        menu["harga"] = input_angka(
            "Harga baru: ", minimal=1
        )
        menu["stok"] = input_angka(
            "Stok baru: ", minimal=0
        )

    else:
        print("Pilihan tidak valid!")
        return

    print("Menu berhasil diperbarui!")


def hapus_menu():
    print("\n=== HAPUS MENU ===")

    kode = input_teks("Masukkan kode menu: ").upper()
    menu = cari_kode(kode)

    if menu is None:
        print("Menu tidak ditemukan!")
        return

    tampilkan_menu([menu])

    konfirmasi = input_teks(
        "Yakin ingin menghapus menu? (y/n): "
    ).lower()

    if konfirmasi == "y":
        daftar_menu.remove(menu)
        print("Menu berhasil dihapus!")

    else:
        print("Penghapusan dibatalkan!")


def cari_menu():
    print("\n=== CARI MENU ===")

    pilihan = input_teks(
        "1. Cari berdasarkan kode\n"
        "2. Cari berdasarkan nama\n"
        "Pilihan: "
    )

    if pilihan == "1":
        kode = input_teks(
            "Masukkan kode menu: "
        ).upper()

        hasil = cari_kode(kode)

        if hasil:
            tampilkan_menu([hasil])
        else:
            print("Menu tidak ditemukan!")

    elif pilihan == "2":
        nama = input_teks(
            "Masukkan nama menu: "
        ).lower()

        hasil = [
            menu for menu in daftar_menu
            if nama in menu["nama"].lower()
        ]

        if hasil:
            tampilkan_menu(hasil)
        else:
            print("Menu tidak ditemukan!")

    else:
        print("Pilihan tidak valid!")


def urutkan_menu():
    print("\n=== URUTKAN MENU ===")

    pilihan = input_teks(
        "1. Berdasarkan nama\n"
        "2. Berdasarkan harga\n"
        "3. Berdasarkan stok\n"
        "Pilihan: "
    )

    if pilihan == "1":
        atribut = "nama"

    elif pilihan == "2":
        atribut = "harga"

    elif pilihan == "3":
        atribut = "stok"

    else:
        print("Pilihan tidak valid!")
        return

    arah = input_teks(
        "1. Ascending\n"
        "2. Descending\n"
        "Pilihan: "
    )

    if arah not in ("1", "2"):
        print("Pilihan tidak valid!")
        return

    hasil = bubble_sort(
        daftar_menu,
        atribut,
        menurun=(arah == "2")
    )

    tampilkan_menu(hasil)