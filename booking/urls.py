from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('pesan/<int:jadwal_id>/', views.pesan_tiket, name='pesan_tiket'),
    path('tiket/<int:tiket_id>/', views.detail_tiket, name='detail_tiket'),
]