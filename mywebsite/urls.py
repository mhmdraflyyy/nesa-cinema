from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return redirect('login')


urlpatterns = [
    path('', home, name='home'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('movie/', include('movie.urls')),
    path('booking/', include('booking.urls')),
    path('payment/', include('payment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)