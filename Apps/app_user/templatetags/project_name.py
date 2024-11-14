from Apps.project_management.models import Project


def get_current_project_name(request):
    project_id = request.user.current_active_project
    project = Project.objects.get(id=project_id)
    return project.name
