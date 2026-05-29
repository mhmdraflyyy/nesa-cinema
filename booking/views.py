import random
from django.shortcuts import render, redirect, get_object_or_404
from movie.models import JadwalTayang
from .models import Tiket, Kursi
from .services import TiketService


def pesan_tiket(request, jadwal_id):

    jadwal = get_object_or_404(JadwalTayang, id=jadwal_id)

    rows = ['A','B','C','D','E','F','G','H','I','J']
    left_cols = [1,2,3,4,5]
    right_cols = [6,7,8,9,10]

    
    kursi_dipesan = Tiket.objects.filter(
        jadwal=jadwal,
        status='AKTIF'
    ).values_list('kursi__nomor_kursi', flat=True).distinct()

    kursi_dipesan = list(kursi_dipesan)

    seat_rows = []

    for row in rows:
        kiri = []
        kanan = []

        for col in left_cols:
            nomor = f"{row}{col}"
            kiri.append({
                'nomor': nomor,
                'dipesan': nomor in kursi_dipesan
            })

        for col in right_cols:
            nomor = f"{row}{col}"
            kanan.append({
                'nomor': nomor,
                'dipesan': nomor in kursi_dipesan
            })

        seat_rows.append({
            'kiri': kiri,
            'kanan': kanan
        })

    if request.method == 'POST':

        nama_pemesan = request.POST.get('nama_pemesan')
        jenis_tiket = request.POST.get('jenis_tiket')

        kursi_ids = request.POST.getlist('kursi')
        kursi_ids = list(dict.fromkeys(kursi_ids))


        kursi_dipilih = Kursi.objects.filter(
            nomor_kursi__in=kursi_ids,
            studio=jadwal.studio
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
                'seat_rows': seat_rows,
                'error': error,
            })

    return render(request, 'booking/pesan_tiket.html', {
        'jadwal': jadwal,
        'seat_rows': seat_rows,
    })

def detail_tiket(request, tiket_id):

    tiket = get_object_or_404(Tiket, id=tiket_id)

    return render(request, 'booking/detail_tiket.html', {
        'tiket': tiket
    })