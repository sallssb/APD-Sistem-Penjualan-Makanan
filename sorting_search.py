# ==========================================
# SORTING DAN SEARCHING
# ==========================================

from data import daftar_menu


def bubble_sort(data, atribut, menurun=False):
    hasil = data.copy()

    for i in range(len(hasil) - 1):
        tertukar = False

        for j in range(len(hasil) - i - 1):
            kiri = hasil[j][atribut]
            kanan = hasil[j + 1][atribut]

            if isinstance(kiri, str):
                kiri = kiri.lower()
                kanan = kanan.lower()

            if (
                (not menurun and kiri > kanan)
                or (menurun and kiri < kanan)
            ):
                hasil[j], hasil[j + 1] = (
                    hasil[j + 1],
                    hasil[j]
                )

                tertukar = True

        if not tertukar:
            break

    return hasil


def cari_kode(kode):
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