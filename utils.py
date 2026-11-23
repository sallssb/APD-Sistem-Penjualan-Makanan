import os

import inquirer
from inquirer.errors import ValidationError
from prettytable import PrettyTable

namaToko = "WARUNG MAKAN SANRIO"
lebarHeader = 64


def bersihkanLayar():
    os.system("cls" if os.name == "nt" else "clear")


def tampilkanHeader(judul):
    garis = "=" * lebarHeader
    print(garis)
    print(namaToko.center(lebarHeader))
    print("Sistem Penjualan Makanan".center(lebarHeader))
    print("-" * lebarHeader)
    print(judul.upper().center(lebarHeader))
    print(garis)


def formatRupiah(nilai):
    return "Rp {:,}".format(int(nilai)).replace(",", ".")


def cetakTabel(judul, kolom, baris, kolomKanan=()):
    tabel = PrettyTable()
    tabel.title = judul
    tabel.field_names = kolom
    for namaKolom in kolom:
        tabel.align[namaKolom] = "r" if namaKolom in kolomKanan else "l"
    for isi in baris:
        tabel.add_row(isi)
    print(tabel)


def pilih(pesan, pilihan):
    try:
        return inquirer.list_input(pesan, choices=pilihan)
    except KeyboardInterrupt:
        return None


def konfirmasi(pesan, default=True):
    """Pertanyaan Ya/Tidak."""
    try:
        return inquirer.confirm(pesan, default=default)
    except KeyboardInterrupt:
        return False


def inputTeks(pesan, validasi=None, default=""):
    try:
        if validasi is None:
            hasil = inquirer.text(pesan, default=default)
        else:
            hasil = inquirer.text(pesan, validate=validasi, default=default)
        return hasil.strip()
    except KeyboardInterrupt:
        return None


def tekanEnter():
    pilih("Selesai", ["Kembali ke menu"])


def validatorAngka(minimum=0):
    def cek(jawaban, current):
        teks = str(current).strip()
        try:
            nilai = int(teks)
        except ValueError:
            raise ValidationError("", reason="Harus berupa angka bulat.")
        if nilai < minimum:
            raise ValidationError("", reason=f"Nilai minimal {minimum}.")
        return True
    return cek


def validatorKode(menu):
    def cek(jawaban, current):
        kode = str(current).strip().upper()
        if not kode:
            raise ValidationError("", reason="Kode tidak boleh kosong.")
        if not kode.isalnum():
            raise ValidationError("", reason="Kode hanya boleh huruf dan angka.")
        if kode in menu:
            raise ValidationError("", reason="Kode sudah digunakan.")
        return True
    return cek


def validatorNama(menu):

    def cek(jawaban, current):
        nama = str(current).strip()
        if len(nama) < 2:
            raise ValidationError("", reason="Nama minimal 2 karakter.")
        namaAda = {info["nama"].lower() for info in menu.values()}
        if nama.lower() in namaAda:
            raise ValidationError("", reason="Nama menu sudah ada.")
        return True
    return cek