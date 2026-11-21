import inquirer
from data import KATEGORI


def rupiah(nominal):
    return f"Rp{nominal:,.0f}".replace(",", ".")


def input_teks(pesan):
    while True:
        teks = input(pesan).strip()

        if teks:
            return teks
        else:
            print("Input tidak boleh kosong!")


def input_angka(pesan, minimal=0):
    while True:
        try:
            angka = int(input(pesan))

            if angka >= minimal:
                return angka
            else:
                print(f"Angka minimal adalah {minimal}!")

        except ValueError:
            print("Masukkan angka yang valid!")


def pilih_opsi(pesan, pilihan):
    pertanyaan = [
        inquirer.List(
            "pilihan",
            message=pesan,
            choices=pilihan
        )
    ]

    jawaban = inquirer.prompt(pertanyaan)

    if jawaban is None:
        return None

    return jawaban["pilihan"]


def pilih_kategori():
    return pilih_opsi(
        "Pilih kategori:",
        list(KATEGORI)
    )