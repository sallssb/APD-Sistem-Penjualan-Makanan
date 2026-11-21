# ==========================================
# INPUT DAN FORMAT
# ==========================================

import inquirer
from data import KATEGORI


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

            if angka < minimum or (
                maksimum is not None and angka > maksimum
            ):
                print("Angka di luar batas yang diizinkan.")
            else:
                return angka

        except ValueError:
            print("Masukkan bilangan bulat, tanpa titik atau koma.")


def pilih_opsi(pesan, pilihan):
    jawaban = inquirer.prompt([
        inquirer.List(
            "pilihan",
            message=pesan,
            choices=pilihan
        )
    ])

    if jawaban is None:
        raise KeyboardInterrupt

    return jawaban["pilihan"]


def pilih_kategori():
    return pilih_opsi(
        "Pilih kategori",
        list(KATEGORI)
    )