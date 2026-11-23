from utils import bersihkanLayar, tampilkanHeader, pilih, konfirmasi
from menuMakanan import (
    buatDataAwal, tambahMenu, tampilkanMenu, ubahMenu,
    hapusMenu, cariMenu, urutkanMenu,
)
from transaksi import transaksiPenjualan
from laporan import laporanPenjualan


def tampilkanMenuUtama():
    bersihkanLayar()
    tampilkanHeader("Menu Utama")
    return pilih("Pilih Menu", [
        ("1. Tambah Menu", 1),
        ("2. Tampilkan Menu", 2),
        ("3. Ubah Data Menu", 3),
        ("4. Hapus Menu", 4),
        ("5. Cari Menu", 5),
        ("6. Urutkan Menu", 6),
        ("7. Transaksi Penjualan", 7),
        ("8. Laporan Penjualan", 8),
        ("9. Keluar", 9),
    ])


def main():
    menu = buatDataAwal()   
    riwayat = []            

    while True:
        pilihan = tampilkanMenuUtama()

        if pilihan == 1:
            tambahMenu(menu)
        elif pilihan == 2:
            tampilkanMenu(menu)
        elif pilihan == 3:
            ubahMenu(menu)
        elif pilihan == 4:
            hapusMenu(menu)
        elif pilihan == 5:
            cariMenu(menu)
        elif pilihan == 6:
            urutkanMenu(menu)
        elif pilihan == 7:
            transaksiPenjualan(menu, riwayat)
        elif pilihan == 8:
            laporanPenjualan(menu, riwayat)
        elif pilihan == 9 or pilihan is None:
            if konfirmasi("Yakin ingin keluar dari program?"):
                bersihkanLayar()
                print("Terima kasih telah menggunakan aplikasi ini!")
                break


if __name__ == "__main__":
    main()