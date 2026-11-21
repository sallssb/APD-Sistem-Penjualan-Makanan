import os
import sys

try:
    from prettytable import PrettyTable
    import inquirer

except ModuleNotFoundError:
    print("Library belum terpasang.")
    print("Jalankan perintah berikut di terminal:")
    print(
        f'"{sys.executable}" '
        '-m pip install prettytable inquirer'
    )

    raise SystemExit(1)


from menu import (
    tambah_menu,
    tampilkan_menu,
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


def main():
    berjalan = True

    while berjalan:
        clear_terminal()

        print(
            "Diskon 10% untuk subtotal minimal Rp100.000."
        )

        print(
            "\n=== SISTEM PENJUALAN MAKANAN ==="
        )

        pilihan = inquirer.prompt([
            inquirer.List(
                "pilihan",
                message=(
                    "Pilih menu "
                    "(panah atas/bawah, lalu Enter)"
                ),
                choices=[
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
        ])

        if pilihan is None:
            raise KeyboardInterrupt

        pilihan = pilihan["pilihan"]

        if pilihan == 1:
            tambah_menu()

        elif pilihan == 2:
            tampilkan_menu(
                __import__("data").daftar_menu
            )

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

        elif pilihan == 9:
            berjalan = False

            print(
                "Program selesai. "
                "Data sesi ini tidak disimpan ke file."
            )

        if berjalan:
            input(
                "\nTekan Enter untuk kembali "
                "ke menu utama..."
            )


if __name__ == "__main__":

    if not sys.stdin.isatty():
        print(
            "Jalankan program di Terminal VS Code, "
            "bukan panel Output."
        )

        print(
            "Perintah: python main.py"
        )

        raise SystemExit(1)

    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print(
            "\nProgram dihentikan. "
        )