import os

from input_utils import pilih_opsi

from menu import (
    tampilkan_menu,
    tambah_menu,
    ubah_menu,
    hapus_menu,
    cari_menu,
    urutkan_menu
)

from pesanan import buat_pesanan
from laporan import laporan_penjualan


def clear_terminal():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )


def menu_utama():
    while True:

        pilihan = pilih_opsi(
            "=== PROGRAM PENJUALAN MAKANAN ===",
            [
                "Tampilkan Menu",
                "Tambah Menu",
                "Ubah Menu",
                "Hapus Menu",
                "Cari Menu",
                "Urutkan Menu",
                "Buat Pesanan",
                "Laporan Penjualan",
                "Keluar"
            ]
        )

        if pilihan is None or pilihan == "Keluar":
            print("\nTerima kasih telah menggunakan program!")
            break

        elif pilihan == "Tampilkan Menu":
            tampilkan_menu()

        elif pilihan == "Tambah Menu":
            tambah_menu()

        elif pilihan == "Ubah Menu":
            ubah_menu()

        elif pilihan == "Hapus Menu":
            hapus_menu()

        elif pilihan == "Cari Menu":
            cari_menu()

        elif pilihan == "Urutkan Menu":
            urutkan_menu()

        elif pilihan == "Buat Pesanan":
            buat_pesanan()

        elif pilihan == "Laporan Penjualan":
            laporan_penjualan()


if __name__ == "__main__":
    menu_utama()