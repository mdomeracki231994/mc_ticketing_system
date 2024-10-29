from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return render(request, 'ticket_management/index.html')
    else:
        return redirect('login')

def create_ticket(request):
    return render(request, 'ticket_management/create_ticket.html')