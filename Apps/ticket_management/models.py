from django.db import models, transaction
from django.contrib.auth import get_user_model

from Apps.org_management.models import Organization

User = get_user_model()


class TicketNumberSequence(models.Model):
    org = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name="ticket_sequence")
    last_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.org.name} - Last Ticket Number: {self.last_number}"


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(default=None, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    mark_deleted = models.BooleanField(default=False)
    ticket_number = models.PositiveIntegerField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            with transaction.atomic():
                sequence, created = TicketNumberSequence.objects.get_or_create(org=self.org)
                sequence.last_number += 1
                self.ticket_number = sequence.last_number
                sequence.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.org.name} - Ticket #{self.ticket_number}: {self.title}"


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
