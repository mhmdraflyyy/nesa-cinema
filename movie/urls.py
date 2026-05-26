from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.daftar_film, name='daftar_film'),
    path('film/<int:film_id>/', views.detail_film, name='detail_film'),
]