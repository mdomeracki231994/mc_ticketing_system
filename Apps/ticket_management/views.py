from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from Apps.app_user.models import AppUser
from Apps.org_management.models import Organization
from Apps.ticket_management.models import Ticket


def home(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(
            Q(created_by=request.user) | Q(assigned_to=request.user),
            mark_deleted=False
        )
        context = {
            'tickets': tickets,
        }
        return render(request, 'ticket_management/index.html', context)
    else:
        return redirect('login')


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
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.mark_deleted = not ticket.mark_deleted
    ticket.save()
    return JsonResponse({'success': True})
