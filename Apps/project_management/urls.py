from django.urls import path

from Apps.project_management import views


urlpatterns = [
    path('', views.index, name='projects_index'),
    path('project_details/<int:project_id>/', views.project_detail, name='project_detail'),
]