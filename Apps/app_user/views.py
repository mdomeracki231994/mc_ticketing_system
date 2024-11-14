from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from Apps.app_user.models import AppUser
from Apps.org_management.models import Organization


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        org_name = request.POST['org_name']
        org = Organization.objects.create(name=org_name)
        new_user = AppUser.objects.create_user(
            email=email,
            password=password,
            is_active=True,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            org_id=org.id,
        )
        new_user.role = AppUser.SITE_OWNER
        new_user.user_permissions.all()
        new_user.save()
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('projects_index')
    return render(request, 'app_user/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('projects_index')
        else:
            print("Error")
    return render(request, 'app_user/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def can_delete(check_user: AppUser):
    if check_user.FULL_EMPLOYEE or check_user.MANAGER or check_user.SITE_OWNER or check_user.SITE_ADMIN:
        return True
    return False
