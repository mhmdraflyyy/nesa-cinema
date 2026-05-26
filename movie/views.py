from django.shortcuts import render, get_object_or_404
from .models import Film, JadwalTayang


def daftar_film(request):
    genre = request.GET.get('genre')

    if genre:
        daftar_film = Film.objects.filter(genre__icontains=genre)
    else:
        daftar_film = Film.objects.all()

    return render(request, 'movie/daftar_film.html', {
        'daftar_film': daftar_film,
        'genre_aktif': genre
    })

def detail_film(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    jadwal = JadwalTayang.objects.filter(film=film)

    return render(request, 'movie/detail_film.html', {
        'film': film,
        'jadwal': jadwal
    })