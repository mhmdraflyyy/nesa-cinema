from abc import ABC, abstractmethod
from django.db import transaction
from .models import Tiket


class HargaTiket(ABC):

    @abstractmethod
    def hitung(self, jadwal, jumlah):
        pass


class HargaReguler(HargaTiket):

    def hitung(self, jadwal, jumlah):
        return jadwal.harga_dasar * jumlah


class HargaPelajar(HargaTiket):

    def hitung(self, jadwal, jumlah):
        diskon = 0.2
        harga_setelah_diskon = jadwal.harga_dasar - (jadwal.harga_dasar * diskon)
        return int(harga_setelah_diskon * jumlah)


class HargaWeekend(HargaTiket):

    def hitung(self, jadwal, jumlah):
        tambahan = 10000
        return (jadwal.harga_dasar + tambahan) * jumlah


class TiketService:

    @staticmethod
    def pilih_jenis_harga(jenis_tiket):
        if jenis_tiket == 'pelajar':
            return HargaPelajar()
        elif jenis_tiket == 'weekend':
            return HargaWeekend()
        else:
            return HargaReguler()

    @staticmethod
    @transaction.atomic
    def buat_tiket(kode_booking, nama_pemesan, jadwal, daftar_kursi, jenis_tiket):
        jumlah_kursi = len(daftar_kursi)

        if jumlah_kursi <= 0:
            raise ValueError("Pilih minimal 1 kursi")

        aturan_harga = TiketService.pilih_jenis_harga(jenis_tiket)
        total = aturan_harga.hitung(jadwal, jumlah_kursi)

        tiket = Tiket(
            kode_booking=kode_booking,
            nama_pemesan=nama_pemesan,
            jadwal=jadwal,
            jenis_tiket=jenis_tiket,
            harga=jadwal.harga_dasar,
            jumlah_kursi=jumlah_kursi
        )

        tiket.simpan_total(total)
        tiket.save()

        for kursi in daftar_kursi:
            kursi.pilih_kursi()
            tiket.kursi.add(kursi)

        return tiket