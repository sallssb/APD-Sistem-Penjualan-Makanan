from utils import (
    tampilkanHeader, bersihkanLayar, cetakTabel, formatRupiah,
    pilih, tekanEnter,
)
from menuMakanan import statusStok


def hitungRingkasan(riwayat):
    totalPendapatan = 0
    totalDiskon = 0
    totalItem = 0
    for trx in riwayat:
        totalPendapatan += trx["total"]
        totalDiskon += trx["diskon"]
        for item in trx["items"]:
            totalItem += item["jumlah"]

    jumlah = len(riwayat)
    return {
        "jumlahTransaksi": jumlah,
        "pendapatan": totalPendapatan,
        "diskon": totalDiskon,
        "itemTerjual": totalItem,
        "rataRata": totalPendapatan // jumlah if jumlah else 0,
    }


def hitungPenjualanPerMenu(riwayat):
    hasil = {}
    for trx in riwayat:
        for item in trx["items"]:
            kode = item["kode"]
            if kode not in hasil:
                hasil[kode] = {"nama": item["nama"], "jumlah": 0, "omzet": 0}
            hasil[kode]["jumlah"] += item["jumlah"]
            hasil[kode]["omzet"] += item["subtotal"]
    return hasil


def tampilRingkasan(riwayat):
    r = hitungRingkasan(riwayat)
    baris = [
        ["Jumlah transaksi", r["jumlahTransaksi"]],
        ["Total item terjual", r["itemTerjual"]],
        ["Total diskon diberikan", formatRupiah(r["diskon"])],
        ["Total pendapatan", formatRupiah(r["pendapatan"])],
        ["Rata-rata per transaksi", formatRupiah(r["rataRata"])],
    ]
    cetakTabel("Ringkasan Penjualan", ["Keterangan", "Nilai"],
               baris, kolomKanan=("Nilai",))


def tampilRiwayat(riwayat):
    baris = []
    for trx in riwayat:
        jumlahItem = sum(item["jumlah"] for item in trx["items"])
        baris.append([trx["id"], trx["waktu"], trx["tipe"], trx["metode"],
                      jumlahItem, formatRupiah(trx["diskon"]),
                      formatRupiah(trx["total"])])
    cetakTabel("Riwayat Transaksi",
               ["ID", "Waktu", "Tipe", "Metode", "Item", "Diskon", "Total"],
               baris, kolomKanan=("Item", "Diskon", "Total"))


def tampilTerlaris(menu, riwayat):
    perMenu = hitungPenjualanPerMenu(riwayat)
    urut = sorted(perMenu.items(), key=lambda x: x[1]["jumlah"], reverse=True)
    baris = []
    for peringkat, (kode, data) in enumerate(urut, start=1):
        baris.append([peringkat, kode, data["nama"], data["jumlah"],
                      formatRupiah(data["omzet"])])
    cetakTabel("Menu Terlaris", ["#", "Kode", "Nama Menu", "Terjual", "Omzet"],
               baris, kolomKanan=("#", "Terjual", "Omzet"))

    belumLaku = set(menu.keys()) - set(perMenu.keys())
    if belumLaku:
        nama = ", ".join(menu[k]["nama"] for k in sorted(belumLaku))
        print(f"Belum pernah terjual: {nama}\n")


def tampilStok(menu):
    baris = []
    for kode, info in menu.items():
        baris.append([kode, info["nama"], info["stok"], statusStok(info["stok"])])
    cetakTabel("Laporan Stok", ["Kode", "Nama Menu", "Stok", "Status"],
               baris, kolomKanan=("Stok",))


def laporanPenjualan(menu, riwayat):
    while True:
        bersihkanLayar()
        tampilkanHeader("Laporan Penjualan")
        jenis = pilih("Pilih laporan", [
            ("Ringkasan penjualan", "ringkasan"),
            ("Riwayat transaksi", "riwayat"),
            ("Menu terlaris", "terlaris"),
            ("Laporan stok", "stok"),
            ("<< Kembali", None),
        ])
        if jenis is None:
            return

        bersihkanLayar()
        tampilkanHeader("Laporan Penjualan")
        if jenis != "stok" and not riwayat:
            print("\nBelum ada transaksi.")
        elif jenis == "ringkasan":
            tampilRingkasan(riwayat)
        elif jenis == "riwayat":
            tampilRiwayat(riwayat)
        elif jenis == "terlaris":
            tampilTerlaris(menu, riwayat)
        elif jenis == "stok":
            tampilStok(menu)
        tekanEnter()