from django.urls import path

from app_user import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]