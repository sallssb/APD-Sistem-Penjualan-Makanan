def bubble_sort(data, atribut, menurun=False):
    data = data.copy()

    for i in range(len(data)):
        for j in range(len(data) - 1 - i):

            if menurun:
                kondisi = (
                    data[j][atribut]
                    < data[j + 1][atribut]
                )
            else:
                kondisi = (
                    data[j][atribut]
                    > data[j + 1][atribut]
                )

            if kondisi:
                data[j], data[j + 1] = (
                    data[j + 1], data[j]
                )

    return data


def cari_kode(kode):
    from data import daftar_menu

    data_urut = bubble_sort(
        daftar_menu,
        "kode"
    )

    kiri = 0
    kanan = len(data_urut) - 1

    while kiri <= kanan:

        tengah = (kiri + kanan) // 2

        if data_urut[tengah]["kode"] == kode:
            return data_urut[tengah]

        elif data_urut[tengah]["kode"] < kode:
            kiri = tengah + 1

        else:
            kanan = tengah - 1

    return None