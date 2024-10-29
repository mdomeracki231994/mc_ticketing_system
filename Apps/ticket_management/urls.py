from django.urls import path, include

from Apps.ticket_management import views

urlpatterns = [
    path('', views.home, name='home' ),
]
