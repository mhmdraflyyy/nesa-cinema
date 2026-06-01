from django.shortcuts import render, get_object_or_404, redirect
from .models import Film, JadwalTayang


def daftar_film(request):

    if 'user_id' not in request.session:
        return redirect('login')

    genre_aktif = request.GET.get('genre', '').strip()

    daftar_film = Film.objects.all()

    if genre_aktif:
        daftar_film = daftar_film.filter(genre__icontains=genre_aktif)

    daftar_genre = Film.objects.exclude(
        genre__isnull=True
    ).exclude(
        genre__exact=''
    ).values_list(
        'genre', flat=True
    ).distinct().order_by('genre')

    return render(request, 'movie/daftar_film.html', {
        'daftar_film': daftar_film,
        'daftar_genre': daftar_genre,
        'genre_aktif': genre_aktif,
    })


def detail_film(request, film_id):

    if 'user_id' not in request.session:
        return redirect('login')

    film = get_object_or_404(Film, id=film_id)
    jadwal = JadwalTayang.objects.filter(film=film)

    return render(request, 'movie/detail_film.html', {
        'film': film,
        'jadwal': jadwal
    })