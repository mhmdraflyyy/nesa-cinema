from django.db import models
from movie.models import Studio, JadwalTayang


class Kursi(models.Model):
    nomor_kursi = models.CharField(max_length=5)

    STATUS_CHOICES = [
        ('TERSEDIA', 'Tersedia'),
        ('DIPESAN', 'Dipesan'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='TERSEDIA'
    )

    studio = models.ForeignKey(
        Studio,
        on_delete=models.CASCADE
    )

    def pilih_kursi(self):
        if self.status == 'DIPESAN':
            raise ValueError("Kursi sudah dipesan")

        self.status = 'DIPESAN'
        self.save()

    def batalkan_kursi(self):
        self.status = 'TERSEDIA'
        self.save()

    def __str__(self):
        return f"{self.nomor_kursi} - {self.studio}"


class Tiket(models.Model):
    JENIS_TIKET_CHOICES = [
        ('reguler', 'Reguler'),
        ('pelajar', 'Pelajar'),
        ('weekend', 'Weekend'),
    ]

    STATUS_CHOICES = [
        ('AKTIF', 'Aktif'),
        ('BATAL', 'Batal'),
    ]

    kode_booking = models.CharField(max_length=20)
    nama_pemesan = models.CharField(max_length=100)
    jenis_tiket = models.CharField(max_length=20, choices=JENIS_TIKET_CHOICES)
    harga = models.IntegerField()
    jumlah_kursi = models.IntegerField()
    total_harga = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AKTIF'
    )

    jadwal = models.ForeignKey(
        JadwalTayang,
        on_delete=models.CASCADE
    )

    kursi = models.ManyToManyField(Kursi)

    def simpan_total(self, total):
        if total < 0:
            raise ValueError("Total harga tidak boleh negatif")

        self.total_harga = total

    def cetak_tiket(self):
        return f"Tiket {self.kode_booking}"

    def batalkan_tiket(self):
        self.status = 'BATAL'
        self.save()

        for kursi in self.kursi.all():
            kursi.batalkan_kursi()

    def __str__(self):
        return self.kode_booking