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
    input_angka
)

from sorting_search import cari_kode
from menu import tampilkan_menu


def hitung_total(pesanan):
    subtotal = sum(
        item["menu"]["harga"] * item["jumlah"]
        for item in pesanan
    )

    if subtotal >= BATAS_DISKON:
        diskon = subtotal * PERSEN_DISKON
    else:
        diskon = 0

    total = subtotal - diskon

    return subtotal, diskon, total


def tampilkan_pesanan(pesanan):
    tabel = PrettyTable()

    tabel.field_names = [
        "Nama",
        "Harga",
        "Jumlah",
        "Subtotal"
    ]

    for item in pesanan:
        menu = item["menu"]
        jumlah = item["jumlah"]

        subtotal_item = menu["harga"] * jumlah

        tabel.add_row([
            menu["nama"],
            rupiah(menu["harga"]),
            jumlah,
            rupiah(subtotal_item)
        ])

    print(tabel)


def buat_pesanan():
    print("\n=== PEMESANAN MAKANAN ===")

    nama_pelanggan = input_teks(
        "Nama pelanggan: "
    )

    pesanan = []

    while True:
        print("\nDaftar menu tersedia:")

        menu_tersedia = [
            menu for menu in daftar_menu
            if menu["stok"] > 0
        ]

        if not menu_tersedia:
            print("Tidak ada menu yang tersedia!")
            return

        tampilkan_menu(menu_tersedia)

        kode = input_teks(
            "Masukkan kode menu "
            "(0 untuk selesai): "
        ).upper()

        if kode == "0":
            break

        menu = cari_kode(kode)

        if menu is None:
            print("Menu tidak ditemukan!")
            continue

        if menu["stok"] <= 0:
            print("Menu sudah habis!")
            continue

        jumlah = input_angka(
            "Masukkan jumlah: ",
            minimal=1
        )

        jumlah_sebelumnya = sum(
            item["jumlah"]
            for item in pesanan
            if item["menu"]["kode"] == kode
        )

        if jumlah + jumlah_sebelumnya > menu["stok"]:
            print("Stok tidak mencukupi!")
            print("Stok tersedia:", menu["stok"])
            continue

        item_ada = False

        for item in pesanan:
            if item["menu"]["kode"] == kode:
                item["jumlah"] += jumlah
                item_ada = True
                break

        if not item_ada:
            pesanan.append({
                "menu": menu,
                "jumlah": jumlah
            })

        print("Menu berhasil ditambahkan ke pesanan!")

    if not pesanan:
        print("Pesanan kosong!")
        return

    print("\n=== RINGKASAN PESANAN ===")

    tampilkan_pesanan(pesanan)

    subtotal, diskon, total = hitung_total(pesanan)

    print("Subtotal :", rupiah(subtotal))
    print("Diskon   :", rupiah(diskon))
    print("Total     :", rupiah(total))

    konfirmasi = input_teks(
        "Lanjutkan pembayaran? (y/n): "
    ).lower()

    if konfirmasi != "y":
        print("Pesanan dibatalkan!")
        return

    bayar = input_angka(
        "Masukkan uang pembayaran: ",
        minimal=0
    )

    if bayar < total:
        print("Uang pembayaran tidak mencukupi!")
        print("Transaksi dibatalkan!")
        return

    kembalian = bayar - total

    # Pengurangan stok dilakukan setelah pembayaran berhasil
    for item in pesanan:
        item["menu"]["stok"] -= item["jumlah"]

    transaksi = {
        "pelanggan": nama_pelanggan,
        "items": [
            {
                "kode": item["menu"]["kode"],
                "nama": item["menu"]["nama"],
                "harga": item["menu"]["harga"],
                "jumlah": item["jumlah"]
            }
            for item in pesanan
        ],
        "subtotal": subtotal,
        "diskon": diskon,
        "total": total,
        "bayar": bayar,
        "kembalian": kembalian
    }

    riwayat_transaksi.append(transaksi)

    print("\n=== STRUK PEMBAYARAN ===")

    tabel = PrettyTable()

    tabel.field_names = [
        "Nama",
        "Harga",
        "Jumlah",
        "Subtotal"
    ]

    for item in pesanan:
        menu = item["menu"]

        tabel.add_row([
            menu["nama"],
            rupiah(menu["harga"]),
            item["jumlah"],
            rupiah(menu["harga"] * item["jumlah"])
        ])

    print(tabel)

    print("Pelanggan :", nama_pelanggan)
    print("Subtotal  :", rupiah(subtotal))
    print("Diskon    :", rupiah(diskon))
    print("Total     :", rupiah(total))
    print("Bayar     :", rupiah(bayar))
    print("Kembalian :", rupiah(kembalian))

    print("\nTransaksi berhasil!")
    print("Stok menu telah diperbarui.")