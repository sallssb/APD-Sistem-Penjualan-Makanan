from prettytable import PrettyTable

from data import daftar_menu

from input_utils import (
    rupiah,
    input_teks,
    input_angka,
    pilih_kategori,
    pilih_opsi
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

    kode = input_teks(
        "Masukkan kode menu: "
    ).upper()

    if cari_kode(kode) is not None:
        print("Kode menu sudah digunakan!")
        return

    nama = input_teks(
        "Masukkan nama menu: "
    )

    kategori = pilih_kategori()

    if kategori is None:
        return

    harga = input_angka(
        "Masukkan harga: ",
        minimal=1
    )

    stok = input_angka(
        "Masukkan stok: ",
        minimal=0
    )

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

    kode = input_teks(
        "Masukkan kode menu: "
    ).upper()

    menu = cari_kode(kode)

    if menu is None:
        print("Menu tidak ditemukan!")
        return

    tampilkan_menu([menu])

    pilihan = pilih_opsi(
        "Pilih data yang ingin diubah:",
        [
            "Nama",
            "Kategori",
            "Harga",
            "Stok",
            "Semua data",
            "Kembali"
        ]
    )

    if pilihan == "Nama":
        menu["nama"] = input_teks(
            "Nama baru: "
        )

    elif pilihan == "Kategori":
        kategori = pilih_kategori()

        if kategori is not None:
            menu["kategori"] = kategori

    elif pilihan == "Harga":
        menu["harga"] = input_angka(
            "Harga baru: ",
            minimal=1
        )

    elif pilihan == "Stok":
        menu["stok"] = input_angka(
            "Stok baru: ",
            minimal=0
        )

    elif pilihan == "Semua data":
        menu["nama"] = input_teks(
            "Nama baru: "
        )

        kategori = pilih_kategori()

        if kategori is not None:
            menu["kategori"] = kategori

        menu["harga"] = input_angka(
            "Harga baru: ",
            minimal=1
        )

        menu["stok"] = input_angka(
            "Stok baru: ",
            minimal=0
        )

    elif pilihan == "Kembali" or pilihan is None:
        return

    print("Menu berhasil diperbarui!")


def hapus_menu():
    print("\n=== HAPUS MENU ===")

    kode = input_teks(
        "Masukkan kode menu: "
    ).upper()

    menu = cari_kode(kode)

    if menu is None:
        print("Menu tidak ditemukan!")
        return

    tampilkan_menu([menu])

    konfirmasi = pilih_opsi(
        "Apakah menu ingin dihapus?",
        ["Ya", "Tidak", "Kembali"]
    )

    if konfirmasi == "Ya":
        daftar_menu.remove(menu)
        print("Menu berhasil dihapus!")

    else:
        print("Penghapusan dibatalkan!")


def cari_menu():
    print("\n=== CARI MENU ===")

    pilihan = pilih_opsi(
        "Pilih metode pencarian:",
        [
            "Berdasarkan kode",
            "Berdasarkan nama",
            "Kembali"
        ]
    )

    if pilihan == "Berdasarkan kode":

        kode = input_teks(
            "Masukkan kode menu: "
        ).upper()

        hasil = cari_kode(kode)

        if hasil:
            tampilkan_menu([hasil])
        else:
            print("Menu tidak ditemukan!")

    elif pilihan == "Berdasarkan nama":

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


def urutkan_menu():
    print("\n=== URUTKAN MENU ===")

    atribut = pilih_opsi(
        "Pilih dasar pengurutan:",
        [
            "Nama",
            "Harga",
            "Stok",
            "Kembali"
        ]
    )

    if atribut is None or atribut == "Kembali":
        return

    if atribut == "Nama":
        kolom = "nama"

    elif atribut == "Harga":
        kolom = "harga"

    else:
        kolom = "stok"

    arah = pilih_opsi(
        "Pilih urutan:",
        [
            "Ascending",
            "Descending",
            "Kembali"
        ]
    )

    if arah is None or arah == "Kembali":
        return

    hasil = bubble_sort(
        daftar_menu,
        kolom,
        menurun=(arah == "Descending")
    )

    tampilkan_menu(hasil)