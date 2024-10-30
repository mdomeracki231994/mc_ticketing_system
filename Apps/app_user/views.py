from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from Apps.app_user.models import AppUser


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        new_user = AppUser.objects.create_user(
            email=email,
            password=password,
            is_active=True,
            is_staff=True,
            is_site_owner=True,
        )
        new_user.save()
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'app_user/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            print("Error")
    return render(request, 'app_user/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
