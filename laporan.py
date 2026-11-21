# ==========================================
# LAPORAN PENJUALAN
# ==========================================

from prettytable import PrettyTable

from data import (
    riwayat_transaksi,
    KATEGORI
)

from input_utils import rupiah
from pesanan import tampilkan_pesanan


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
        print(
            f"\n#{transaksi['nomor']} "
            f"| {transaksi['pelanggan']}"
        )

        tampilkan_pesanan(
            transaksi["pesanan"]
        )

        omzet_kotor += transaksi["subtotal"]
        total_diskon += transaksi["diskon"]
        pendapatan += transaksi["total"]

        for item in transaksi["pesanan"]:
            jumlah_item += item["jumlah"]

            kategori_terjual.add(
                item["kategori"]
            )

    ringkasan = PrettyTable(
        ["Informasi", "Hasil"]
    )

    ringkasan.align = "l"

    ringkasan.add_rows([
        [
            "Jumlah transaksi",
            len(riwayat_transaksi)
        ],
        [
            "Jumlah item",
            jumlah_item
        ],
        [
            "Omzet kotor",
            rupiah(omzet_kotor)
        ],
        [
            "Total diskon",
            rupiah(total_diskon)
        ],
        [
            "Pendapatan",
            rupiah(pendapatan)
        ],
        [
            "Kategori terjual",
            ", ".join(
                k for k in KATEGORI
                if k in kategori_terjual
            )
        ]
    ])

    print(ringkasan)