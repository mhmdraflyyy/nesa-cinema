from django.shortcuts import render, redirect
from .models import Account


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(
                username=username,
                password=password
            )

            request.session['user_id'] = user.id
            request.session['username'] = user.username

            return redirect('movie:daftar_film')

        except Account.DoesNotExist:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Username atau Password salah'
                }
            )

    return render(request, 'accounts/login.html')


def dashboard(request):

    if 'user_id' not in request.session:
        return redirect('login')

    return render(
        request,
        'accounts/dashboard.html',
        {
            'username': request.session['username']
        }
    )


def logout_view(request):

    request.session.flush()

    return redirect('login')

def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if Account.objects.filter(username=username).exists():

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Username sudah digunakan'
                }
            )

        Account.objects.create(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'accounts/register.html')