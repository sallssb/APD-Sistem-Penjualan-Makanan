# ==========================================
# PESANAN DAN PEMBAYARAN
# ==========================================

from prettytable import PrettyTable

from data import (
    daftar_menu,
    riwayat_transaksi,
    PERSEN_DISKON,
    BATAS_DISKON
)

from input_utils import (
    rupiah,
    input_teks,
    input_angka,
    pilih_opsi
)

from sorting_search import cari_kode
from menu import tampilkan_menu


# ==========================================
# PERHITUNGAN TOTAL DAN DISKON
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
# MENAMPILKAN PESANAN
# ==========================================

def tampilkan_pesanan(pesanan):
    tabel = PrettyTable()

    tabel.field_names = [
        "Menu", "Jumlah", "Harga", "Total"
    ]

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

    ringkasan = PrettyTable(
        ["Informasi", "Nominal"]
    )

    ringkasan.align = "l"

    ringkasan.add_rows([
        ["Subtotal", rupiah(subtotal)],
        ["Diskon", rupiah(diskon)],
        ["Total bayar", rupiah(total)]
    ])

    print(ringkasan)


# ==========================================
# MEMBUAT PESANAN
# ==========================================

def buat_pesanan():
    if not daftar_menu:
        print("Tambahkan menu terlebih dahulu.")
        return

    pelanggan = input_teks(
        "Nama pelanggan: "
    ).title()

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
            print(
                "Pesanan dibatalkan. "
                "Tidak dicatat sebagai penjualan."
            )

            return

        elif pilihan == 1:
            menu = cari_kode(
                input_teks("Kode menu: ")
            )

            if menu is None:
                print("Kode tidak ditemukan.")
                continue

            jumlah = input_angka(
                "Jumlah pesanan: ", 1
            )

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

            subtotal, diskon, total = hitung_total(
                pesanan
            )

            while True:
                bayar = input_angka(
                    "Uang pembayaran (0 untuk batal): ",
                    0
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

            print(
                f"\nSTRUK #{transaksi['nomor']} "
                f"| {pelanggan}"
            )

            tampilkan_pesanan(pesanan)

            print(f"Bayar    : {rupiah(bayar)}")
            print(
                f"Kembalian: "
                f"{rupiah(transaksi['kembalian'])}"
            )

            print(
                "Transaksi berhasil. Terima kasih!"
            )

            return