from django.urls import path, include

from Apps.ticket_management import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('create_ticket/', views.create_ticket, name='create_ticket' ),
    path('update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
]
