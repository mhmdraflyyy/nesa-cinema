from django.db import models


class Film(models.Model):
    judul = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    durasi = models.IntegerField()
    sinopsis = models.TextField()
    poster = models.ImageField(upload_to='poster/', blank=True, null=True)

    def __str__(self):
        return self.judul


class Studio(models.Model):
    nomor_studio = models.IntegerField()
    kapasitas = models.IntegerField()

    def tampilkan_info(self):
        return f"Studio {self.nomor_studio} kapasitas {self.kapasitas}"

    def __str__(self):
        return f"Studio {self.nomor_studio}"


class JadwalTayang(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    tanggal = models.DateField()
    jam = models.TimeField()
    harga_dasar = models.PositiveIntegerField(default=35000)

    def tampilkan_jadwal(self):
        return f"{self.film.judul} - {self.tanggal} {self.jam}"

    def __str__(self):
        return f"{self.film.judul} | {self.tanggal} {self.jam}"