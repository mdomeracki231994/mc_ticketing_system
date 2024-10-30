from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from Apps.app_user.models import AppUser
from Apps.org_management.models import Organization
from Apps.ticket_management.models import Ticket


@login_required(login_url='/accounts/login/')
def home(request):
    tickets = Ticket.objects.filter(
        mark_deleted=False
    )
    total_ticket_count = tickets.count()
    context = {
        'tickets': tickets,
        'total_ticket_count': total_ticket_count,
    }
    return render(request, 'ticket_management/index.html', context)


@login_required
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST['name']
        description = request.POST['description']
        status = request.POST['status']
        priority = request.POST['priority']
        created_by = request.user
        assigned_user_id = request.POST['assigned_user']
        assigned_to = get_object_or_404(AppUser, pk=assigned_user_id)

        new_ticket = Ticket.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            created_by=created_by,
            assigned_to=assigned_to
        )
        new_ticket.save()
        return redirect('home')

    users_org_id = request.user.org_id
    org = Organization.objects.get(id=users_org_id)
    all_users_for_org = AppUser.objects.filter(org=org)

    status = Ticket.STATUS_CHOICES
    priority = Ticket.PRIORITY_CHOICES
    context = {
        'users': all_users_for_org,
        'status': status,
        'priority': priority,
    }
    return render(request, 'ticket_management/create_ticket.html', context)


@login_required
def view_my_tickets(request):
    tickets = Ticket.objects.filter(
        assigned_to=request.user
    )
    total_ticket_count = tickets.count()
    context = {
        'tickets': tickets,
        'total_ticket_count': total_ticket_count,
    }
    return render(request, 'ticket_management/my_tickets.html', context)


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        ticket.title = request.POST.get('title', ticket.title)
        ticket.description = request.POST.get('description', ticket.description)
        ticket.priority = request.POST.get('priority', ticket.priority)
        ticket.save()
        return redirect('home')

    return render(request, 'ticket_management/ticket_details.html', {'ticket': ticket})


@login_required
def mark_ticket_closed(request, ticket_id):
    pass


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.mark_deleted = not ticket.mark_deleted
    ticket.save()
    return JsonResponse({'success': True})

@login_required
def recover_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.mark_deleted = False
    ticket.save()
    return JsonResponse({'success': True})


@login_required
def all_deleted_tickets(request):
    tickets = Ticket.objects.filter(
        mark_deleted=True
    )
    total_ticket_count = tickets.count()
    context = {
        'tickets': tickets,
        'total_ticket_count': total_ticket_count,
    }
    return render(request, 'ticket_management/all_deleted.html', context)
