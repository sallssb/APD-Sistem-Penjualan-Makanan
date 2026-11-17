""SISTEM PENJUALAN MAKANAN - Proyek UAS APD

Cara menjalankan: python penjualan_makanan.py
Memerlukan Python 3, tanpa instalasi library tambahan.
Data menu dan transaksi disimpan di memori selama program berjalan.
Saat program ditutup, data kembali ke data awal pada eksekusi berikutnya.

Pseudocode proses utama:
1. Siapkan daftar menu, kategori tetap, dan riwayat transaksi.
2. Ulangi tampilan menu utama sampai pengguna memilih keluar.
3. Jalankan tambah/tampil/ubah/hapus/cari/urutkan sesuai pilihan.
4. Untuk pesanan, masukkan kode dan jumlah sampai checkout atau batal.
5. Hitung subtotal, diskon, dan total; validasi uang pembayaran.
6. Simpan transaksi setelah pembayaran cukup, lalu tampilkan struk.
7. Laporan menjumlahkan transaksi berhasil dan kategori yang terjual.

Aturan contoh: diskon 10% untuk subtotal minimal Rp100.000.
Diskon dibulatkan ke rupiah terdekat menggunakan round().
"""

# Tuple untuk kategori tetap; list berisi dictionary sebagai data bertingkat.
KATEGORI = ("Makanan", "Minuman")
PERSEN_DISKON = 0.10  # float
BATAS_DISKON = 100000
daftar_menu = [
    {"kode": "M01", "nama": "Nasi Goreng", "kategori": "Makanan", "harga": 18000},
    {"kode": "M02", "nama": "Mie Goreng", "kategori": "Makanan", "harga": 15000},
    {"kode": "M03", "nama": "Ayam Geprek", "kategori": "Makanan", "harga": 20000},
    {"kode": "D01", "nama": "Es Teh", "kategori": "Minuman", "harga": 5000},
    {"kode": "D02", "nama": "Es Jeruk", "kategori": "Minuman", "harga": 8000},
]
riwayat_transaksi = []


def rupiah(nilai):
    return "Rp" + format(nilai, ",").replace(",", ".")


def input_teks(pesan):
    while True:
        teks = input(pesan).strip()
        if teks:
            return teks
        print("Input tidak boleh kosong.")


def input_angka(pesan, minimum=0, maksimum=None):
    while True:
        try:
            angka = int(input(pesan))
            if angka < minimum or (maksimum is not None and angka > maksimum):
                print("Angka di luar batas yang diizinkan.")
            else:
                return angka
        except ValueError:
            print("Masukkan bilangan bulat, tanpa titik atau koma.")


def pilih_kategori():
    for nomor, kategori in enumerate(KATEGORI, 1):
        print(f"{nomor}. {kategori}")
    pilihan = input_angka("Pilih kategori: ", 1, len(KATEGORI))
    return KATEGORI[pilihan - 1]


def bubble_sort(data, atribut, menurun=False):
    # Salinan list agar pencarian/pengurutan tidak mengubah data sumber.
    hasil = data.copy()
    for i in range(len(hasil) - 1):
        tertukar = False
        for j in range(len(hasil) - i - 1):
            kiri = hasil[j][atribut]
            kanan = hasil[j + 1][atribut]
            if isinstance(kiri, str):
                kiri = kiri.lower()
                kanan = kanan.lower()
            if (not menurun and kiri > kanan) or (menurun and kiri < kanan):
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
                tertukar = True
        if not tertukar:
            break
    return hasil


def cari_kode(kode):
    # Binary Search wajib menggunakan data yang telah terurut berdasarkan kode.
    data = bubble_sort(daftar_menu, "kode")
    kode = kode.strip().upper()
    bawah = 0
    atas = len(data) - 1
    while bawah <= atas:
        tengah = (bawah + atas) // 2
        if data[tengah]["kode"] == kode:
            return data[tengah]
        elif data[tengah]["kode"] < kode:
            bawah = tengah + 1
        else:
            atas = tengah - 1
    return None


def tampilkan_menu(data):
    if not data:
        print("Tidak ada menu yang dapat ditampilkan.")
        return
    print("\nDAFTAR MENU")
    for menu in data:
        print(f"{menu['kode']} | {menu['nama']} | {menu['kategori']} | {rupiah(menu['harga'])}")


def tambah_menu():
    while True:
        kode = input_teks("Kode menu (huruf/angka, contoh M04): ").upper()
        if not kode.isascii() or not kode.isalnum():
            print("Kode hanya boleh berisi huruf A-Z dan angka 0-9.")
        elif cari_kode(kode) is not None:
            print("Kode sudah digunakan.")
        else:
            break
    nama = input_teks("Nama menu: ").title()
    kategori = pilih_kategori()
    harga = input_angka("Harga (Rp): ", 1)
    daftar_menu.append({"kode": kode, "nama": nama, "kategori": kategori, "harga": harga})
    print("Menu berhasil ditambahkan.")


def ubah_menu():
    tampilkan_menu(daftar_menu)
    if not daftar_menu:
        return
    menu = cari_kode(input_teks("Kode menu yang diubah: "))
    if menu is None:
        print("Kode tidak ditemukan.")
        return
    nama = input_teks("Nama baru: ").title()
    kategori = pilih_kategori()
    harga = input_angka("Harga baru (Rp): ", 1)
    menu.update({"nama": nama, "kategori": kategori, "harga": harga})
    print("Menu berhasil diubah. Kode menu tetap.")


def hapus_menu():
    tampilkan_menu(daftar_menu)
    if not daftar_menu:
        return
    menu = cari_kode(input_teks("Kode menu yang dihapus: "))
    if menu is None:
        print("Kode tidak ditemukan.")
        return
    print(f"Hapus {menu['nama']}?")
    if input_angka("1. Ya | 0. Batal: ", 0, 1) == 1:
        daftar_menu.remove(menu)
        print("Menu berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")


def cari_menu():
    print("1. Cari kode (Binary Search)\n2. Cari sebagian nama")
    pilihan = input_angka("Pilih pencarian: ", 1, 2)
    if pilihan == 1:
        menu = cari_kode(input_teks("Kode menu: "))
        hasil = [menu] if menu is not None else []
    else:
        kata = input_teks("Nama menu: ").lower()
        hasil = []
        for menu in daftar_menu:
            if kata in menu["nama"].lower():
                hasil.append(menu)
    tampilkan_menu(hasil)


def urutkan_menu():
    print("1. Berdasarkan nama\n2. Berdasarkan harga")
    pilihan = input_angka("Pilih kriteria: ", 1, 2)
    atribut = "nama" if pilihan == 1 else "harga"
    print("1. Menaik (A-Z / termurah)\n2. Menurun (Z-A / termahal)")
    menurun = input_angka("Pilih urutan: ", 1, 2) == 2
    tampilkan_menu(bubble_sort(daftar_menu, atribut, menurun))


def hitung_total(pesanan):
    subtotal = 0
    for item in pesanan:
        subtotal += item["harga"] * item["jumlah"]
    diskon = round(subtotal * PERSEN_DISKON) if subtotal >= BATAS_DISKON else 0
    return subtotal, diskon, subtotal - diskon


def tampilkan_pesanan(pesanan):
    for item in pesanan:
        total_item = item["harga"] * item["jumlah"]
        print(f"{item['nama']} x{item['jumlah']} @ {rupiah(item['harga'])} = {rupiah(total_item)}")
    subtotal, diskon, total = hitung_total(pesanan)
    print(f"Subtotal : {rupiah(subtotal)}")
    print(f"Diskon   : {rupiah(diskon)}")
    print(f"Total    : {rupiah(total)}")


def buat_pesanan():
    if not daftar_menu:
        print("Tambahkan menu terlebih dahulu.")
        return
    pelanggan = input_teks("Nama pelanggan: ").title()
    pesanan = []
    while True:
        tampilkan_menu(daftar_menu)
        print("1. Tambah item\n2. Bayar\n0. Batalkan pesanan")
        pilihan = input_angka("Pilih: ", 0, 2)
        if pilihan == 0:
            print("Pesanan dibatalkan. Tidak dicatat sebagai penjualan.")
            return
        elif pilihan == 1:
            menu = cari_kode(input_teks("Kode menu: "))
            if menu is None:
                print("Kode tidak ditemukan.")
                continue
            jumlah = input_angka("Jumlah pesanan: ", 1)
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
            subtotal, diskon, total = hitung_total(pesanan)
            while True:
                bayar = input_angka("Uang pembayaran (0 untuk batal): ", 0)
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
                "kembalian": bayar - total,
            }
            riwayat_transaksi.append(transaksi)
            print(f"\nSTRUK #{transaksi['nomor']} | {pelanggan}")
            tampilkan_pesanan(pesanan)
            print(f"Bayar    : {rupiah(bayar)}")
            print(f"Kembalian: {rupiah(transaksi['kembalian'])}")
            print("Transaksi berhasil. Terima kasih!")
            return


def laporan_penjualan():
    if not riwayat_transaksi:
        print("Belum ada transaksi berhasil.")
        return
    omzet_kotor = 0
    total_diskon = 0
    pendapatan = 0
    jumlah_item = 0
    kategori_terjual = set()  # Set mencegah kategori terhitung berulang.
    print("\nLAPORAN PENJUALAN")
    for transaksi in riwayat_transaksi:
        print(f"\n#{transaksi['nomor']} | {transaksi['pelanggan']}")
        tampilkan_pesanan(transaksi["pesanan"])
        omzet_kotor += transaksi["subtotal"]
        total_diskon += transaksi["diskon"]
        pendapatan += transaksi["total"]
        for item in transaksi["pesanan"]:
            jumlah_item += item["jumlah"]
            kategori_terjual.add(item["kategori"])
    print(f"\nJumlah transaksi : {len(riwayat_transaksi)}")
    print(f"Jumlah item      : {jumlah_item}")
    print(f"Omzet kotor      : {rupiah(omzet_kotor)}")
    print(f"Total diskon     : {rupiah(total_diskon)}")
    print(f"Pendapatan       : {rupiah(pendapatan)}")
    print(f"Kategori terjual : {len(kategori_terjual)} jenis")
    for kategori in KATEGORI:
        if kategori in kategori_terjual:
            print(f"- {kategori}")


def main():
    berjalan = True
    print("Data tersimpan selama program berjalan saja.")
    print("Diskon 10% untuk subtotal minimal Rp100.000.")
    while berjalan:
        print("\n=== SISTEM PENJUALAN MAKANAN ===")
        print("1. Tambah menu\n2. Tampilkan menu\n3. Ubah menu\n4. Hapus menu")
        print("5. Cari menu\n6. Urutkan menu\n7. Buat pesanan\n8. Laporan penjualan\n9. Keluar")
        pilihan = input_angka("Pilih menu: ", 1, 9)
        if pilihan == 1:
            tambah_menu()
        elif pilihan == 2:
            tampilkan_menu(daftar_menu)
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
        else:
            berjalan = False
            print("Program selesai. Data sesi ini tidak disimpan ke file.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan. Data sesi ini tidak disimpan ke file.")