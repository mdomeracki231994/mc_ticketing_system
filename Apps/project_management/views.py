from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Apps.project_management.models import Project


@login_required
def index(request):
    projects = Project.objects.filter(
        organization=request.user.org_id,
    )
    total_projects = projects.count()
    context = {
        'projects': projects,
        'total_projects': total_projects,
    }
    return render(request, 'project_management/index.html', context)

@login_required
def project_detail(request, project_id):
    user = request.user
    user.current_active_project = project_id
    user.save()
    project = Project.objects.get(id=project_id)
    context = {
        'project': project,
    }
    return render(request, 'project_management/project_details.html', context)

@login_required
def create_project(request):
    pass


@login_required
def update_project(request):
    pass


@login_required
def delete_project(request):
    pass
