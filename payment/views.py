from django.shortcuts import render
from django.http import HttpResponse

# Create your views here
def index_payment(request):
    return HttpResponse("Halaman payment berhasil dibuka")

