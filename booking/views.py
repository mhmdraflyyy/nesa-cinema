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

    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    left_cols = [1, 2, 3, 4, 5]

    right_cols = [6, 7, 8, 9, 10]

    if request.method == 'POST':

        nama_pemesan = request.POST.get('nama_pemesan')

        jenis_tiket = request.POST.get('jenis_tiket')

        kursi_ids = request.POST.getlist('kursi')

        kursi_ids = list(dict.fromkeys(kursi_ids))

        kursi_dipilih = Kursi.objects.filter(
            nomor_kursi__in=kursi_ids,
            studio=jadwal.studio,
            status='TERSEDIA'
        )

        kode_booking = f"BK{random.randint(1000, 9999)}"

        try:

            tiket = TiketService.buat_tiket(
                kode_booking=kode_booking,
                nama_pemesan=nama_pemesan,
                jadwal=jadwal,
                daftar_kursi=kursi_dipilih,
                jenis_tiket=jenis_tiket
            )

            return redirect(
                'booking:detail_tiket',
                tiket_id=tiket.id
            )

        except ValueError as error:

            return render(request, 'booking/pesan_tiket.html', {

                'jadwal': jadwal,

                'daftar_kursi': daftar_kursi,

                'error': error,

                'rows': rows,

                'left_cols': left_cols,

                'right_cols': right_cols

            })

    return render(request, 'booking/pesan_tiket.html', {

        'jadwal': jadwal,

        'daftar_kursi': daftar_kursi,

        'rows': rows,

        'left_cols': left_cols,

        'right_cols': right_cols

    })


def detail_tiket(request, tiket_id):

    tiket = get_object_or_404(Tiket, id=tiket_id)

    return render(request, 'booking/detail_tiket.html', {
        'tiket': tiket
    })