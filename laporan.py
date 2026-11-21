from prettytable import PrettyTable

from data import riwayat_transaksi, KATEGORI
from input_utils import rupiah


def laporan_penjualan():
    print("\n=== LAPORAN PENJUALAN ===")

    if not riwayat_transaksi:
        print("Belum ada transaksi!")
        return

    total_transaksi = len(riwayat_transaksi)
    total_barang = 0
    omzet = 0
    total_diskon = 0
    pendapatan = 0

    kategori_terjual = set()

    tabel = PrettyTable()

    tabel.field_names = [
        "Pelanggan",
        "Barang",
        "Subtotal",
        "Diskon",
        "Total"
    ]

    for transaksi in riwayat_transaksi:

        jumlah_barang_transaksi = sum(
            item["jumlah"]
            for item in transaksi["items"]
        )

        total_barang += jumlah_barang_transaksi
        omzet += transaksi["subtotal"]
        total_diskon += transaksi["diskon"]
        pendapatan += transaksi["total"]

        for item in transaksi["items"]:

            for kategori in KATEGORI:
                if kategori == "Makanan":
                    nama_makanan = [
                        menu["nama"]
                        for menu in []
                    ]

                # Mengambil kategori dari katalog saat ini
                from data import daftar_menu

                for menu in daftar_menu:
                    if menu["nama"] == item["nama"]:
                        kategori_terjual.add(menu["kategori"])

        tabel.add_row([
            transaksi["pelanggan"],
            jumlah_barang_transaksi,
            rupiah(transaksi["subtotal"]),
            rupiah(transaksi["diskon"]),
            rupiah(transaksi["total"])
        ])

    print(tabel)

    print("\n=== RINGKASAN ===")
    print("Jumlah transaksi :", total_transaksi)
    print("Jumlah barang   :", total_barang)
    print("Omzet           :", rupiah(omzet))
    print("Total diskon    :", rupiah(total_diskon))
    print("Pendapatan      :", rupiah(pendapatan))

    print(
        "Kategori terjual:",
        kategori_terjual
    )