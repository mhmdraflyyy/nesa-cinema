from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Tiket  
from .models import Payment       

def index_payment(request, tiket_id):
    
    tiket = get_object_or_404(Tiket, id=tiket_id)

    
    if request.method == 'POST':
        method_terpilih = request.POST.get('payment_method')

        Payment.objects.create(
            tiket=tiket,
            amount=tiket.total_harga, 
            payment_method=method_terpilih,
            status='SUCCESS'          
        )

        return redirect('booking:detail_tiket', tiket_id=tiket.id) 

    
    return render(request, 'payment/payment_page.html', {'tiket': tiket})
