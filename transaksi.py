from datetime import datetime

from utils import (
    tampilkanHeader, bersihkanLayar, cetakTabel, formatRupiah,
    pilih, konfirmasi, tekanEnter,
)
from menuMakanan import pilihKodeMenu

aturanDiskon = ((100000, 10), (50000, 5))
tipePesanan = ("Makan di tempat", "Bawa pulang")
metodeBayar = ("Tunai", "QRIS", "Transfer")
kelipatanUang = (5000, 10000, 50000, 100000)
maksJumlahSekaliPilih = 10


def susunItem(menu, keranjang):
    items = []
    for kode, jumlah in keranjang.items():
        info = menu[kode]
        items.append({
            "kode": kode,
            "nama": info["nama"],
            "harga": info["harga"],
            "jumlah": jumlah,
            "subtotal": info["harga"] * jumlah,
        })
    return items


def hitungSubtotal(items):
    total = 0
    for item in items:
        total += item["subtotal"]
    return total


def hitungDiskon(subtotal):
    for batas, persen in aturanDiskon:
        if subtotal >= batas:
            return persen, subtotal * persen // 100
    return 0, 0


def buatPilihanNominal(total):
    kandidat = {total}  
    for kelipatan in kelipatanUang:
        pembulatan = -(-total // kelipatan) * kelipatan  
        kandidat.add(pembulatan)
    return sorted(kandidat)


def tampilkanKeranjang(items):
    baris = []
    for nomor, item in enumerate(items, start=1):
        baris.append([nomor, item["kode"], item["nama"],
                      formatRupiah(item["harga"]), item["jumlah"],
                      formatRupiah(item["subtotal"])])
    cetakTabel("Keranjang Belanja",
               ["No", "Kode", "Nama Menu", "Harga", "Qty", "Subtotal"],
               baris, kolomKanan=("No", "Harga", "Qty", "Subtotal"))
    print(f"Subtotal : {formatRupiah(hitungSubtotal(items))}\n")


def cetakStruk(trx):
    bersihkanLayar()
    tampilkanHeader("Struk Pembelian")
    print(f"No. Transaksi : {trx['id']}")
    print(f"Waktu         : {trx['waktu']}")
    print(f"Tipe Pesanan  : {trx['tipe']}")
    print(f"Pembayaran    : {trx['metode']}\n")

    baris = []
    for nomor, item in enumerate(trx["items"], start=1):
        baris.append([nomor, item["nama"], item["jumlah"],
                      formatRupiah(item["harga"]),
                      formatRupiah(item["subtotal"])])
    cetakTabel(f"Rincian {trx['id']}",
               ["No", "Menu", "Qty", "Harga", "Subtotal"],
               baris, kolomKanan=("No", "Qty", "Harga", "Subtotal"))

    ringkasan = [
        ["Subtotal", formatRupiah(trx["subtotal"])],
        [f"Diskon ({trx['diskonPersen']}%)", "- " + formatRupiah(trx["diskon"])],
        ["TOTAL", formatRupiah(trx["total"])],
        ["Bayar", formatRupiah(trx["bayar"])],
        ["Kembalian", formatRupiah(trx["kembali"])],
    ]
    cetakTabel("Ringkasan Pembayaran", ["Keterangan", "Jumlah"],
               ringkasan, kolomKanan=("Jumlah",))
    print("Terima kasih, selamat menikmati!")


def tambahKeKeranjang(menu, keranjang):
    tersedia = {kode: info for kode, info in menu.items()
                if info["stok"] - keranjang.get(kode, 0) > 0}
    if not tersedia:
        print("Semua stok menu sudah masuk keranjang / habis.")
        tekanEnter()
        return

    kode = pilihKodeMenu(tersedia, "Pilih menu")
    if kode is None:
        return

    sisa = menu[kode]["stok"] - keranjang.get(kode, 0)
    batas = min(sisa, maksJumlahSekaliPilih)
    jumlah = pilih(f"Jumlah '{menu[kode]['nama']}' (sisa stok {sisa})",
                   [(str(n), n) for n in range(1, batas + 1)])
    if jumlah is None:
        return

    keranjang[kode] = keranjang.get(kode, 0) + jumlah


def hapusDariKeranjang(menu, keranjang):
    pilihan = [(f"{kode} | {menu[kode]['nama']} x{jumlah}", kode)
               for kode, jumlah in keranjang.items()]
    pilihan.append(("<< Batal", None))
    kode = pilih("Hapus item", pilihan)
    if kode is not None:
        del keranjang[kode]


def prosesPembayaran(menu, keranjang, riwayat):
    items = susunItem(menu, keranjang)
    subtotal = hitungSubtotal(items)
    persen, diskon = hitungDiskon(subtotal)
    total = subtotal - diskon

    bersihkanLayar()
    tampilkanHeader("Pembayaran")
    tampilkanKeranjang(items)
    print(f"Diskon ({persen}%) : - {formatRupiah(diskon)}")
    print(f"TOTAL BAYAR   : {formatRupiah(total)}\n")

    tipe = pilih("Tipe pesanan", list(tipePesanan))
    if tipe is None:
        return False
    metode = pilih("Metode pembayaran", list(metodeBayar))
    if metode is None:
        return False

    if metode == "Tunai":
        pilihan = [(formatRupiah(n) + ("  (uang pas)" if n == total else ""), n)
                   for n in buatPilihanNominal(total)]
        bayar = pilih("Uang yang diterima", pilihan)
        if bayar is None:
            return False
    else:
        bayar = total  
    if not konfirmasi("Proses transaksi ini?"):
        return False

    for item in items:
        menu[item["kode"]]["stok"] -= item["jumlah"]

    trx = {
        "id": f"TRX{len(riwayat) + 1:03d}",
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "tipe": tipe,
        "metode": metode,
        "items": items,
        "subtotal": subtotal,
        "diskonPersen": persen,
        "diskon": diskon,
        "total": total,
        "bayar": bayar,
        "kembali": bayar - total,
    }
    riwayat.append(trx)
    cetakStruk(trx)
    return True


def transaksiPenjualan(menu, riwayat):
    keranjang = {}  

    while True:
        bersihkanLayar()
        tampilkanHeader("Transaksi Penjualan")
        if keranjang:
            tampilkanKeranjang(susunItem(menu, keranjang))
        else:
            print("Keranjang masih kosong.\n")

        aksi = [("Tambah item", "tambah")]
        if keranjang:
            aksi += [("Hapus item", "hapus"), ("Lanjut ke pembayaran", "bayar")]
        aksi.append(("Batalkan transaksi", "batal"))

        pilihan = pilih("Pilih aksi", aksi)
        if pilihan in (None, "batal"):
            return
        elif pilihan == "tambah":
            tambahKeKeranjang(menu, keranjang)
        elif pilihan == "hapus":
            hapusDariKeranjang(menu, keranjang)
        elif pilihan == "bayar":
            if prosesPembayaran(menu, keranjang, riwayat):
                tekanEnter()
                return