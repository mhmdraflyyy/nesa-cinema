from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('<int:tiket_id>/', views.index_payment, name='index_payment'),
]