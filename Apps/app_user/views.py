from django.contrib.auth import logout, authenticate
from django.shortcuts import render, redirect


def signup(request):
    return render(request, 'app_user/signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request)
            return redirect('home')
    return render(request, 'app_user/login.html')


def logout_view(request):
    logout(request)
    return redirect(login)
