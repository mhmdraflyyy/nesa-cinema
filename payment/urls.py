from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.index_payment, name='index_payment'),
]