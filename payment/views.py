from django.shortcuts import render


# Create your views here
def index_payment(request):
    return render(request, 'payment/index_payment.html')