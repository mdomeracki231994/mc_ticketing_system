from django.urls import path

from Apps.ticket_management import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_tickets/', views.view_my_tickets, name='my_tickets'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),

    path('mark_closed/<int:ticket_id>/', views.mark_ticket_closed, name='mark_closed'),
    path('update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('permanently_delete/<int:ticket_id>/', views.permanently_delete_ticket, name='permanently_delete_ticket'),
    path('recover/<int:ticket_id>/', views.recover_ticket, name='recover_ticket'),
    path('all_deleted_tickets/', views.all_deleted_tickets, name='all_deleted_tickets'),
    path('all_closed_tickets/', views.all_closed_tickets, name='all_closed_tickets'),
]
