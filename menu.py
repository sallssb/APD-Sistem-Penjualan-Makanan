# ==========================================
# CRUD MENU
# ==========================================

from prettytable import PrettyTable

from data import daftar_menu, KATEGORI
from input_utils import (
    rupiah,
    input_teks,
    input_angka,
    pilih_opsi,
    pilih_kategori
)

from sorting_search import bubble_sort, cari_kode


# ==========================================
# MENAMPILKAN MENU
# ==========================================

def tampilkan_menu(data):
    if not data:
        print("Tidak ada menu yang dapat ditampilkan.")
        return

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
# CREATE
# ==========================================

def tambah_menu():
    while True:
        kode = input_teks(
            "Kode menu (contoh M05): "
        ).upper()

        if not kode.isascii() or not kode.isalnum():
            print(
                "Kode hanya boleh berisi huruf A-Z "
                "dan angka 0-9."
            )

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
# UPDATE
# ==========================================

def ubah_menu():
    tampilkan_menu(daftar_menu)

    if not daftar_menu:
        return

    menu = cari_kode(
        input_teks("Kode menu yang diubah: ")
    )

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
# DELETE
# ==========================================

def hapus_menu():
    tampilkan_menu(daftar_menu)

    if not daftar_menu:
        return

    menu = cari_kode(
        input_teks("Kode menu yang dihapus: ")
    )

    if menu is None:
        print("Kode tidak ditemukan.")
        return

    print(f"Hapus {menu['nama']}?")

    konfirmasi = pilih_opsi(
        "Konfirmasi hapus",
        [
            ("Batal", 0),
            ("Ya, hapus", 1)
        ]
    )

    if konfirmasi == 1:
        daftar_menu.remove(menu)
        print("Menu berhasil dihapus.")

    else:
        print("Penghapusan dibatalkan.")


# ==========================================
# PENCARIAN MENU
# ==========================================

def cari_menu():
    pilihan = pilih_opsi(
        "Pilih pencarian",
        [
            ("Kode (Binary Search)", 1),
            ("Sebagian nama", 2)
        ]
    )

    if pilihan == 1:
        menu = cari_kode(
            input_teks("Kode menu: ")
        )

        hasil = [menu] if menu is not None else []

    else:
        kata = input_teks(
            "Nama menu: "
        ).lower()

        hasil = []

        for menu in daftar_menu:
            if kata in menu["nama"].lower():
                hasil.append(menu)

    tampilkan_menu(hasil)


# ==========================================
# SORTING MENU
# ==========================================

def urutkan_menu():
    pilihan = pilih_opsi(
        "Urutkan berdasarkan",
        [
            ("Nama", 1),
            ("Harga", 2)
        ]
    )

    atribut = "nama" if pilihan == 1 else "harga"

    menurun = pilih_opsi(
        "Pilih urutan",
        [
            ("Menaik (A-Z / termurah)", False),
            ("Menurun (Z-A / termahal)", True)
        ]
    )

    hasil = bubble_sort(
        daftar_menu,
        atribut,
        menurun
    )

    tampilkan_menu(hasil)