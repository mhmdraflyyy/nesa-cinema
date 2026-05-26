import random
from django.shortcuts import render, redirect, get_object_or_404
from movie.models import JadwalTayang
from .models import Tiket, Kursi
from .services import TiketService


def pesan_tiket(request, jadwal_id):
    jadwal = get_object_or_404(JadwalTayang, id=jadwal_id)
    daftar_kursi = Kursi.objects.filter(
        studio=jadwal.studio,
        status='TERSEDIA'
    )

    if request.method == 'POST':
        nama_pemesan = request.POST.get('nama_pemesan')
        jenis_tiket = request.POST.get('jenis_tiket')
        kursi_ids = request.POST.getlist('kursi')

        kursi_dipilih = Kursi.objects.filter(id__in=kursi_ids)

        kode_booking = f"BK{random.randint(1000, 9999)}"

        try:
            tiket = TiketService.buat_tiket(
                kode_booking=kode_booking,
                nama_pemesan=nama_pemesan,
                jadwal=jadwal,
                daftar_kursi=kursi_dipilih,
                jenis_tiket=jenis_tiket
            )

            return redirect('booking:detail_tiket', tiket_id=tiket.id)

        except ValueError as error:
            return render(request, 'booking/pesan_tiket.html', {
                'jadwal': jadwal,
                'daftar_kursi': daftar_kursi,
                'error': error
            })

    return render(request, 'booking/pesan_tiket.html', {
        'jadwal': jadwal,
        'daftar_kursi': daftar_kursi
    })


def detail_tiket(request, tiket_id):
    tiket = get_object_or_404(Tiket, id=tiket_id)

    return render(request, 'booking/detail_tiket.html', {
        'tiket': tiket
    })